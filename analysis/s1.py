"""S1 (UG responder): H1 and H3.

  * mixed-effects logistic regression  reject ~ emotion * offer * stakes + (1 | prompt variant)
    (offer centred at 30%, stakes effect-coded, Neutral message = reference)
  * MAO (offer with predicted P(accept) = .5) per emotion, pooled and per stakes, with
    cluster-bootstrap 95% CIs (resampling prompt variants); shift vs Neutral in percentage points
  * Fehr-Schmidt (1999) fit by emotion:  P(accept) = sigmoid(lambda * [x - alpha * max(0, 1 - 2x)])
  * fallback graded DV: linear mixed model on logit P(accept) from token log-probabilities
"""
import warnings

import matplotlib
import numpy as np
import pandas as pd
import patsy
from scipy import optimize, special

from analysis.common import EMO_ORDER, fit_mixedlm, md_table
from analysis.glmm import fit_glmm

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

FORMULA = "C(emotion, Treatment('neutral')) * offer_c * stakes_c"
OFFER_CENTER = 0.30


def _prep(df):
    d = df[df.sub_exp == "S1"].copy()
    d["emotion"] = d.emotion.astype(str)
    d["offer_c"] = d.offer_share - OFFER_CENTER
    return d


def _design(d):
    return patsy.dmatrix(FORMULA, d, return_type="dataframe")


def _mao_from_params(params, design_info, emotions, stakes_vals=(-0.5, 0.5, 0.0)):
    """offer* where logit P(reject) = 0, for each emotion x stakes_c (0.0 = averaged over stakes)."""
    out = {}
    for e in emotions:
        for s in stakes_vals:
            grid = pd.DataFrame({"emotion": [e, e], "offer_c": [0.0, 1.0], "stakes_c": [s, s]})
            Xg = patsy.build_design_matrices([design_info], grid, return_type="dataframe")[0]
            a, ab = Xg.values @ params
            b = ab - a
            out[(e, s)] = OFFER_CENTER - a / b if b < 0 else np.nan  # rejection must fall with offer
    return out


def fit_s1(d, n_quad=25, start=None):
    X = _design(d)
    res = fit_glmm(X, d.reject.values, d.variant_id.values, n_quad=n_quad, start=start)
    return res, X.design_info


def mao_bootstrap(d, res, design_info, n_boot=500, seed=0):
    emotions = [e for e in EMO_ORDER if e in set(d.emotion)]
    point = _mao_from_params(res.params.values, design_info, emotions)
    rng = np.random.default_rng(seed)
    clusters = d.variant_id.unique()
    by_cluster = {c: g for c, g in d.groupby("variant_id")}
    boots = []
    for b in range(n_boot):
        pick = rng.choice(clusters, len(clusters), replace=True)
        bd = pd.concat([by_cluster[c].assign(variant_id=f"{c}#{i}") for i, c in enumerate(pick)])
        if bd.reject.nunique() < 2:
            continue
        Xb = patsy.build_design_matrices([design_info], bd, return_type="dataframe")[0]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            rb = fit_glmm(Xb, bd.reject.values, bd.variant_id.values, n_quad=11, start=res.params.values)
        boots.append(_mao_from_params(rb.params.values, design_info, emotions))
    lo, hi = d.offer_share.min(), d.offer_share.max()
    V = res.cov[:-1, :-1]
    slopes = {}
    for (e, s) in point:
        grid = pd.DataFrame({"emotion": [e, e], "offer_c": [0.0, 1.0], "stakes_c": [s, s]})
        Xg = patsy.build_design_matrices([design_info], grid, return_type="dataframe")[0].values
        L = Xg[1] - Xg[0]
        slopes[(e, s)] = (float(L @ res.params.values), float(np.sqrt(L @ V @ L)))
    rows = []
    for (e, s), v in point.items():
        bs = np.array([bt[(e, s)] for bt in boots], float)
        nb = np.array([bt[("neutral", s)] for bt in boots], float) if "neutral" in emotions else None
        shift = bs - nb if nb is not None else None
        rows.append(dict(
            emotion=e, stakes={-0.5: "low (INR 100)", 0.5: "high (INR 10,000)", 0.0: "pooled"}[s],
            MAO=v, MAO_lo=np.nanpercentile(bs, 2.5) if len(bs) else np.nan,
            MAO_hi=np.nanpercentile(bs, 97.5) if len(bs) else np.nan,
            in_range=bool(lo <= v <= hi) if np.isfinite(v) else False,
            shift_vs_neutral_pp=100 * (v - point[("neutral", s)]) if nb is not None else np.nan,
            shift_lo_pp=100 * np.nanpercentile(shift, 2.5) if shift is not None and len(bs) else np.nan,
            shift_hi_pp=100 * np.nanpercentile(shift, 97.5) if shift is not None and len(bs) else np.nan,
            boot_undefined_frac=float(np.mean(~np.isfinite(bs))) if len(bs) else np.nan,
            offer_slope=slopes[(e, s)][0], slope_se=slopes[(e, s)][1],
        ))
    out = pd.DataFrame(rows)
    # MAO is identified only if rejection reliably falls with the offer (95% CI of the slope below 0)
    # and the crossing lies inside the sampled offers; otherwise point estimates/CIs are extrapolations.
    out["identified"] = (out.offer_slope + 1.96 * out.slope_se < 0) & out.in_range
    ref = out[out.emotion == "neutral"].set_index("stakes").identified
    cols = ["MAO", "MAO_lo", "MAO_hi"]
    out.loc[~out.identified, cols] = np.nan
    shift_ok = out.identified & out.stakes.map(ref).fillna(False).astype(bool)
    out.loc[~shift_ok, ["shift_vs_neutral_pp", "shift_lo_pp", "shift_hi_pp"]] = np.nan
    return out, len(boots)


