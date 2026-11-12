"""Equivalence tests (TOST) for every planned emotion-vs-neutral effect, and a pooled main + follow-up estimate (P14).

Inputs: results/main/message_re.csv and results/followup/message_re.csv (the stricter model with message as a random
factor, analysis/message_re.py). Effects are classified with two one-sided t-tests (same df as message_re) against a
smallest effect size of interest (SESOI). The SESOIs were chosen AFTER the results were known, so two are reported:
  shares:  +-5 pp (primary) and +-10 pp
  S1:      OR 1.5 (log-OR +-0.405, primary) and OR 2 (log-OR +-0.693)
Classification (alpha = .05; 90% CI for equivalence, 95% CI for difference):
  "equivalent to zero"  - 90% CI inside +-SESOI and not significant
  "small but real"      - significant and 90% CI inside +-SESOI
  "real"                - significant and not equivalent
"Significant" uses the study-wide BH-adjusted p from message_re (pooled: BH over the pooled tests).
  "inconclusive"        - neither
Pooled: fixed-effect inverse-variance combination of the main study (life-event messages) and the follow-up
(event-free messages) for the tests run in both (S1, S2, S3b; Llama, Qwen), with Cochran's Q for heterogeneity. This
is a secondary, not pre-registered analysis: it pools 10 messages per emotion, but across two message styles.

  python -m analysis.equivalence     -> results/main/equivalence.md, equivalence.csv, pooled.csv
"""
import numpy as np
import pandas as pd
from scipy import stats

from analysis.common import md_table
from config import RESULTS_DIR

BOUNDS = {"pp": (5.0, 10.0), "logOR": (np.log(1.5), np.log(2.0))}


def scale_of(test):
    return "logOR" if test.startswith("S1") else "pp"


def tost(est, se, df, bound):
    p_lo = stats.t.sf((est + bound) / se, df)     # H0: effect <= -bound
    p_hi = stats.t.cdf((est - bound) / se, df)    # H0: effect >= +bound
    return max(p_lo, p_hi)


def classify(est, se, df, bound, p_adj):
    sig = p_adj < .05  # multiplicity-adjusted (study-wide BH), not the raw p
    eq = tost(est, se, df, bound) < .05
    return {(False, True): "equivalent to zero", (True, True): "small but real",
            (True, False): "real", (False, False): "inconclusive"}[(sig, eq)]


def load(study):
    m = pd.read_csv(RESULTS_DIR / study / "message_re.csv")
    m = m[m.estimable == True].copy()  # noqa: E712  (Mistral S1 is at ceiling)
    m["study"] = study
    return m[["study", "model", "test", "emotion", "est_new", "se_new", "df", "p_t", "p_holm_study", "p_bh_study"]].rename(
        columns={"est_new": "est", "se_new": "se"})


def add_classes(d):
    d = d.copy()
    d["scale"] = d.test.map(scale_of)
    tc = stats.t.ppf(.95, d.df)
    d["ci90_lo"], d["ci90_hi"] = d.est - tc * d.se, d.est + tc * d.se
    for i, name in enumerate(["primary", "lenient"]):
        b = d.scale.map(lambda s: BOUNDS[s][i])
        d[f"bound_{name}"] = b
        d[f"p_tost_{name}"] = [tost(e, s, f, bb) for e, s, f, bb in zip(d.est, d.se, d.df, b)]
        d[f"class_{name}"] = [classify(e, s, f, bb, pa) for e, s, f, bb, pa in zip(d.est, d.se, d.df, b, d.p_bh_study)]
    return d


