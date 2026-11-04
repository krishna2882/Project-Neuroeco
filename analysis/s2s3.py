"""S2 (UG vs DG proposer; H3, H4), S3a (TG trustee; H2, H3), S3b (TG investor; H3).

Linear mixed models on the share given / returned / sent with a random intercept per prompt
variant (statsmodels MixedLM, REML). A fractional-logit GLM with variant-clustered SEs is fitted
as the pre-specified robustness check for bounded, non-normal shares. Planned emotion-vs-neutral
contrasts are Holm-corrected within each sub-experiment.
"""
import warnings

import matplotlib
import numpy as np
import pandas as pd
import patsy
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

from analysis.common import EMO_ORDER, cohens_d, fit_mixedlm, holm, md_table

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

EMO = "C(emotion, Treatment('neutral'))"
SPECS = {
    "S2": dict(formula=f"share ~ {EMO} * C(game, Treatment('DG')) * stakes_c", by="game",
               dv="share of pie given"),
    "S3a": dict(formula=f"share ~ {EMO} * sent_c * stakes_c", by=None, dv="share of tripled amount returned"),
    "S3b": dict(formula=f"share ~ {EMO} * stakes_c", by=None, dv="share of endowment sent"),
}


def _prep(df, sub):
    d = df[df.sub_exp == sub].copy()
    d["emotion"] = d.emotion.astype(str)
    if sub == "S3a":
        d["sent_c"] = d.sent_share - d.sent_share.mean()
    return d


def _fit_lmm(d, formula):
    return fit_mixedlm(formula, d, d.variant_id)


def _contrast(m, design_info, row_a: dict, row_b: dict):
    Xa = patsy.build_design_matrices([design_info], pd.DataFrame([row_a]), return_type="dataframe")[0].values[0]
    Xb = patsy.build_design_matrices([design_info], pd.DataFrame([row_b]), return_type="dataframe")[0].values[0]
    L = Xa - Xb
    fe = m.fe_params.values
    V = m.cov_params().loc[m.fe_params.index, m.fe_params.index].values
    est = L @ fe
    se = np.sqrt(L @ V @ L)
    return est, se, L


