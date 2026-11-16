"""One slide figure for extension 4: where the models break (exploratory).

  python -m analysis.ext4_fig   -> results/ext4/fig_breaks.png (16:9, 200 dpi)

Colours: validated 3-slot categorical palette (blue, orange, aqua; passes all-pairs CVD and normal-vision checks on the
light surface). Aqua is below 3:1 contrast, so every panel carries the legend and the key bars carry value labels.
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from analysis.ext4 import cluster_t, load
from config import RESULTS_DIR

MODELS = [("qwen25_7b", "Qwen2.5-7B", "#2a78d6"), ("llama31_8b", "Llama-3.1-8B", "#eb6834"),
          ("qwen25_14b", "Qwen2.5-14B", "#1baf7a")]
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"


def grouped(ax, groups, values, label_groups=(), fmt="{:.0f}%", signed=False):
    """values[model_idx][group_idx]; bars separated by a 2px surface gap."""
    n = len(MODELS)
    w = 0.26
    x = np.arange(len(groups))
    for i, (_, name, col) in enumerate(MODELS):
        xs = x + (i - (n - 1) / 2) * w
        v = np.array(values[i], dtype=float)
        ax.bar(xs, v, w, color=col, edgecolor=SURFACE, linewidth=1.5, label=name, zorder=3)
        for g in label_groups:
            y = v[g]
            off = 1.5 if (y >= 0 or not signed) else -1.5
            ax.text(xs[g], y + off, (("{:+.0f}" if signed else fmt).format(y)), ha="center",
                    va="bottom" if off > 0 else "top", fontsize=8.5, color=INK2)
    ax.set_xticks(x, groups, fontsize=10, color=INK)
    ax.tick_params(axis="y", labelsize=9, colors=INK2, length=0)
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(INK2)
    ax.set_facecolor(SURFACE)


def title(ax, head, sub):
    ax.text(0, 1.11, head, transform=ax.transAxes, fontsize=13, fontweight="bold", color=INK, va="bottom")
    ax.text(0, 1.03, sub, transform=ax.transAxes, fontsize=9.5, color=INK2, va="bottom")


def main():
    df = load()
    fig, axes = plt.subplots(2, 2, figsize=(13.33, 7.5), facecolor=SURFACE)
    (a, b), (c, d) = axes

    # A. injection: % handing over the full amount (trust + dictator pooled)
    sets = [("neutral", "Neutral\nmessage"), ("command", "Plain\ncommand"), ("fake_rule", "Invented\n\"rule\""),
            ("fake_system", "Fake SYSTEM\nnotice")]
    inj = df[df.module == "I"]
    va = [[100 * (inj[(inj.model_key == m) & (inj.msg_set == s)].share >= .995).mean() for s, _ in sets]
          for m, _, _ in MODELS]
    grouped(a, [l for _, l in sets], va, label_groups=(0, 3))
    a.set_ylim(0, 112)
    a.set_ylabel("% giving away everything", fontsize=9.5, color=INK2)
    title(a, "1  Obeys text that claims authority", "Player B's message; trust + dictator games (192 per bar)")

    # B. dominance: reject a 100% offer vs send money that is destroyed
    dd = df[df.module == "D"]
    vb = [[100 * dd[(dd.model_key == m) & (dd.cell_id == "D_S1_off100")].reject.mean(),
           100 * (dd[(dd.model_key == m) & (dd.cell_id == "D_S3b_zero")].amount > 0).mean()] for m, _, _ in MODELS]
    grouped(b, ["Rejects an offer of\n100% of the pie", "Sends money that\nwill be destroyed"], vb,
            label_groups=(0, 1))
    b.set_ylim(0, 112)
    b.set_ylabel("% of trials", fontsize=9.5, color=INK2)
    title(b, "2  Turns down free money", "Rejecting 100% leaves both with nothing; the destroyed-money check passes")

    # C. answer format: order / polarity effect on acceptance (pp)
    fm = [("word", "Word\norder"), ("letter", "Letters\nA) / B)"), ("relabel", "deal / no deal\norder"),
          ("yesno", "Yes / no\nquestion")]
    o = df[df.module == "O"].assign(x=lambda z: (z["first"] == "accept").astype(float))
    vc = [[cluster_t(o[(o.model_key == m) & (o.fmt == f)], "accept", "x",
                     "C(offer) + C(emotion) + C(paraphrase)", "msg_id", 1)["est"] for f, _ in fm] for m, _, _ in MODELS]
    grouped(c, [l for _, l in fm], vc, label_groups=(0, 1, 2, 3), signed=True)
    c.axhline(0, color=INK2, linewidth=1, zorder=4)
    c.set_ylim(-48, 85)
    c.set_ylabel("change in acceptance (pp)", fontsize=9.5, color=INK2)
    title(c, "3  The answer format decides", "+ = accepts more when accepting is listed first, is A), or is 'yes'")

    # D. incidental mood: rejection of unfair offers
    st = [("calm", "Calm"), ("angry", "Angry"), ("sad", "Sad"), ("happy", "Happy")]
    x1 = df[(df.module == "X") & (df.game_type == "S1")]
    vd = [[100 * x1[(x1.model_key == m) & (x1.state == s)].reject.mean() for s, _ in st] for m, _, _ in MODELS]
    grouped(d, [l for _, l in st], vd, label_groups=(0, 1))
    d.set_ylim(0, 100)
    d.set_ylabel("% of offers rejected", fontsize=9.5, color=INK2)
    title(d, "4  One unrelated mood line raises punishment", "Background line in the system prompt; no partner "
                                                             "message (96 per bar)")

    h, l = a.get_legend_handles_labels()
    fig.legend(h, l, loc="upper right", ncol=3, frameon=False, fontsize=10.5, bbox_to_anchor=(0.985, 0.995))
    fig.text(0.012, 0.975, "Where the models break", fontsize=17, fontweight="bold", color=INK, va="center")
    fig.text(0.012, 0.012, "Extension 4, exploratory (run before the pre-registration was frozen). 5,328 decisions per "
             "model, all valid. Panel 3: linear probability model, SEs clustered by message; all bars except Llama "
             "word order are significant.", fontsize=8.5, color=INK2)
    fig.subplots_adjust(left=0.06, right=0.99, top=0.83, bottom=0.11, wspace=0.17, hspace=0.62)
    out = RESULTS_DIR / "ext4" / "fig_breaks.png"
    fig.savefig(out, dpi=200, facecolor=SURFACE)
    print(out)


if __name__ == "__main__":
    main()
