"""Refit every planned emotion-vs-neutral test with MESSAGE as a random factor (P12).

Why: emotion is manipulated *between messages* (5 messages per emotion). The original models have one random
intercept per variant_id = sub_exp|paraphrase|message, i.e. per paraphrase x message cell. That treats the four
paraphrases of the same message as unrelated, so a message-specific quirk ("this particular sad text") is counted
as an emotion effect, and the SEs of emotion contrasts are too small.

Model here (same fixed effects as the main analysis, plus paraphrase as a fixed effect):
    outcome ~ <original fixed effects> + C(paraphrase) + (1 | message) + (1 | message:paraphrase)
  * S1: two-level nested random-intercept logistic GLMM (nested Gauss-Hermite quadrature, ML)
  * S2/S3: MixedLM (REML), groups = message, variance component for paraphrase within message
Inference uses t with df = (#message groups - #emotion levels): the emotion contrast is a between-message
comparison, so the number of messages, not trials, bounds the information. z-based p values are also reported.

  python -m analysis.message_re --out main
  python -m analysis.message_re --out followup     # also prints the pre-registered F1/F2 under this model
Reads results/<out>/tidy_trials.csv and all_effects.csv; writes message_re.csv and message_re.md there.
"""
import argparse
import warnings
from dataclasses import dataclass

import numpy as np
import pandas as pd
import patsy
import statsmodels.formula.api as smf
from scipy import optimize, sparse, special, stats

from analysis.common import holm, md_table
from analysis.forest import bh
from analysis.s1 import FORMULA as S1_FORMULA, OFFER_CENTER
from analysis.s2s3 import SPECS
from config import RESULTS_DIR

EMOS = ["angry", "sad", "happy"]
EMO_TERM = "C(emotion, Treatment('neutral'))[T.{}]"


# --------------------------------------------------------------------------- nested logistic GLMM
@dataclass
class NestedGLMM:
    params: pd.Series
    bse: pd.Series
    sd_msg: float
    sd_sub: float
    loglik: float
    converged: bool


def fit_nested_glmm(X: pd.DataFrame, y, g_outer, g_inner, n_quad=12, ridge=1e-6) -> NestedGLMM:
    """logit P(y=1) = X b + u_outer + v_inner,  u ~ N(0, s1^2), v ~ N(0, s2^2), inner nested in outer."""
    Xv, y = np.asarray(X, float), np.asarray(y, float)
    inner_codes, inner_uni = pd.factorize(pd.Series(np.asarray(g_outer)).astype(str) + "||" + pd.Series(np.asarray(g_inner)).astype(str))
    outer_of_inner = pd.factorize(pd.Series(inner_uni).str.split(r"\|\|").str[0])[0]
    n, p = Xv.shape
    K, G = len(inner_uni), outer_of_inner.max() + 1
    M_in = sparse.csr_matrix((np.ones(n), (inner_codes, np.arange(n))), shape=(K, n))
    M_out = sparse.csr_matrix((np.ones(K), (outer_of_inner, np.arange(K))), shape=(G, K))
    nodes, w = np.polynomial.hermite.hermgauss(n_quad)
    logw = np.log(w / np.sqrt(np.pi))
    Q = n_quad

    def nll_grad(theta):
        beta, s1, s2 = theta[:p], np.exp(theta[p]), np.exp(theta[p + 1])
        u, v = np.sqrt(2) * s1 * nodes, np.sqrt(2) * s2 * nodes
        lin = (Xv @ beta)[:, None, None] + u[None, :, None] + v[None, None, :]     # (n,Q,R)
        ll = y[:, None, None] * lin - np.logaddexp(0, lin)
        S = (M_in @ ll.reshape(n, Q * Q)).reshape(K, Q, Q)                        # inner sums
        A = special.logsumexp(S + logw[None, None, :], axis=2)                    # (K,Q) integrate v
        B = M_out @ A + logw[None, :]                                             # (G,Q)
        L = special.logsumexp(B, axis=1)                                          # (G,)
        post_q = np.exp(B - L[:, None])                                           # (G,Q)
        post_r = np.exp(S + logw[None, None, :] - A[:, :, None])                  # (K,Q,R)
        W = post_q[outer_of_inner][:, :, None] * post_r                           # (K,Q,R)
        Wi = W[inner_codes]                                                       # (n,Q,R)
        R = Wi * (y[:, None, None] - special.expit(lin))
        g_beta = Xv.T @ R.sum(axis=(1, 2))
        g_s1 = np.sum(R * u[None, :, None])
        g_s2 = np.sum(R * v[None, None, :])
        nll = -L.sum() + ridge * beta @ beta
        return nll, -np.concatenate([g_beta, [g_s1, g_s2]]) + np.concatenate([2 * ridge * beta, [0, 0]])

    theta0 = np.concatenate([np.zeros(p), [np.log(0.5), np.log(0.5)]])
    res = optimize.minimize(nll_grad, theta0, jac=True, method="BFGS", options={"maxiter": 3000, "gtol": 1e-5})
    th = res.x
    H = np.zeros((p + 2, p + 2))
    for k in range(p + 2):
        h = 1e-4 * max(1.0, abs(th[k]))
        e = np.zeros(p + 2)
        e[k] = h
        H[:, k] = (nll_grad(th + e)[1] - nll_grad(th - e)[1]) / (2 * h)
    H = (H + H.T) / 2
    try:
        cov = np.linalg.inv(H)
    except np.linalg.LinAlgError:
        cov = np.linalg.pinv(H)
    se = np.sqrt(np.clip(np.diag(cov), 0, None))
    names = list(X.columns)
    return NestedGLMM(pd.Series(th[:p], names), pd.Series(se[:p], names), float(np.exp(th[p])),
                      float(np.exp(th[p + 1])), float(-res.fun), bool(res.success))