def run(df, out, model_label):
    blocks, results = [], {}
    for sub, spec in SPECS.items():
        d = _prep(df, sub)
        if d.empty:
            continue
        lines = [f"## {sub} ({model_label}): {spec['dv']}", ""]
        by = spec["by"]
        desc = d.groupby(([by] if by else []) + ["emotion", "stakes"], observed=True).share.agg(
            ["mean", "std", "count"]).round(3)
        if sub == "S3a":
            desc = d.groupby(["sent_share", "emotion"], observed=True).share.agg(["mean", "std", "count"]).round(3)
        desc.to_csv(out / f"{sub.lower()}_descriptives_{model_label}.csv")
        lines += ["### Descriptives", "", md_table(desc), ""]

        if d.share.nunique() < 2:
            lines += ["**No variance in the outcome - model not estimable.**", ""]
            blocks.append("\n".join(lines))
            continue
        m = _fit_lmm(d, spec["formula"])
        di = patsy.dmatrix(spec["formula"].split("~")[1], d, return_type="dataframe").design_info
        fe = pd.DataFrame({"coef": m.fe_params, "se": m.bse_fe, "p": m.pvalues[m.fe_params.index]})
        fe.to_csv(out / f"{sub.lower()}_lmm_{model_label}.csv")
        lines += [f"### LMM: {spec['formula']} + (1|variant)",
                  f"n={int(m.nobs)}, variants={len(m.random_effects)}, var(variant)={float(m.cov_re.iloc[0, 0]):.4f}, "
                  f"residual var={m.scale:.4f}, converged={m.converged}", "", md_table(fe), ""]

        # Planned contrasts: each emotion (and no-message) vs neutral, within game for S2
        base = {"stakes_c": 0.0}
        if sub == "S3a":
            base["sent_c"] = 0.0
        strata = sorted(d[by].unique()) if by else [None]
        rows = []
        for s in strata:
            for e in [e for e in EMO_ORDER if e != "neutral" and e in set(d.emotion)]:
                ra = {**base, "emotion": e}
                rb = {**base, "emotion": "neutral"}
                if by:
                    ra[by] = rb[by] = s
                est, se, _ = _contrast(m, di, ra, rb)
                ga = d[(d.emotion == e) & ((d[by] == s) if by else True)].share
                gb = d[(d.emotion == "neutral") & ((d[by] == s) if by else True)].share
                dd, dlo, dhi = cohens_d(ga, gb)
                rows.append(dict(stratum=s or "all", contrast=f"{e} - neutral", diff_pp=100 * est,
                                 ci_lo_pp=100 * (est - 1.96 * se), ci_hi_pp=100 * (est + 1.96 * se),
                                 p=2 * stats.norm.sf(abs(est / se)), cohens_d=dd, d_lo=dlo, d_hi=dhi,
                                 planned=e != "none"))
        con = pd.DataFrame(rows)
        con["p_holm"] = np.nan
        con.loc[con.planned, "p_holm"] = holm(con.loc[con.planned, "p"])
        con.to_csv(out / f"{sub.lower()}_contrasts_{model_label}.csv", index=False)
        lines += ["### Emotion vs Neutral contrasts (model-based, at average stakes; Holm over planned emotion "
                  "contrasts; 'none - neutral' = effect of a neutral message vs no message, not in the family)", "",
                  md_table(con.drop(columns=["planned"])), ""]

        names = list(m.fe_params.index)
        if sub == "S2":
            # H4: Emotion x Game; key test = (angry - neutral)_UG - (angry - neutral)_DG
            inter = [n for n in names if n.startswith("C(emotion") and "C(game" in n and "stakes" not in n
                     and "none" not in n]
            lines.append(_wald(m, inter, "H4 Emotion x Game (angry/sad/happy, joint)"))
            for e in ("angry", "sad", "happy"):
                ug, se_ug, L1 = _contrast(m, di, {**base, "emotion": e, "game": "UG"}, {**base, "emotion": "neutral", "game": "UG"})
                dg, se_dg, L2 = _contrast(m, di, {**base, "emotion": e, "game": "DG"}, {**base, "emotion": "neutral", "game": "DG"})
                L = L1 - L2
                V = m.cov_params().loc[names, names].values
                est, se = L @ m.fe_params.values, np.sqrt(L @ V @ L)
                lines.append(f"- ({e} - neutral)_UG - ({e} - neutral)_DG = {100 * est:+.2f} pp "
                             f"[{100 * (est - 1.96 * se):+.2f}, {100 * (est + 1.96 * se):+.2f}], "
                             f"p={2 * stats.norm.sf(abs(est / se)):.4g}")
            ug_dg = _contrast(m, di, {**base, "emotion": "neutral", "game": "UG"}, {**base, "emotion": "neutral", "game": "DG"})
            lines.append(f"- Strategic giving (UG - DG, neutral message): {100 * ug_dg[0]:+.2f} pp "
                         f"(se {100 * ug_dg[1]:.2f})")
        if sub == "S3a":
            lines.append(f"- H2 slope of share returned on share sent (neutral, avg stakes): "
                         f"b={m.fe_params['sent_c']:.3f} (se {m.bse_fe['sent_c']:.3f}, p={m.pvalues['sent_c']:.4g}); "
                         "positive = more returned when more was sent")
            inter = [n for n in names if n.startswith("C(emotion") and "sent_c" in n and "stakes" not in n
                     and "none" not in n]
            lines.append(_wald(m, inter, "Emotion x Amount-sent (joint)"))
        lines.append("")

        # Robustness: fractional logit with variant-clustered SEs
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fl = smf.glm(spec["formula"], d, family=sm.families.Binomial()).fit(
                cov_type="cluster", cov_kwds={"groups": pd.factorize(d.variant_id)[0]})
        emo_rows = [n for n in fl.params.index if n.startswith("C(emotion") and ":" not in n]
        fr = pd.DataFrame({"coef_logit": fl.params[emo_rows], "se": fl.bse[emo_rows], "p": fl.pvalues[emo_rows]})
        fr.to_csv(out / f"{sub.lower()}_fraclogit_{model_label}.csv")
        lines += ["### Robustness: fractional-logit GLM, cluster-robust SEs (emotion main effects)", "",
                  md_table(fr), ""]
        _plot(d, sub, by, out / f"fig_{sub.lower()}_{model_label}.png", model_label, spec["dv"])
        blocks.append("\n".join(lines))
        results[sub] = dict(model=m, contrasts=con)
    return "\n\n".join(blocks), results


def _wald(m, terms, label):
    if not terms:
        return f"- {label}: no terms"
    r = m.wald_test(np.array([[1.0 if n == t else 0.0 for n in m.params.index] for t in terms]), scalar=True)
    return f"- {label}: chi2({len(terms)})={float(r.statistic):.2f}, p={float(r.pvalue):.4g}"


def _plot(d, sub, by, path, label, dv):
    emos = [e for e in EMO_ORDER if e in set(d.emotion)]
    colors = {"none": "#888888", "neutral": "#1f77b4", "angry": "#d62728", "sad": "#9467bd", "happy": "#2ca02c"}
    if sub == "S3a":
        groups = sorted(d.sent_share.unique())
        key, lab = "sent_share", lambda g: f"sent {int(g * 100)}%"
    elif by:
        groups, key, lab = sorted(d[by].unique()), by, str
    else:
        groups, key, lab = [None], None, lambda g: "all"
    fig, ax = plt.subplots(figsize=(7, 3.6))
    w = 0.8 / len(emos)
    for i, e in enumerate(emos):
        means, ses = [], []
        for g in groups:
            s = d[(d.emotion == e) & ((d[key] == g) if key else True)].share
            means.append(s.mean())
            ses.append(s.std(ddof=1) / np.sqrt(len(s)) if len(s) > 1 else 0)
        ax.bar(np.arange(len(groups)) + i * w - 0.4 + w / 2, means, w, yerr=1.96 * np.array(ses),
               color=colors[e], label=e, capsize=2)
    ax.set_xticks(range(len(groups)), [lab(g) for g in groups])
    ax.set_ylabel(dv)
    ax.set_title(f"{sub} - {label}")
    ax.legend(frameon=False, fontsize=8, ncol=5)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
