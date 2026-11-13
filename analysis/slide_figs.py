"""Figures for the presentation (blue/white theme). Every number is read from the results files, never typed in.
  python -m analysis.slide_figs   -> results/slides/*.png
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

from config import RESULTS_DIR  # noqa: E402

OUT = RESULTS_DIR / "slides"
NAVY, BLUE, MID, SKY, PALE, INK, MUTED, ANGER = "#0B2545", "#1F5FBF", "#5B8FD9", "#A9C7EE", "#EEF4FB", "#13233F", "#5A6B85", "#D9622B"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 15, "axes.edgecolor": "#B8C6DA", "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": INK, "axes.spines.top": False, "axes.spines.right": False})


def anger_trust():
    def get(folder, model):
        m = pd.read_csv(RESULTS_DIR / folder / "message_re.csv")
        r = m[(m.model == model) & (m.test == "S3b sent (pp)") & (m.emotion == "angry")].iloc[0]
        return r.est_new, r.lo_new, r.hi_new

    pooled = pd.read_csv(RESULTS_DIR / "main" / "pooled.csv")

    def pool(model):
        r = pooled[(pooled.model == model) & (pooled.test == "S3b sent (pp)") & (pooled.emotion == "angry")].iloc[0]
        q = stats.norm.ppf(.975)  # same interval as results/main/equivalence.md (pooled section)
        return r.est, r.est - q * r.se, r.est + q * r.se

    rows = [("Qwen2.5-7B · main", *get("main", "qwen25_7b"), "e"),
            ("Qwen2.5-7B · follow-up (pre-reg. F2)", *get("followup", "qwen25_7b"), "c"),
            ("Qwen2.5-7B · pooled", *pool("qwen25_7b"), "p"),
            ("Qwen2.5-7B 8-bit (pre-reg. X3)", *get("ext2", "qwen25_7b_q8"), "c"),
            ("Qwen2.5-3B (pre-reg. X2)", *get("ext2", "qwen25_3b"), "c"),
            ("Qwen2.5-14B (pre-reg. X1)", *get("ext2", "qwen25_14b"), "c"),
            ("Llama-3.1-8B · main", *get("main", "llama31_8b"), "e"),
            ("Llama-3.1-8B · follow-up", *get("followup", "llama31_8b"), "e"),
            ("Llama-3.1-8B · pooled", *pool("llama31_8b"), "p"),
            ("Mistral Large 4 · main", *get("main", "mistral"), "e")]
    fig, ax = plt.subplots(figsize=(13, 7.2))
    for i, (lab, e, lo, hi, kind) in enumerate(rows):
        col = NAVY if kind == "c" else (BLUE if kind == "p" else MID)
        ax.plot([lo, hi], [i, i], color=col, lw=3, solid_capstyle="round")
        ax.plot(e, i, marker="D" if kind == "p" else "o", ms=13 if kind == "p" else 11, color=col, mec="white", mew=2)
        ax.text(12, i, f"{e:+.1f} [{lo:+.1f}, {hi:+.1f}]", va="center", fontsize=14, color=INK)
    ax.axvline(0, color="#8FA3BF", lw=1.5, ls="--")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=14)
    ax.invert_yaxis()
    ax.set_xlim(-36, 34)
    ax.set_xticks([-30, -20, -10, 0, 10])
    ax.set_xlabel("Change in share sent to an angry vs neutral partner (percentage points, 95% CI)", fontsize=14)
    ax.grid(axis="x", color="#E3EAF4")
    ax.spines["bottom"].set_bounds(-36, 10)
    fig.tight_layout()
    fig.savefig(OUT / "anger_trust.png", dpi=170, facecolor="white")
    plt.close(fig)
    return rows


def value_curve():
    t = pd.read_csv(RESULTS_DIR / "main" / "tidy_trials.csv", low_memory=False)
    d = t[(t.sub_exp == "S1") & (t.model_key == "qwen25_7b") & t.p_accept_lp.notna()]
    c = d.groupby(["emotion", "offer_share"]).p_accept_lp.mean().unstack(0)
    fig, ax = plt.subplots(figsize=(10, 6.4))
    spec = {"neutral": (MID, "o", "neutral"), "sad": (NAVY, "^", "sad"), "angry": (ANGER, "s", "angry")}
    for e, (col, mk, lab) in spec.items():
        y = c[e]
        ax.plot(100 * y.index, y.values, color=col, lw=3, marker=mk, ms=10, mec="white", mew=1.5)
        ax.text(100 * y.index[-1] + 1.2, y.values[-1], lab, color=col, fontsize=16, va="center", fontweight="bold")
    ax.axhline(.5, color="#B8C6DA", lw=1.2)
    ax.set_xlim(2, 58)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Offer (% of the pie)", fontsize=15)
    ax.set_ylabel("Model's P(accept), from log-probabilities", fontsize=15)
    ax.grid(axis="y", color="#E3EAF4")
    fig.tight_layout()
    fig.savefig(OUT / "value_curve_qwen7b.png", dpi=170, facecolor="white")
    plt.close(fig)
    return c


def wording():
    t = pd.read_csv(RESULTS_DIR / "main" / "tidy_trials.csv", low_memory=False)
    d = t[(t.sub_exp == "S1") & (t.model_key == "llama31_8b") & ~t.is_baseline.astype(bool) & (t.emotion != "none")]
    by_para = d.groupby("paraphrase").accept.mean() * 100
    by_emo = d.groupby("emotion").accept.mean().reindex(["neutral", "angry", "sad", "happy"]) * 100
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5.6), sharey=True)
    a1.bar([f"Wording {i + 1}" for i in by_para.index], by_para.values, color=NAVY, width=.62)
    a2.bar([e.capitalize() for e in by_emo.index], by_emo.values, color=SKY, width=.62)
    for ax, s, title in ((a1, by_para, "Same game, 4 wordings of the instructions"),
                         (a2, by_emo, "Same game, 4 emotions of the partner")):
        for i, v in enumerate(s.values):
            ax.text(i, v + 1.5, f"{v:.0f}%", ha="center", fontsize=15, color=INK)
        ax.set_title(title, fontsize=15, color=INK, loc="left")
        ax.set_ylim(0, 100)
        ax.grid(axis="y", color="#E3EAF4")
        ax.set_axisbelow(True)
    a1.set_ylabel("Llama-3.1-8B: offers accepted", fontsize=14)
    fig.tight_layout()
    fig.savefig(OUT / "wording_llama.png", dpi=170, facecolor="white")
    plt.close(fig)
    return by_para, by_emo


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for r in anger_trust():
        print(f"{r[0]:40s} {r[1]:+6.1f} [{r[2]:+6.1f}, {r[3]:+6.1f}]")
    print(value_curve().round(3).to_string())
    p, e = wording()
    print(p.round(1).to_dict(), e.round(1).to_dict())


if __name__ == "__main__":
    main()
