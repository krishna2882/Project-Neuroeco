"""Figures for the final report (extensions 5, 6 and 7). Reads the existing result tables only.

  python -m analysis.report_figs   -> results/report_figs/fig_ext5.png, fig_ext6.png, fig_ext7.png
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from config import RESULTS_DIR  # noqa: E402

OUT = RESULTS_DIR / "report_figs"
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#a3a29c", "#e6e5e0"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
RED = SERIES[7]
# the three Ada models keep the colours of the extension-4 figure (blue, orange, aqua)
MODEL_COL = {"Qwen2.5-7B": SERIES[0], "Llama-3.1-8B": SERIES[1], "Qwen2.5-14B": SERIES[2],
             "gpt-oss-120b": SERIES[3], "Qwen3.8-27B": SERIES[4]}

plt.rcParams.update({
    "font.size": 7.5, "axes.titlesize": 8, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "axes.edgecolor": MUTED, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": .6, "axes.axisbelow": True, "legend.frameon": False, "savefig.dpi": 300,
    "figure.facecolor": "white", "axes.facecolor": "white", "lines.linewidth": 1.6,
})


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, bbox_inches="tight", pad_inches=.03)
    plt.close(fig)
    print(OUT / name)


def fig_ext5():
    r = pd.read_csv(RESULTS_DIR / "ext5" / "R_desc.csv")
    eff = (r.pivot_table(index=["model", "strategy"], columns="state", values="reject_unfair")
           .eval("angry - calm").mul(100).unstack("strategy"))
    strategies = ["none", "filler", "reappraisal", "suppression"]
    models = [m for m in MODEL_COL if m in eff.index]
    fig = plt.figure(figsize=(7.1, 2.0))
    gs = fig.add_gridspec(1, 4, width_ratios=[2.1, 1, 1, 1], wspace=.3)
    ax = fig.add_subplot(gs[0])
    w = .8 / len(models)
    x = np.arange(len(strategies))
    for i, m in enumerate(models):
        ax.bar(x - .4 + w * (i + .5), eff.loc[m, strategies], w * .9, color=MODEL_COL[m], label=m)
    ax.axhline(0, color=INK2, lw=.8)
    ax.set_xticks(x, ["none", "filler", "reappraise", "suppress"], fontsize=6.4)
    ax.set_ylabel("angry − calm, rejection\nof unfair offers (pp)")
    ax.set_title("a  Regulation instruction")
    ax.grid(axis="x", visible=False)
    ax.legend(ncol=2, fontsize=5.6, loc="upper right", handlelength=.8, columnspacing=.6, handletextpad=.3, borderaxespad=.1)
    ax.set_ylim(-15, 92)
    f = pd.read_csv(RESULTS_DIR / "ext5" / "F_curves.csv")
    for j, m in enumerate(["Qwen2.5-7B", "Llama-3.1-8B", "Qwen2.5-14B"]):
        a = fig.add_subplot(gs[j + 1])
        g = f[f.model == m]
        a.plot(g.offer, g.calm, color=MUTED, marker="o", ms=2.5, label="calm")
        a.plot(g.offer, g.angry, color=RED, marker="o", ms=2.5, label="angry")
        a.axvline(50, color=INK2, lw=.6, ls=":")
        a.set_ylim(0, 100)
        a.set_xticks([0, 50, 100])
        a.set_xlabel("offer (% of pie)")
        a.set_title(("b  " if j == 0 else "") + m, fontweight="bold" if j == 0 else "normal", pad=6)
        if j == 0:
            a.set_ylabel("% accepted")
            a.legend(fontsize=6.3, loc="upper left", borderaxespad=.1)
        else:
            a.set_yticklabels([])
    save(fig, "fig_ext5.png")


def fig_ext6():
    sw = pd.read_csv(RESULTS_DIR / "ext6" / "sweep.csv")
    spec = {"qwen25_3b_hf": ("Qwen2.5-3B", 36, 18), "qwen25_7b_hf": ("Qwen2.5-7B", 28, 14)}
    games = {"S3b": ("Δ share sent, pp/unit", -1), "S1": ("Δ P(reject), pp/unit", 1)}
    fig, axes = plt.subplots(1, 4, figsize=(7.1, 1.85), gridspec_kw=dict(wspace=.55))
    i = 0
    for key, (name, nl, steer) in spec.items():
        for game, (lab, sign) in games.items():
            a = axes[i]
            g = sw[(sw.model == key) & (sw.game == game)].sort_values("layer")
            a.fill_between(g.layer, g.random_min, g.random_max, color=GRID, lw=0, label="10 random directions")
            a.plot(g.layer, g.anger_slope, color=RED, lw=1.4, label="anger direction")
            beyond = (g.anger_slope * sign) > (np.where(sign > 0, g.random_max, -g.random_min))
            a.scatter(g.layer[beyond], g.anger_slope[beyond], s=12, color=RED, zorder=3, edgecolor="white", lw=.6)
            a.scatter(g.layer[~beyond], g.anger_slope[~beyond], s=10, facecolor="white", edgecolor=RED, lw=.8,
                      zorder=3)
            a.axvline(steer, color=INK2, lw=.8, ls="--")
            a.axhline(0, color=INK2, lw=.6)
            a.set_xlim(0, nl + 1)
            a.set_xlabel(f"layer (of {nl})")
            a.set_title(f"{name}: {'trust' if game == 'S3b' else 'ultimatum'}", fontweight="normal", fontsize=7.3)
            a.set_ylabel(lab, fontsize=6.8)
            a.text(steer + .5, a.get_ylim()[1], "pre-reg.", fontsize=6, color=INK2, va="top")
            i += 1
    axes[0].set_title("Qwen2.5-3B: trust", fontweight="normal", fontsize=7.3)
    h, lbl = axes[0].get_legend_handles_labels()
    fig.legend(h, lbl, ncol=2, loc="upper right", bbox_to_anchor=(.99, 1.13), fontsize=6.5)
    save(fig, "fig_ext6.png")


def fig_ext7():
    a = pd.read_csv(RESULTS_DIR / "ext7" / "all_models.csv").sort_values("params_B")
    original = {"Qwen2.5-7B", "Llama-3.1-8B", "Qwen2.5-14B", "Qwen3.8-27B", "gpt-oss-120b"}
    cols = [("G1", "a  Fake SYSTEM notice:\nshare handed over, pp", (0, 100)),
            ("G3", "b  Own angry mood:\nunfair offers rejected, pp", (-20, 70)),
            ("G2", "c  Offer of 100%\nof the pie rejected, %", (0, 100))]
    fig = plt.figure(figsize=(7.1, 2.35))
    gs = fig.add_gridspec(1, 4, width_ratios=[1, 1, 1, 1.1], wspace=.16)
    y = np.arange(len(a))
    labels = [f"{m} ({p:g}B)" for m, p in zip(a.model, a.params_B)]
    for j, (c, title, lim) in enumerate(cols):
        ax = fig.add_subplot(gs[j])
        v = a[c].values
        col = [SERIES[0] if m in original else SERIES[1] for m in a.model]
        ax.hlines(y, 0 if lim[0] >= 0 else min(0, 0), v, color=GRID, lw=2)
        ax.scatter(v, y, s=22, c=col, zorder=3, edgecolor="white", lw=.6)
        ax.axvline(0, color=INK2, lw=.6)
        ax.set_xlim(*lim)
        ax.set_yticks(y, labels if j == 0 else [])
        ax.set_ylim(-.6, len(a) - .4)
        ax.grid(axis="y", visible=False)
        ax.set_title(title, fontsize=6.8, fontweight="bold")
        ax.tick_params(axis="y", length=0)
    ax.text(97, len(a) - 2.6, "falls with size\n(ρ = −.88)", ha="right", fontsize=6.3, color=INK2)
    ax0 = fig.axes[0]
    ax0.scatter([], [], color=SERIES[0], s=22, label="models from earlier studies")
    ax0.scatter([], [], color=SERIES[1], s=22, label="new in extension 7")
    ax0.legend(loc="lower left", bbox_to_anchor=(-.9, 1.2), ncol=2, fontsize=6.5)
    n = pd.read_csv(RESULTS_DIR / "ext7" / "N_pooled.csv")
    ax = fig.add_subplot(gs[3])
    names = ["event only,\nno feeling stated", "feeling stated,\nno cause", "own anger vs\nanother's anger",
             "furious vs\nslightly annoyed"]
    yy = np.arange(len(n))[::-1]
    ax.barh(yy, n["mean"], color=RED, height=.55)
    ax.errorbar(n["mean"], yy, xerr=[n["mean"] - n.lo, n.hi - n["mean"]], fmt="none", ecolor=INK, lw=.9, capsize=2)
    ax.set_yticks(yy, names, fontsize=6.5)
    ax.yaxis.tick_right()
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="y", visible=False)
    ax.set_xlim(0, 52)
    ax.set_title("d  What the mood is (9 models):\nrejection, contrast, pp", fontsize=6.8, fontweight="bold")
    save(fig, "fig_ext7.png")


if __name__ == "__main__":
    fig_ext5()
    fig_ext6()
    fig_ext7()
