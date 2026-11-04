"""Temperature robustness (S1): T = 1.0 (tag main) vs T = 0.7 (tag temp07), per model.

Tests whether the emotion effects on rejection depend on sampling temperature:
  reject ~ emotion * temp07 + offer_c * stakes_c + (1 | variant), joint Wald test on emotion x temp07.
"""
import numpy as np
import pandas as pd
import patsy

from analysis.common import EMO_ORDER, md_table, tidy_trials
from analysis.glmm import fit_glmm


def run(raw_dir=None, tag_main="main", tag_rob="temp07"):
    kw = {} if raw_dir is None else {"raw_dir": raw_dir}
    try:
        rob = tidy_trials(tag_rob, **kw)
    except FileNotFoundError:
        return "## Temperature robustness\n\nNo temp07 data.\n"
    main = tidy_trials(tag_main, **kw)
    lines = ["## Temperature robustness (S1): T=1.0 vs T=0.7", ""]
    for m in sorted(rob.model_key.unique()):
        a = main[(main.model_key == m) & (main.sub_exp == "S1") & ~main.extension].assign(temp07=0.0)
        b = rob[(rob.model_key == m) & (rob.sub_exp == "S1") & ~rob.extension].assign(temp07=1.0)
        if b.empty or a.empty:
            continue
        d = pd.concat([a, b])
        d["emotion"] = d.emotion.astype(str)
        d["offer_c"] = d.offer_share - 0.3
        tab = d.pivot_table(index="emotion", columns="temp07", values="accept").reindex(
            [e for e in EMO_ORDER if e in set(d.emotion)])
        tab.columns = ["P(accept) T=1.0", "P(accept) T=0.7"]
        lines += [f"### {m}", "", md_table(tab.round(3)), ""]
        f = "C(emotion, Treatment('neutral')) * temp07 + offer_c * stakes_c"
        X = patsy.dmatrix(f, d, return_type="dataframe")
        r = fit_glmm(X, d.reject.values, d.variant_id.values)
        terms = [c for c in X.columns if c.startswith("C(emotion") and "temp07" in c]
        chi, k, p = r.wald(terms)
        bt = r.params["temp07"]
        lines += [f"- Main effect of T=0.7 on rejection (logit): {bt:+.3f} (se {r.bse['temp07']:.3f})",
                  f"- Emotion x Temperature: chi2({k})={chi:.2f}, p={p:.4g} "
                  f"({'emotion effects differ by temperature' if p < .05 else 'no evidence that emotion effects depend on temperature'})",
                  f"- Decision agreement is not expected (different sampling); n = {len(a)} vs {len(b)}", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    print(run())