# --------------------------------------------------------------------------- fits
def _df(d):
    return d.msg_id.nunique() - d.emotion.nunique()


def s1_effects(d, model):
    d = d[d.sub_exp == "S1"].copy()
    d["emotion"] = d.emotion.astype(str)
    d["offer_c"] = d.offer_share - OFFER_CENTER
    X = patsy.dmatrix(S1_FORMULA + " + C(paraphrase)", d, return_type="dataframe")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = fit_nested_glmm(X, d.reject.values, d.msg_id.values, d.paraphrase.values)
    rows = []
    for e in EMOS:
        k = EMO_TERM.format(e)
        est, se = r.params[k], r.bse[k]
        estimable = se < 5 and d.reject.mean() > 0.005
        rows.append(dict(model=model, test="S1 rejection (log-OR)", emotion=e, est_new=est,
                         lo_new=est - 1.96 * se, hi_new=est + 1.96 * se, se_new=se, df=_df(d),
                         estimable=estimable, sd_msg=r.sd_msg, sd_msg_para=r.sd_sub, converged=r.converged))
    return rows


def lmm_effects(d_all, model, sub):
    spec = SPECS[sub]
    d = d_all[d_all.sub_exp == sub].copy()
    if d.empty or d.share.nunique() < 2:
        return []
    d["emotion"] = d.emotion.astype(str)
    if sub == "S3a":
        d["sent_c"] = d.sent_share - d.sent_share.mean()
    f = spec["formula"] + " + C(paraphrase)"
    m = None
    for method in ("bfgs", "lbfgs", "powell"):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                m = smf.mixedlm(f, d, groups=d.msg_id, re_formula="1",
                                vc_formula={"para": "0 + C(paraphrase)"}).fit(reml=True, method=method)
            if m.converged:
                break
        except (np.linalg.LinAlgError, ValueError):
            continue
    di = patsy.dmatrix(f.split("~")[1], d, return_type="dataframe").design_info
    names = list(m.fe_params.index)
    V = m.cov_params().loc[names, names].values
    base = {"stakes_c": 0.0, "paraphrase": d.paraphrase.min()}
    if sub == "S3a":
        base["sent_c"] = 0.0
    strata = sorted(d[spec["by"]].unique()) if spec["by"] else [None]
    rows = []
    for s in strata:
        for e in EMOS:
            ra, rb = {**base, "emotion": e}, {**base, "emotion": "neutral"}
            if s is not None:
                ra[spec["by"]] = rb[spec["by"]] = s
            Xa = patsy.build_design_matrices([di], pd.DataFrame([ra]), return_type="dataframe")[0].values[0]
            Xb = patsy.build_design_matrices([di], pd.DataFrame([rb]), return_type="dataframe")[0].values[0]
            L = Xa - Xb
            est, se = 100 * L @ m.fe_params.values, 100 * np.sqrt(L @ V @ L)
            name = {"S2": "S2 giving", "S3a": "S3a returned", "S3b": "S3b sent"}[sub]
            test = f"{name} ({s}) (pp)" if sub == "S2" else f"{name} (pp)"
            rows.append(dict(model=model, test=test, emotion=e, est_new=est, lo_new=est - 1.96 * se,
                             hi_new=est + 1.96 * se, se_new=se, df=_df(d), estimable=True,
                             sd_msg=100 * np.sqrt(max(float(m.cov_re.iloc[0, 0]), 0)),
                             sd_msg_para=100 * np.sqrt(max(float(m.vcomp[0]), 0)), converged=m.converged))
    return rows


