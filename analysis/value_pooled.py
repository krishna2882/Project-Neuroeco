"""Pooled valuation model across all 7 log-probability runs (exploratory, post hoc; P19).

Does a counterpart's emotion shift the model's P(accept) on average across runs? One linear mixed model on logit P(accept)
(S1, no-message trials excluded), pooling Llama-3.1-8B, Qwen2.5-3B/7B/14B and Qwen2.5-7B Q8 over the main and follow-up
messages:
  fixed:   C(emotion) * offer_c + stakes_c + C(run) * offer_c + C(run):C(paraphrase)
  random:  message (shared by runs that used the same messages), run x message, run x emotion
           (the emotion effect may differ between runs; its variance enters the SE of the pooled effect)
The pooled emotion effect is tested with t(df = #runs - 1 = 6), a deliberately conservative choice because runs are the
units the effect must generalise over; z is shown too. Sensitivity: Qwen runs only (5 runs, df = 4).
  python -m analysis.value_pooled   -> results/value_signal/pooled.md, pooled.csv
"""
import warnings

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

from analysis.common import holm, md_table
from analysis.value_signal import OUT, RUNS, load

TERM = "C(emotion, Treatment('neutral'))[T.{}]"


def stack(runs):
    parts = []
    for folder, model, label, msgs in runs:
        d = load(folder, model)
        d = d[d.emotion != "none"]
        parts.append(d.assign(run=f"{label} ({msgs})"))
    return pd.concat(parts, ignore_index=True)


def fit(d):
    d = d.copy()
    d["one"] = 1
    d["run_msg"] = d.run + "|" + d.msg_id
    d["run_emo"] = d.run + "|" + d.emotion
    f = ("logit_pa ~ C(emotion, Treatment('neutral')) * offer_c + stakes_c + C(run) * offer_c "
         "+ C(run):C(paraphrase)")
    vc = {"msg": "0 + C(msg_id)", "run_msg": "0 + C(run_msg)", "run_emo": "0 + C(run_emo)"}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        m = smf.mixedlm(f, d, groups=d.one, re_formula="0", vc_formula=vc).fit(reml=True, method="lbfgs")
    return m


def effects(m, n_runs, label):
    rows = []
    dfree = n_runs - 1
    q = stats.t.ppf(.975, dfree)
    for e in ["angry", "sad", "happy"]:
        for kind, k in (("value shift (logit at 30% offer)", TERM.format(e)),
                        ("gain shift (slope on offer)", f"{TERM.format(e)}:offer_c")):
            est, se = m.fe_params[k], m.bse_fe[k]
            rows.append(dict(sample=label, emotion=e, measure=kind, est=est, lo=est - q * se, hi=est + q * se,
                             p_t=2 * stats.t.sf(abs(est / se), dfree), p_z=2 * stats.norm.sf(abs(est / se)),
                             df=dfree, runs=n_runs))
    return rows


def main():
    all_runs = RUNS
    qwen = [r for r in RUNS if r[1].startswith("qwen")]
    rows, vcs = [], []
    for label, runs in (("all 7 runs", all_runs), ("Qwen runs only", qwen)):
        d = stack(runs)
        print(f"[{label}] n={len(d)}", flush=True)
        m = fit(d)
        rows += effects(m, len(runs), label)
        vcs.append(dict(sample=label, converged=m.converged,
                        **{f"SD {n}": np.sqrt(v) for n, v in zip(m.model.exog_vc.names, m.vcomp)}))
    res = pd.DataFrame(rows)
    res["p_holm"] = np.nan
    for s in res["sample"].unique():
        k = res["sample"] == s
        res.loc[k, "p_holm"] = holm(res.loc[k, "p_t"])
    res.to_csv(OUT / "pooled.csv", index=False)
    tab = res.assign(estimate=[f"{r.est:+.2f} [{r.lo:+.2f}, {r.hi:+.2f}]" for r in res.itertuples()])[
        ["sample", "emotion", "measure", "estimate", "p_t", "p_z", "p_holm"]].round(4)
    lines = ["# Pooled valuation model across runs (exploratory, post hoc; P19)", "",
             "Logit P(accept) from S1 log-probabilities, all runs stacked. Random effects: message, run × message, "
             "run × emotion; the emotion effect is the average over runs, and its SE includes how much it varies between "
             "runs. t with df = #runs − 1 (conservative); 95% CIs on the t scale; Holm over the 6 tests within each sample. "
             "Value shift > 0 = the same offer is more acceptable than after a neutral message.", "",
             md_table(tab), "", "## Random-effect SDs (logit scale)", "", md_table(pd.DataFrame(vcs).round(3)), ""]
    (OUT / "pooled.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
