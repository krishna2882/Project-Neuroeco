"""Exploratory: does the anger -> trust (S3b) effect grow with how threatening raters found each anger message?
Uses all 10 anger messages the models saw (main A1-A7, follow-up FA2-FA7) and the human threat ratings.
  python -m analysis.threat   -> results/threat/threat.md, threat_per_message.csv
"""
import warnings

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from analysis.common import md_table
from config import RESULTS_DIR, STIM_DIR

SOURCES = [("main", "main", ["llama31_8b", "qwen25_7b", "mistral"]),
           ("ext2", "main", ["qwen25_3b", "qwen25_14b", "qwen25_7b_q8"]),
           ("followup", "followup", ["llama31_8b", "qwen25_7b"])]


def load():
    rows = []
    for folder, study, models in SOURCES:
        t = pd.read_csv(RESULTS_DIR / folder / "tidy_trials.csv", low_memory=False)
        t = t[(t.sub_exp == "S3b") & t.model_key.isin(models) & t.emotion.isin(["angry", "neutral"])]
        rows.append(t.assign(study=study))
    d = pd.concat(rows, ignore_index=True)
    d["y"] = 100 * d["share"]
    return d


def main():
    r = pd.read_csv(STIM_DIR / "rating" / "human_ratings.csv")
    rat = r.groupby("msg_id").agg(threat=("threat_or_promise", "mean"), recog=("perceived_emotion",
                                  lambda s: np.nan)).drop(columns="recog")
    d = load()
    d["ms"] = d.model_key + "|" + d.study
    neut = d[d.emotion == "neutral"].groupby("ms").y.mean()
    a = d[d.emotion == "angry"]
    per = a.groupby(["ms", "model_key", "study", "msg_id"]).y.agg(["mean", "count"]).reset_index()
    per["effect_pp"] = per["mean"] - per.ms.map(neut)
    per = per.join(rat, on="msg_id")
    per.to_csv(RESULTS_DIR / "threat" / "threat_per_message.csv", index=False)

    # trial-level LMM: share ~ model-study x angry + angry:threat, random intercept per message
    th = rat.threat.to_dict()
    d["angry"] = (d.emotion == "angry").astype(int)
    d["threat_c"] = d.msg_id.map(th).fillna(0) - per.drop_duplicates("msg_id").threat.mean()
    d["at"] = d.angry * d.threat_c
    fits = []
    for label, sub in [("all models", d), ("without Mistral", d[d.model_key != "mistral"]),
                       ("Qwen 7B (4-bit) only", d[d.model_key == "qwen25_7b"])]:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            m = smf.mixedlm("y ~ C(ms) * angry + at + C(ms):at + stakes_c" if False else
                            "y ~ C(ms) * angry + at + stakes_c", sub, groups=sub.msg_id).fit(reml=True)
        b, se = m.params["at"], m.bse["at"]
        fits.append(dict(sample=label, n_trials=len(sub), n_anger_msgs=sub[sub.angry == 1].msg_id.nunique(),
                         slope_pp_per_10pct_threat=b / 10, lo=(b - 1.96 * se) / 10, hi=(b + 1.96 * se) / 10,
                         p=m.pvalues["at"]))
    fits = pd.DataFrame(fits)
    # simple message-level view: mean effect across models per message
    msg = per.groupby(["msg_id", "study"]).agg(threat=("threat", "first"), effect_pp=("effect_pp", "mean"),
                                               n_models=("ms", "nunique")).reset_index().sort_values("threat").reset_index(drop=True)
    rho = msg[["threat", "effect_pp"]].corr(method="spearman").iloc[0, 1]
    wide = per.pivot_table(index="msg_id", columns="ms", values="effect_pp").round(1)
    lines = ["# Is the anger effect on trust driven by perceived threat? (exploratory, post hoc)", "",
             "Threat = share of the 9 human raters who read the message as a threat or promise. Effect = share sent "
             "after this angry message minus the share sent after neutral messages, same model and study (pp). "
             "Slope from a trial-level mixed model: share ~ model-study x angry + angry x threat + stakes, random "
             "intercept per message; reported per 10 percentage points of threat.", "",
             "## Slope of the anger effect on threat", "", md_table(fits, floatfmt=3), "",
             f"Message level (mean effect over models): Spearman rho = {rho:.2f} over {len(msg)} messages.", "",
             md_table(msg, floatfmt=2), "", "## Effect per message and model (pp)", "",
             md_table(wide.reset_index()), ""]
    (RESULTS_DIR / "threat" / "threat.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