def pooled(main, fu):
    keys = ["model", "test", "emotion"]
    j = main.merge(fu, on=keys, suffixes=("_main", "_fu"))
    rows = []
    for r in j.itertuples():
        w = np.array([1 / r.se_main ** 2, 1 / r.se_fu ** 2])
        e = np.array([r.est_main, r.est_fu])
        est = (w * e).sum() / w.sum()
        se = np.sqrt(1 / w.sum())
        q = float((w * (e - est) ** 2).sum())
        rows.append(dict(model=r.model, test=r.test, emotion=r.emotion, est_main=r.est_main, est_fu=r.est_fu,
                         est=est, se=se, df=int(r.df_main + r.df_fu), p_t=2 * stats.t.sf(abs(est / se), r.df_main + r.df_fu),
                         Q=q, p_het=stats.chi2.sf(q, 1)))
    p = pd.DataFrame(rows)
    from analysis.common import holm
    p["p_holm"] = holm(p.p_t)
    from analysis.forest import bh
    p["p_bh_study"] = bh(p.p_t)
    return add_classes(p)


def fmt(e, lo, hi, scale):
    return f"{e:+.2f} [{lo:+.2f}, {hi:+.2f}]" if scale == "logOR" else f"{e:+.1f} [{lo:+.1f}, {hi:+.1f}]"


def main():
    main_, fu = load("main"), load("followup")
    allx = add_classes(pd.concat([main_, fu], ignore_index=True))
    pool = pooled(main_, fu)
    out = RESULTS_DIR / "main"
    allx.to_csv(out / "equivalence.csv", index=False)
    pool.to_csv(out / "pooled.csv", index=False)

    counts = (allx.groupby(["study", "model"]).class_primary.value_counts().unstack(fill_value=0)
              .reindex(columns=["equivalent to zero", "small but real", "real", "inconclusive"], fill_value=0))
    counts_len = (allx.groupby(["study", "model"]).class_lenient.value_counts().unstack(fill_value=0)
                  .reindex(columns=["equivalent to zero", "small but real", "real", "inconclusive"], fill_value=0))
    tab = allx.assign(**{"estimate [90% CI]": [fmt(*v) for v in allx[["est", "ci90_lo", "ci90_hi", "scale"]].values]})
    tab = tab[["study", "model", "test", "emotion", "estimate [90% CI]", "p_t", "p_tost_primary", "class_primary",
               "class_lenient"]]
    ptab = pool.assign(**{"main": pool.est_main.round(2), "follow-up": pool.est_fu.round(2),
                          "pooled [95% CI]": [fmt(e, e - 1.96 * s, e + 1.96 * s, sc) for e, s, sc in
                                              pool[["est", "se", "scale"]].values]})
    ptab = ptab[["model", "test", "emotion", "main", "follow-up", "pooled [95% CI]", "p_t", "p_holm", "p_bh_study", "p_het",
                 "class_primary"]]
    lines = [
        "# Equivalence tests and pooled estimates (P14; Llama, Qwen, Mistral)", "",
        "Built on the stricter model with message as a random factor (`message_re.md`). Smallest effect of interest "
        "(SESOI), chosen **after** seeing the results, so two are shown: primary ±5 pp / OR 1.5, lenient ±10 pp / OR 2. "
        "Classes: *equivalent to zero* (90% CI inside ±SESOI, not significant), *small but real* (significant, inside "
        "±SESOI), *real* (significant, not equivalent), *inconclusive*. Significant = study-wide FDR (BH) < .05. Script: `analysis/equivalence.py`.", "",
        "## How many emotion effects fall in each class (primary SESOI: ±5 pp / OR 1.5)", "", md_table(counts), "",
        "## Same with the lenient SESOI (±10 pp / OR 2)", "", md_table(counts_len), "",
        "## Pooled main + follow-up (10 messages per emotion; secondary, not pre-registered)", "",
        "Fixed-effect inverse-variance pooling; `p_het` tests whether the two studies disagree (life-event vs "
        "event-free messages); a small `p_het` means pooling hides a real difference. Holm over the pooled tests.", "",
        md_table(ptab, floatfmt=3), "",
        "## Every test", "", md_table(tab, floatfmt=3), ""]
    (out / "equivalence.md").write_text("\n".join(lines))
    print("\n".join(lines[:16]))
    print(md_table(ptab, floatfmt=3))


if __name__ == "__main__":
    main()