# ------------------------------------------------------------------ Fehr-Schmidt
def fs_nll(theta, x, acc):
    alpha, lam = np.exp(theta)
    u = x - alpha * np.maximum(0, 1 - 2 * x)
    z = lam * u
    return -np.sum(acc * -np.logaddexp(0, -z) + (1 - acc) * -np.logaddexp(0, z))


def fit_fs(x, acc):
    best = None
    for a0 in (0.05, 0.3, 1.0, 3.0):
        for l0 in (5.0, 20.0):
            r = optimize.minimize(fs_nll, np.log([a0, l0]), args=(x, acc), method="Nelder-Mead",
                                  options={"xatol": 1e-6, "fatol": 1e-8, "maxiter": 4000})
            if best is None or r.fun < best.fun:
                best = r
    alpha, lam = np.exp(best.x)
    return alpha, lam


def fehr_schmidt(d, n_boot=500, seed=1):
    rng = np.random.default_rng(seed)
    rows = []
    xmin, xmax = d.offer_share.min(), d.offer_share.max()
    for e in [e for e in EMO_ORDER if e in set(d.emotion)]:
        g = d[d.emotion == e]
        alpha, lam = fit_fs(g.offer_share.values, g.accept.values)
        mao = alpha / (1 + 2 * alpha)
        by_c = [cg for _, cg in g.groupby("variant_id")]
        bs = []
        for _ in range(n_boot):
            bd = pd.concat([by_c[i] for i in rng.integers(0, len(by_c), len(by_c))])
            bs.append(fit_fs(bd.offer_share.values, bd.accept.values)[0])
        bs = np.array(bs)
        rows.append(dict(emotion=e, alpha=alpha, alpha_lo=np.percentile(bs, 2.5), alpha_hi=np.percentile(bs, 97.5),
                         lam=lam, implied_MAO=mao, identified=bool(xmin <= mao <= xmax),
                         accept_rate=g.accept.mean(), n=len(g)))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ log-prob fallback
def logprob_lmm(d):
    if "p_accept_lp" not in d or d.p_accept_lp.notna().sum() < 50:
        return None
    g = d[d.p_accept_lp.notna()].copy()
    g["logit_pa"] = special.logit(g.p_accept_lp.clip(1e-4, 1 - 1e-4))
    m = fit_mixedlm(f"logit_pa ~ {FORMULA}", g, g.variant_id)
    return m


