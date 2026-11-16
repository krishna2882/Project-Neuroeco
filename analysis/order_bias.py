"""Option-order effect in the ultimatum responder decision (S1), from data already collected (P22; post hoc, exploratory).

D6 randomised, per trial, whether "accept" or "reject" is named first (in the question and the JSON enum). It was a control
and was never analysed. This script asks how much the order alone moves the decision, and compares it with the emotion
effects measured in the same runs.

Order effect = P(accept | "accept" named first) - P(accept | "reject" named first), in percentage points, from a linear
probability model  accept ~ first + C(offer) + C(stakes) + C(emotion) + C(paraphrase)  with standard errors clustered by
message (the no-message baseline's four slots count as clusters), t with df = #clusters - 1. Order is randomised within
every cell, so it is balanced across emotions and the emotion effects reported elsewhere are not biased by it.

  python -m analysis.order_bias   -> results/order_bias/order_bias.md, order_bias.csv, fig_order_bias.png
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

from analysis.common import md_table
from config import DATA_DIR, RAW_DIR, RESULTS_DIR

OUT = RESULTS_DIR / "order_bias"
SCEN = DATA_DIR / "scenarios"
LABEL = {"qwen25_7b": "Qwen2.5-7B", "qwen25_7b_q8": "Qwen2.5-7B Q8", "qwen25_14b": "Qwen2.5-14B",
         "qwen25_3b": "Qwen2.5-3B", "llama31_8b": "Llama-3.1-8B", "mistral": "Mistral Large 4"}
RUNS = [(m, "main", "trials") for m in LABEL] + \
       [(m, "temp07", "trials") for m in ("qwen25_7b", "llama31_8b")] + \
       [(m, "followup", "followup_trials") for m in ("qwen25_7b", "llama31_8b")]


def load(model, tag, bank):
    path = RAW_DIR / model / f"{tag}.jsonl"
    if not path.exists():
        return None
    r = pd.read_json(path, lines=True, dtype=False)
    r = r[r.status == "ok"].sort_values("attempt").drop_duplicates("trial_id")
    b = pd.read_json(SCEN / f"{bank}.jsonl", lines=True, dtype=False)
    b = b[b.sub_exp == "S1"][["trial_id", "option_order", "emotion", "offer_share", "stakes", "paraphrase", "msg_id",
                              "extension"]]
    d = r[["trial_id", "decision"] + (["p_accept_lp", "decision_top_logprobs"] if "decision_top_logprobs" in r else [])]
    d = d.merge(b, on="trial_id")
    if d.empty:
        return None
    d["accept"] = (d.decision == "accept").astype(float)
    d["accept_first"] = d.option_order.str.startswith("accept").astype(float)
    d["offer"] = (100 * d.offer_share).round().astype(int)
    if "decision_top_logprobs" in d:  # only records from the corrected log-prob parser are valid (see analysis/common)
        d["p_lp"] = d.p_accept_lp.where(d.decision_top_logprobs.notna())
    if model == "llama31_8b" and tag == "main":
        lp = RAW_DIR / model / "main_lp.jsonl"
        if lp.exists():
            x = pd.read_json(lp, lines=True, dtype=False)
            x = x[x.status == "ok"].sort_values("attempt").drop_duplicates("trial_id")[["trial_id", "p_accept_lp"]]
            d = d.drop(columns=["p_lp"], errors="ignore").merge(x.rename(columns={"p_accept_lp": "p_lp"}),
                                                                on="trial_id", how="left")
    return d


def lpm(d, y="accept", x="accept_first", controls="C(offer) + C(stakes) + C(emotion) + C(paraphrase)",
        cluster="msg_id"):
    d = d.dropna(subset=[y])
    m = smf.ols(f"{y} ~ {x} + {controls}", d).fit(cov_type="cluster",
                                                   cov_kwds={"groups": pd.factorize(d[cluster])[0]})
    g = d[cluster].nunique()
    est, se = 100 * m.params[x], 100 * m.bse[x]
    q = stats.t.ppf(.975, g - 1)
    return dict(est=est, lo=est - q * se, hi=est + q * se, p=2 * stats.t.sf(abs(est / se), g - 1), clusters=g)


def emotion_effects(d, with_order=True):
    """Acceptance difference emotion - neutral message (pp), pooled over order; same controls."""
    out = {}
    for e in ("angry", "sad", "happy"):
        s = d[d.emotion.isin([e, "neutral"])].assign(x=lambda z: (z.emotion == e).astype(float))
        if s.x.nunique() == 2:
            out[e] = lpm(s, x="x", controls="C(offer) + C(stakes) + C(paraphrase)"
                         + (" + accept_first" if with_order else ""))["est"]
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows, by_emo, curves = [], [], {}
    for model, tag, bank in RUNS:
        d = load(model, tag, bank)
        if d is None:
            continue
        r = lpm(d)
        emo = emotion_effects(d)
        big = max(emo.items(), key=lambda kv: abs(kv[1])) if emo else (None, np.nan)
        row = dict(model=LABEL[model], run=tag, n=len(d),
                   accept_if_accept_first=d[d.accept_first == 1].accept.mean(),
                   accept_if_reject_first=d[d.accept_first == 0].accept.mean(),
                   order_effect_pp=r["est"], ci=f"[{r['lo']:+.1f}, {r['hi']:+.1f}]", p=r["p"],
                   largest_emotion_effect_pp=big[1], largest_emotion=big[0],
                   ratio=abs(r["est"]) / abs(big[1]) if big[0] and abs(big[1]) > 0.5 else np.nan)
        if "p_lp" in d and d.p_lp.notna().sum() > 100:
            rl = lpm(d, y="p_lp")
            row["order_effect_logprob_pp"] = rl["est"]
        rows.append(row)
        for e, g in d.groupby("emotion"):
            by_emo.append(dict(model=LABEL[model], run=tag, emotion=e,
                               accept_first=g[g.accept_first == 1].accept.mean(),
                               reject_first=g[g.accept_first == 0].accept.mean()))
        if tag == "main":
            curves[model] = d.groupby(["accept_first", "offer"]).accept.mean().unstack(0)

    t = pd.DataFrame(rows)
    t.to_csv(OUT / "order_bias.csv", index=False)
    e = pd.DataFrame(by_emo)
    e.to_csv(OUT / "order_bias_by_emotion.csv", index=False)

    # emotion effects (angry/sad - neutral) computed separately within each order, Qwen-7B main
    within = []
    for model in ("qwen25_7b", "qwen25_7b_q8", "qwen25_14b"):
        d = load(model, "main", "trials")
        if d is None:
            continue
        for f, g in d.groupby("accept_first"):
            for emo_name, v in emotion_effects(g, with_order=False).items():
                within.append(dict(model=LABEL[model], named_first="accept" if f == 1 else "reject",
                                   emotion=emo_name, effect_on_acceptance_pp=v))
    w = pd.DataFrame(within)

    ncol = 3
    nrow = int(np.ceil(len(curves) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(10, 3.3 * nrow), sharey=True, squeeze=False)
    axes = axes.ravel()
    for ax in axes[len(curves):]:
        ax.axis("off")
    for ax, (model, c) in zip(axes, curves.items()):
        ax.plot(c.index, 100 * c[1.0], "o-", color="#2a6f97", label='"accept" named first')
        ax.plot(c.index, 100 * c[0.0], "s-", color="#c0392b", label='"reject" named first')
        ax.set_title(LABEL[model], fontsize=10)
        ax.set_xlabel("offer (% of pie)")
        ax.set_ylim(-3, 103)
        ax.grid(alpha=.3)
    for ax in axes[::ncol]:
        ax.set_ylabel("% of offers accepted")
    axes[0].legend(fontsize=8, loc="center right")
    fig.suptitle("Ultimatum responder: acceptance by which option the prompt names first (main study, T = 1.0)",
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(OUT / "fig_order_bias.png", dpi=200)

    show = t.copy()
    for c in ("accept_if_accept_first", "accept_if_reject_first"):
        show[c] = (100 * show[c]).round(1)
    lines = ["# Option order in the ultimatum decision (P22; post hoc, exploratory)", "",
             "Order effect = P(accept | \"accept\" named first) − P(accept | \"reject\" named first), pp; linear probability "
             "model with offer, stakes, emotion and paraphrase as controls, SEs clustered by message, t with df = "
             "#clusters − 1. `largest_emotion_effect_pp` = the largest emotion − neutral acceptance difference in the same "
             "run (same model, order as a control); `ratio` = |order effect| / |that emotion effect|. "
             "`order_effect_logprob_pp` = the same model on the log-probability P(accept) where available.", "",
             md_table(show.round(3)), "",
             "## Emotion effects on acceptance, estimated separately within each order", "",
             "If order and emotion were independent, the two rows of each emotion would agree.", "",
             md_table(w.round(1)) if not w.empty else "No data.", "",
             "## Acceptance by condition and order (all runs)", "", md_table((e.set_index(["model", "run", "emotion"]) * 100)
                                                                           .round(0).reset_index()), "",
             "![order bias](fig_order_bias.png)", ""]
    (OUT / "order_bias.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[:8]))
    print(md_table(w.round(1)) if not w.empty else "")


if __name__ == "__main__":
    main()