def run(out_name):
    out = RESULTS_DIR / out_name
    df = pd.read_csv(out / "tidy_trials.csv", low_memory=False)
    rows = []
    for model, g in df.groupby("model_key"):
        print(f"[{model}] S1 nested GLMM ...", flush=True)
        rows += s1_effects(g, model)
        for sub in ("S2", "S3a", "S3b"):
            rows += lmm_effects(g, model, sub)
    new = pd.DataFrame(rows)
    new["p_z"] = 2 * stats.norm.sf(np.abs(new.est_new / new.se_new))
    new["p_t"] = 2 * stats.t.sf(np.abs(new.est_new / new.se_new), new.df)
    new.loc[~new.estimable, ["p_z", "p_t"]] = np.nan
    ok = new.p_t.notna()
    for col in ("p_holm_study", "p_bh_study"):
        new[col] = np.nan
    new.loc[ok, "p_holm_study"] = holm(new.loc[ok, "p_t"])
    new.loc[ok, "p_bh_study"] = bh(new.loc[ok, "p_t"])
    old = pd.read_csv(out / "all_effects.csv")[["model", "test", "emotion", "est", "lo", "hi", "p",
                                                  "p_holm_study", "p_bh_study"]]
    old = old.rename(columns={"est": "est_old", "lo": "lo_old", "hi": "hi_old", "p": "p_old",
                              "p_holm_study": "p_holm_old", "p_bh_study": "p_bh_old"})
    m = old.merge(new, on=["model", "test", "emotion"], how="outer")
    m.to_csv(out / "message_re.csv", index=False)
    write_md(m, out, out_name)
    return m


def _fmt_ci(e, lo, hi):
    return "" if pd.isna(e) else f"{e:+.2f} [{lo:+.2f}, {hi:+.2f}]"


def _p(x):
    return "n/a" if pd.isna(x) else ("< .001" if x < .001 else f"{x:.3f}")


def write_md(m, out, out_name):
    m = m.copy()
    m["survives_old"] = m.p_holm_old < .05
    m["survives_new"] = m.p_holm_study < .05
    m["fdr_old"] = m.p_bh_old < .05
    m["fdr_new"] = m.p_bh_study < .05
    key = m[m.fdr_old | m.fdr_new | m.survives_old | m.survives_new]
    tab = pd.DataFrame({
        "model": key.model, "test": key.test, "emotion": key.emotion,
        "original [95% CI]": [_fmt_ci(*r) for r in key[["est_old", "lo_old", "hi_old"]].values],
        "with message RE [95% CI]": [_fmt_ci(*r) for r in key[["est_new", "lo_new", "hi_new"]].values],
        "Holm old": key.p_holm_old.map(_p), "Holm new": key.p_holm_study.map(_p),
        "FDR old": key.p_bh_old.map(_p), "FDR new": key.p_bh_study.map(_p)})
    vc = m.groupby(["model", "test"])[["sd_msg", "sd_msg_para", "df"]].first().reset_index()
    lines = [f"# Emotion effects with message as a random factor ({out_name})", "",
             "Model: original fixed effects + C(paraphrase) + (1 | message) + (1 | message:paraphrase). "
             "p values: t with df = #message groups - #emotion levels (emotion varies between messages); "
             "Holm and BH across the whole study, as in `forest.md`. Script: `analysis/message_re.py` (P12).", "",
             f"- Holm-significant study-wide: **{int(m.survives_old.sum())} → {int(m.survives_new.sum())}**",
             f"- FDR-significant study-wide: **{int(m.fdr_old.sum())} → {int(m.fdr_new.sum())}**", "",
             "## Effects significant (FDR or Holm) in either analysis", "", md_table(tab.reset_index(drop=True)), "",
             "## Between-message variability (SD of message intercepts; S1 on logit scale, others in pp)", "",
             md_table(vc, floatfmt=2), "",
             "## All tests", "", md_table(m[["model", "test", "emotion", "est_old", "p_old", "est_new", "se_new",
                                           "p_z", "p_t", "p_holm_study", "p_bh_study"]], floatfmt=3), ""]
    if out_name.startswith("followup"):
        lines += ["## Pre-registered confirmatory tests under this model (one-sided, Holm over F1, F2)", ""]
        f = []
        for fid, test, emo in [("F1", "S1 rejection (log-OR)", "sad"), ("F2", "S3b sent (pp)", "angry")]:
            r = m[(m.model == "qwen25_7b") & (m.test == test) & (m.emotion == emo)].iloc[0]
            f.append(dict(id=fid, estimate=_fmt_ci(r.est_new, r.lo_new, r.hi_new),
                          p_one_sided=stats.t.cdf(r.est_new / r.se_new, r.df)))
        f = pd.DataFrame(f)
        f["p_holm"] = holm(f.p_one_sided)
        lines += [md_table(f), ""]
    (out / "message_re.md").write_text("\n".join(lines))
    print(f"-> {out / 'message_re.md'}")
    print("\n".join(lines[:8]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="main")
    run(ap.parse_args().out)
