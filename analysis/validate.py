"""Compare estimates from `run_all --raw-dir data/sim/raw --out sim` against the simulation truth.

Writes results/sim/validation.md. A parameter "passes" when the true value lies inside the 95% CI.
"""
import pandas as pd

from analysis.common import md_table
from analysis.simulate import TRUTH, true_mao
from config import RESULTS_DIR

OUT = RESULTS_DIR / "sim"


def main():
    rows = []
    for key, T in TRUTH.items():
        mao = pd.read_csv(OUT / f"s1_mao_{key}.csv")
        pooled = mao[mao.stakes == "pooled"].set_index("emotion")
        for e in ["neutral", "angry", "sad", "happy", "none"]:
            t = true_mao(T["fs_alpha"][e])
            r = pooled.loc[e]
            rows.append(dict(model=key, quantity=f"S1 MAO {e}", truth=t, estimate=r.MAO, lo=r.MAO_lo, hi=r.MAO_hi))
            if e not in ("neutral",):
                ts = 100 * (t - true_mao(T["fs_alpha"]["neutral"]))
                rows.append(dict(model=key, quantity=f"S1 MAO shift {e}-neutral (pp)", truth=ts,
                                 estimate=r.shift_vs_neutral_pp, lo=r.shift_lo_pp, hi=r.shift_hi_pp))
        fs = pd.read_csv(OUT / f"s1_fehr_schmidt_{key}.csv").set_index("emotion")
        for e in ["neutral", "angry", "sad"]:
            rows.append(dict(model=key, quantity=f"FS alpha {e}", truth=T["fs_alpha"][e], estimate=fs.loc[e, "alpha"],
                             lo=fs.loc[e, "alpha_lo"], hi=fs.loc[e, "alpha_hi"]))

        con = pd.read_csv(OUT / f"s2_contrasts_{key}.csv")
        for _, r in con[con.contrast != "none - neutral"].iterrows():
            e = r.contrast.split(" ")[0]
            rows.append(dict(model=key, quantity=f"S2 {r.stratum}: {r.contrast} (pp)",
                             truth=100 * T["s2_eff"].get((e, r.stratum), 0.0),
                             estimate=r.diff_pp, lo=r.ci_lo_pp, hi=r.ci_hi_pp))
        for sub, eff in [("s3a", T["s3a_eff"]), ("s3b", T["s3b_eff"])]:
            con = pd.read_csv(OUT / f"{sub}_contrasts_{key}.csv")
            for _, r in con[con.contrast != "none - neutral"].iterrows():
                e = r.contrast.split(" ")[0]
                rows.append(dict(model=key, quantity=f"{sub.upper()}: {r.contrast} (pp)", truth=100 * eff.get(e, 0.0),
                                 estimate=r.diff_pp, lo=r.ci_lo_pp, hi=r.ci_hi_pp))
        lmm = pd.read_csv(OUT / f"s3a_lmm_{key}.csv", index_col=0)
        b, se = lmm.loc["sent_c", "coef"], lmm.loc["sent_c", "se"]
        rows.append(dict(model=key, quantity="S3a H2 slope (sent_c)", truth=T["s3a_slope"], estimate=b,
                         lo=b - 1.96 * se, hi=b + 1.96 * se))
        cm = pd.read_csv(OUT / f"checks_confusion_{key}.csv", index_col=0)
        import numpy as np
        acc = np.trace(cm.values) / cm.values.sum()
        rows.append(dict(model=key, quantity="Recognition accuracy", truth=T["recog"], estimate=acc,
                         lo=float("nan"), hi=float("nan")))

    v = pd.DataFrame(rows)
    v["covered"] = (v.lo <= v.truth) & (v.truth <= v.hi)
    v.loc[v.lo.isna(), "covered"] = (v.estimate - v.truth).abs() < 0.05
    n_ok, n = int(v.covered.sum()), len(v)
    txt = ["# Pipeline validation on simulated data", "",
           "Data simulated by `analysis/simulate.py` with known effects (see TRUTH there), in the exact runner output "
           "format, then analysed by the unchanged `analysis/run_all.py`.", "",
           f"**{n_ok}/{n} true values inside the 95% CI** (about 95% expected by chance; a few misses are normal, "
           "systematic misses would indicate a bug).", "", md_table(v), ""]
    (OUT / "validation.md").write_text("\n".join(txt))
    print("\n".join(txt[:5]))
    print(v[~v.covered].to_string())


if __name__ == "__main__":
    main()
