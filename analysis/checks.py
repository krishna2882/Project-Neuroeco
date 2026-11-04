"""Manipulation and belief checks: emotion-recognition confusion matrices, perceived intensity,
perceived fairness, and perceived probability of rejection/retaliation by emotion."""
import matplotlib
import numpy as np
import pandas as pd

from analysis.common import EMO_ORDER, md_table
from config import EMOTIONS

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def run(ck, out, model_label):
    lines = [f"## Manipulation & belief checks ({model_label})", ""]
    msg = ck[~ck.is_baseline]
    cm = pd.crosstab(pd.Categorical(msg.emotion, EMOTIONS), pd.Categorical(msg.perceived_emotion, EMOTIONS),
                     rownames=["intended"], colnames=["perceived"], dropna=False)
    cm.to_csv(out / f"checks_confusion_{model_label}.csv")
    acc = (msg.emotion == msg.perceived_emotion).mean()
    per = msg.assign(hit=msg.emotion == msg.perceived_emotion).groupby("emotion").hit.mean()
    by_msg = msg.assign(hit=msg.emotion == msg.perceived_emotion).groupby(["emotion", "msg_id"]).hit.mean()
    by_msg.to_csv(out / f"checks_recognition_by_message_{model_label}.csv")
    lines += [f"Recognition accuracy: {acc:.1%} (n={len(msg)}); by emotion: "
              + ", ".join(f"{e} {per.get(e, np.nan):.0%}" for e in EMOTIONS), "",
              "### Confusion matrix (rows intended, columns perceived)", "", md_table(cm), ""]
    poorly = by_msg[by_msg < 0.75]
    if len(poorly):
        lines += ["Messages recognised < 75% of the time: "
                  + ", ".join(f"{m} ({v:.0%})" for (_, m), v in poorly.items()), ""]

    agg = {"p_retaliate": "mean"}
    if "intensity" in ck:
        agg["intensity"] = "mean"
    if "fairness" in ck:
        agg["fairness"] = "mean"
    tab = ck.groupby(["sub_exp", "emotion"]).agg(agg).round(2)
    tab = tab.reindex([(s, e) for s in tab.index.get_level_values(0).unique() for e in EMO_ORDER
                       if (s, e) in tab.index])
    tab.to_csv(out / f"checks_beliefs_{model_label}.csv")
    lines += ["### Mean intensity (1-7), fairness (1-7), P(reject/retaliate) (0-100) by emotion", "",
              md_table(tab), ""]

    fig, ax = plt.subplots(figsize=(4.2, 3.6))
    norm = cm.div(cm.sum(axis=1).replace(0, np.nan), axis=0).fillna(0)
    ax.imshow(norm.values, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(4), EMOTIONS, rotation=30)
    ax.set_yticks(range(4), EMOTIONS)
    for i in range(4):
        for j in range(4):
            ax.text(j, i, f"{norm.values[i, j]:.2f}", ha="center", va="center",
                    color="white" if norm.values[i, j] > 0.5 else "black", fontsize=8)
    ax.set_xlabel("perceived")
    ax.set_ylabel("intended")
    ax.set_title(f"Emotion recognition - {model_label}", fontsize=9)
    fig.tight_layout()
    fig.savefig(out / f"fig_checks_confusion_{model_label}.png", dpi=150)
    plt.close(fig)
    return "\n".join(lines), dict(confusion=cm, accuracy=acc)
