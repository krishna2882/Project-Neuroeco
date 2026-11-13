"""How much does WORDING move decisions compared with EMOTION? (exploratory, post hoc; P19)

For every model run and sub-experiment, the variance of the decision (S1: accept 0/1; S2/S3: share given/returned/sent)
is split by sequential increments in adjusted R² (entered in this order):
  design      offer / game / sent amount x stakes (the payoffs the experiment varies on purpose)
  emotion     the four message emotions (no-message trials excluded)
  message     which message within an emotion (5 per emotion)
  wording     the 4 instruction paraphrases (3 df, like-for-like with emotion)
  wording x design
  emotion x wording
  residual    sampling noise at T = 1.0 (same prompt, different draws)
Plus two intuitive numbers in percentage points: the spread of the four paraphrase means (max - min, neutral messages
only) and the largest |emotion - neutral| difference.

  python -m analysis.wording   -> results/wording/wording.md, wording.csv, fig_wording.png
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import statsmodels.formula.api as smf  # noqa: E402

from analysis.common import md_table  # noqa: E402
from config import RESULTS_DIR  # noqa: E402

OUT = RESULTS_DIR / "wording"
RUNS = [("main", "llama31_8b", "Llama-3.1-8B"), ("main", "qwen25_7b", "Qwen2.5-7B"), ("main", "mistral", "Mistral Large 4"),
        ("ext2", "qwen25_3b", "Qwen2.5-3B"), ("ext2", "qwen25_14b", "Qwen2.5-14B"), ("ext2", "qwen25_7b_q8", "Qwen2.5-7B Q8"),
        ("followup", "llama31_8b", "Llama-3.1-8B (follow-up)"), ("followup", "qwen25_7b", "Qwen2.5-7B (follow-up)")]
DESIGN = {"S1": "C(offer_share) * C(stakes)", "S2": "C(game) * C(stakes)", "S3a": "C(sent_share) * C(stakes)",
          "S3b": "C(stakes)"}
TEST = {"S1": "UG accept/reject", "S2": "UG/DG giving", "S3a": "TG returning", "S3b": "TG sending"}
PARTS = ["design", "emotion", "message", "wording", "wording x design", "emotion x wording", "residual"]
# validated categorical palette (dataviz reference) for the five explained parts; residual in neutral grey
COL = {"design": "#2a78d6", "emotion": "#eb6834", "message": "#1baf7a", "wording": "#eda100",
       "wording x design": "#008300", "emotion x wording": "#e87ba4", "residual": "#d6d5cf"}


def r2(d, f):
    return smf.ols(f"y ~ {f}", d).fit().rsquared_adj


def decompose(d, sub):
    des = DESIGN[sub]
    steps = [("design", des), ("emotion", f"{des} + C(emotion)"), ("message", f"{des} + C(emotion) + C(msg_id)"),
             ("wording", f"{des} + C(emotion) + C(msg_id) + C(paraphrase)"),
             ("wording x design", f"{des} + C(emotion) + C(msg_id) + C(paraphrase) * ({des})"),
             ("emotion x wording", f"{des} + C(emotion) + C(msg_id) + C(paraphrase) * ({des}) + C(emotion):C(paraphrase)")]
    out, prev = {}, 0.0
    for name, f in steps:
        r = r2(d, f)
        out[name] = 100 * (r - prev)
        prev = r
    out["residual"] = 100 * (1 - prev)
    neu = d[d.emotion == "neutral"]
    para_means = neu.groupby("paraphrase").y.mean()
    emo_means = d.groupby("emotion").y.mean()
    out["wording_range_pp"] = 100 * (para_means.max() - para_means.min())
    out["emotion_max_pp"] = 100 * (emo_means.drop("neutral") - emo_means["neutral"]).abs().max()
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for folder, model, label in RUNS:
        t = pd.read_csv(RESULTS_DIR / folder / "tidy_trials.csv", low_memory=False)
        t = t[(t.model_key == model) & ~t.is_baseline.astype(bool) & (t.emotion != "none")]
        for sub in ["S1", "S2", "S3a", "S3b"]:
            d = t[t.sub_exp == sub].copy()
            if d.empty:
                continue
            d["y"] = d.accept.astype(float) if sub == "S1" else d["share"].astype(float)
            d = d[d.y.notna()]
            if d.y.nunique() < 2:
                continue
            rows.append(dict(run=label, test=TEST[sub], n=len(d), **decompose(d, sub)))
    res = pd.DataFrame(rows)
    res.to_csv(OUT / "wording.csv", index=False)

    res["wording_vs_emotion"] = (res.wording / res.emotion.replace(0, np.nan)).round(1)
    share = res.assign(wording_beats_emotion=res.wording > res.emotion)
    n_beat = int(share.wording_beats_emotion.sum())
    med = res[["emotion", "message", "wording", "wording x design", "emotion x wording"]].median()

    # figure: stacked horizontal bars of % variance per run x test (explained parts only + residual)
    fig_rows = res.sort_values(["test", "run"])
    labels = [f"{r.run}: {r.test}" for r in fig_rows.itertuples()]
    fig, ax = plt.subplots(figsize=(11, 0.32 * len(fig_rows) + 1.6))
    left = np.zeros(len(fig_rows))
    for p in PARTS:
        v = np.clip(fig_rows[p].values, 0, None)  # small negative adjusted increments = chance level, drawn as 0
        ax.barh(range(len(fig_rows)), v, left=left, color=COL[p], edgecolor="white", linewidth=1.5, height=.78,
                label=p)
        left += v
    ax.set_yticks(range(len(fig_rows)))
    ax.set_yticklabels(labels, fontsize=8.5, color="#3d3d39")
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("% of variance in the decision", color="#55554f")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(colors="#55554f")
    ax.legend(ncol=7, loc="lower left", bbox_to_anchor=(-0.02, 1.005), frameon=False, fontsize=8.5,
              handlelength=1.2, columnspacing=1.0)
    fig.suptitle("What moves the decision? Payoffs, emotion, which message, and prompt wording",
                 x=0.01, ha="left", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(OUT / "fig_wording.png", dpi=180, facecolor="white")
    plt.close(fig)

    tab = res[["run", "test", "n", "design", "emotion", "message", "wording", "wording x design", "emotion x wording", "residual",
               "wording_range_pp", "emotion_max_pp"]].round(1)
    lines = ["# Wording vs emotion: what moves the decision? (exploratory, post hoc; P19)", "",
             "Sequential increments in **adjusted** R² (% of variance, corrected for the number of parameters, so a factor with "
             "many levels gets no credit for chance) in this order: design (payoffs) → emotion (3 df) → message within emotion "
             "→ prompt wording (4 paraphrases, 3 df: the like-for-like comparison with emotion) → wording × payoffs → "
             "emotion × wording → residual (sampling noise at T = 1.0). Small negative values = nothing beyond chance. "
             "No-message trials excluded. S1 outcome = accept (0/1); S2/S3 = share. `wording_range_pp` = max − min of the "
             "four paraphrase means (neutral messages); `emotion_max_pp` = largest |emotion − neutral| difference.", "",
             "![variance decomposition](fig_wording.png)", "",
             f"- **Wording (3 df) explains more variance than emotion (3 df) in {n_beat} of {len(res)} model × game combinations.**",
             f"- Median share of variance: emotion {med['emotion']:.1f}%, message within emotion {med['message']:.1f}%, "
             f"wording {med['wording']:.1f}% (plus {med['wording x design']:.1f}% wording × payoffs), "
             f"emotion × wording {med['emotion x wording']:.1f}%.",
             f"- Median spread across paraphrases {res.wording_range_pp.median():.0f} pp vs median largest emotion effect "
             f"{res.emotion_max_pp.median():.0f} pp.", "",
             md_table(tab), ""]
    (OUT / "wording.md").write_text("\n".join(lines))
    print("\n".join(lines[:9]))


if __name__ == "__main__":
    main()