# ------------------------------------------------------------------ driver
def run(df, out, model_label, n_boot=500):
    d = _prep(df)
    lines = [f"## S1 UG-responder ({model_label})", ""]
    rate = (d.groupby(["emotion", "stakes", "offer_share"], observed=True).reject.mean()
            .unstack("offer_share").round(3))
    rate.columns = [f"off{int(round(c * 100))}%" for c in rate.columns]
    rate.to_csv(out / f"s1_reject_rates_{model_label}.csv")
    lines += ["### Rejection rate by emotion x stakes x offer", "", md_table(rate), ""]

    ceiling = d.reject.mean() < 0.02 or d.reject.mean() > 0.98
    if d.reject.nunique() < 2:
        lines += ["**All decisions identical - logistic model not estimable (ceiling/floor).**", ""]
        return "\n".join(lines), {}

    res, di = fit_s1(d)
    summ = res.summary()
    summ.to_csv(out / f"s1_glmm_{model_label}.csv")
    lines += [f"### GLMM: reject ~ {FORMULA} + (1|variant)",
              f"n={res.n_obs}, variants={res.n_groups}, sigma_variant={res.sigma:.3f}, logLik={res.loglik:.1f}, "
              f"converged={res.converged}, separation_warning={res.separation_warning}", "",
              md_table(summ[["coef", "se", "p", "OR"]]), ""]
    emo_terms = [c for c in res.params.index if c.startswith("C(emotion") and ":" not in c]
    inter_terms = [c for c in res.params.index if c.startswith("C(emotion") and ":" in c]
    chi, df_, p = res.wald(emo_terms)
    lines.append(f"Wald test, emotion main effects (at offer 30%, averaged over stakes): chi2({df_})={chi:.2f}, p={p:.4g}")
    chi, df_, p = res.wald(inter_terms)
    lines += [f"Wald test, all emotion interactions: chi2({df_})={chi:.2f}, p={p:.4g}",
              f"H1 offer slope (neutral, avg stakes): b={res.params['offer_c']:.2f} (se {res.bse['offer_c']:.2f}); "
              "negative = rejection falls as offer rises", ""]

    mao, nb = mao_bootstrap(d, res, di, n_boot=n_boot)
    mao.to_csv(out / f"s1_mao_{model_label}.csv", index=False)
    lines += [f"### MAO by emotion (cluster bootstrap over prompt variants, {nb} resamples)",
              "MAO is reported only where it is identified: the emotion's offer slope (logit of rejection per "
              "unit share) has a 95% CI below zero and the 50% crossing lies within the sampled offers. "
              "Blank = not identified (no reliable offer dependence, or crossing outside the grid).", "",
              md_table(mao.drop(columns=["boot_undefined_frac"])), ""]
    if ceiling:
        lines.append("**Ceiling/floor: <2% or >98% rejections; MAO likely outside the sampled range "
                     "(pre-registered fallback applies).**")

    fs = fehr_schmidt(d, n_boot=max(100, n_boot // 2))
    pooled_id = mao[mao.stakes == "pooled"].set_index("emotion").identified
    fs["identified"] = fs.identified & fs.emotion.map(pooled_id).fillna(False).astype(bool)
    fs.loc[~fs.identified, ["alpha", "alpha_lo", "alpha_hi", "implied_MAO"]] = np.nan
    fs.to_csv(out / f"s1_fehr_schmidt_{model_label}.csv", index=False)
    lines += ["### Fehr-Schmidt disadvantageous inequity aversion by emotion", "", md_table(fs), ""]

    lp = logprob_lmm(d)
    if lp is not None:
        t = pd.DataFrame({"coef": lp.fe_params, "se": lp.bse_fe, "p": lp.pvalues[lp.fe_params.index]})
        t.to_csv(out / f"s1_logprob_lmm_{model_label}.csv")
        lines += ["### Graded DV: LMM on logit P(accept) from log-probabilities", "", md_table(t), ""]

    _plot(d, res, di, out / f"fig_s1_curves_{model_label}.png", model_label)
    return "\n".join(lines), dict(glmm=res, mao=mao, fs=fs)


def _plot(d, res, di, path, label):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    colors = {"none": "#888888", "neutral": "#1f77b4", "angry": "#d62728", "sad": "#9467bd", "happy": "#2ca02c"}
    xs = np.linspace(d.offer_share.min(), d.offer_share.max(), 100)
    for ax, (s, name) in zip(axes, [(-0.5, "INR 100"), (0.5, "INR 10,000")]):
        sub = d[d.stakes_c == s]
        for e in [e for e in EMO_ORDER if e in set(d.emotion)]:
            obs = sub[sub.emotion == e].groupby("offer_share").accept.mean()
            ax.plot(obs.index, obs.values, "o", color=colors[e], alpha=0.6)
            grid = pd.DataFrame({"emotion": e, "offer_c": xs - OFFER_CENTER, "stakes_c": s})
            Xg = patsy.build_design_matrices([di], grid, return_type="dataframe")[0]
            ax.plot(xs, 1 - special.expit(Xg.values @ res.params.values), color=colors[e], label=e)
        ax.axhline(0.5, ls=":", c="k", lw=0.8)
        ax.set_title(f"S1 {label}: stakes {name}")
        ax.set_xlabel("offer (share of pie)")
    axes[0].set_ylabel("P(accept)")
    axes[1].legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
