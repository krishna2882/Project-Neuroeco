"""Log-probabilities as a graded "value signal" for accepting an offer (exploratory, post hoc; P18).

In neuroeconomics, responder behaviour is modelled as a valuation curve: the subjective value of accepting rises with the
offer, and rejection happens below an indifference point (the minimum acceptable offer, MAO). Choices at T = 1.0 are
noisy samples, and at ceiling they identify no MAO. The model's own probability of answering "accept" (S1 log-probs,
same prompts and seeds) is a continuous signal, so the valuation curve and its shift by emotion can be estimated directly.

Per run (model x message set) a linear mixed model on logit P(accept):
    logit_pa ~ C(emotion, Treatment('neutral')) * offer_c + stakes_c + C(paraphrase)
               + (1 | message) + (1 | message:paraphrase)              (P12-style random structure)
For each emotion vs neutral it reports:
    value shift  = change in logit P(accept) at a 30% offer (does the emotion make the same offer more/less acceptable?)
    gain shift   = change in the slope on offer (does the emotion change sensitivity to fairness?)
    indifference = offer where P(accept) = .5 (the MAO analogue), and its shift, with parametric-bootstrap 95% CIs.
Also: calibration of P(accept) against the sampled choices (validity of the signal).

  python -m analysis.value_signal   -> results/value_signal/value_signal.md, .csv, fig_value_curves.png
"""
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import statsmodels.formula.api as smf  # noqa: E402
from scipy import special, stats  # noqa: E402

from analysis.common import holm, md_table  # noqa: E402
from analysis.s1 import OFFER_CENTER  # noqa: E402
from config import RESULTS_DIR  # noqa: E402

OUT = RESULTS_DIR / "value_signal"
RUNS = [("main", "llama31_8b", "Llama-3.1-8B", "main"), ("main", "qwen25_7b", "Qwen2.5-7B", "main"),
        ("followup", "llama31_8b", "Llama-3.1-8B", "follow-up"), ("followup", "qwen25_7b", "Qwen2.5-7B", "follow-up"),
        ("ext2", "qwen25_3b", "Qwen2.5-3B", "main"), ("ext2", "qwen25_14b", "Qwen2.5-14B", "main"),
        ("ext2", "qwen25_7b_q8", "Qwen2.5-7B Q8", "main")]
EMOS = ["angry", "sad", "happy"]
# validated categorical palette (dataviz reference, light mode); markers give a second, non-colour encoding
COL = {"neutral": "#2a78d6", "angry": "#eb6834", "sad": "#1baf7a", "happy": "#eda100", "none": "#8a8a85"}
MARK = {"neutral": "o", "angry": "s", "sad": "^", "happy": "D", "none": "x"}
TERM = "C(emotion, Treatment('neutral'))[T.{}]"
N_SIM = 4000


def load(folder, model):
    t = pd.read_csv(RESULTS_DIR / folder / "tidy_trials.csv", low_memory=False)
    d = t[(t.sub_exp == "S1") & (t.model_key == model) & t.p_accept_lp.notna()].copy()
    d["emotion"] = d.emotion.astype(str)
    d["offer_c"] = d.offer_share - OFFER_CENTER
    d["logit_pa"] = special.logit(d.p_accept_lp.clip(1e-3, 1 - 1e-3))
    return d


def fit(d):
    f = "logit_pa ~ C(emotion, Treatment('neutral')) * offer_c + stakes_c + C(paraphrase)"
    last = None
    for method in ("lbfgs", "bfgs", "powell"):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                m = smf.mixedlm(f, d, groups=d.msg_id, re_formula="1",
                                vc_formula={"para": "0 + C(paraphrase)"}).fit(reml=True, method=method)
            if np.all(np.isfinite(m.bse_fe)):
                return m
            last = m
        except Exception:  # noqa: BLE001
            continue
    return last


def effects(m, d):
    fe = m.fe_params
    V = m.cov_params().loc[fe.index, fe.index].values
    sims = pd.DataFrame(np.random.default_rng(1).multivariate_normal(fe.values, V, N_SIM), columns=fe.index)
    para = [k for k in fe.index if k.startswith("C(paraphrase)")]
    dfree = d.msg_id.nunique() - d.emotion.nunique()
    q = stats.t.ppf(.975, dfree)

    def indiff(s, e):
        a = s["Intercept"] + (s[para].sum(axis=1) / (len(para) + 1) if para else 0)
        b = s["offer_c"]
        if e != "neutral":
            a = a + s[TERM.format(e)]
            b = b + s[f"{TERM.format(e)}:offer_c"]
        return OFFER_CENTER - a / b

    base = indiff(sims, "neutral")
    lo_slope = fe["offer_c"] - q * m.bse_fe["offer_c"]

    def identified(x):  # crossing must lie in (or within 5 pp of) the tested 5-50% range, with a reliably rising curve
        return lo_slope > 0 and -0.0 <= np.median(x) <= 0.55
    rows = []
    for e in [x for x in EMOS + ["none"] if x in set(d.emotion)]:
        k, ks = TERM.format(e), f"{TERM.format(e)}:offer_c"
        v, sv = fe[k], m.bse_fe[k]
        g, sg = fe[ks], m.bse_fe[ks]
        ie = indiff(sims, e)
        shift = (ie - base) * 100
        ok = identified(base) and identified(ie)
        rows.append(dict(emotion=e, value_shift=v, value_lo=v - q * sv, value_hi=v + q * sv,
                         p_value=2 * stats.t.sf(abs(v / sv), dfree),
                         gain_shift=g, gain_lo=g - q * sg, gain_hi=g + q * sg, p_gain=2 * stats.t.sf(abs(g / sg), dfree),
                         indiff_neutral=100 * np.median(base), indiff=100 * np.median(ie),
                         indiff_shift=np.median(shift), shift_lo=np.percentile(shift, 2.5),
                         shift_hi=np.percentile(shift, 97.5), indiff_identified=ok, df=dfree))
    return pd.DataFrame(rows)


def calibration(d):
    bins = pd.cut(d.p_accept_lp, [0, .1, .3, .5, .7, .9, 1.0], include_lowest=True)
    return d.groupby(bins, observed=True).agg(n=("accept", "size"), mean_p=("p_accept_lp", "mean"),
                                              accept_rate=("accept", "mean")).round(3)


def figure(curves):
    n = len(curves)
    fig, axes = plt.subplots(2, 4, figsize=(15, 7.2), sharex=True, sharey=True)
    axes = axes.ravel()
    for ax, (title, c) in zip(axes, curves):
        for e in ["none", "neutral", "angry", "sad", "happy"]:
            s = c[c.emotion == e]
            if s.empty:
                continue
            ax.plot(s.offer, s.p, color=COL[e], lw=2, ls="--" if e == "none" else "-", marker=MARK[e], ms=6,
                    mec="white", mew=1.0, label=e if e != "none" else "no message", zorder=3 if e != "none" else 2)
        ax.axhline(.5, color="#c9c8c2", lw=1, zorder=1)
        ax.set_title(title, fontsize=11, loc="left")
        ax.grid(axis="y", color="#ecebe7", lw=.8)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.spines["left"].set_color("#b5b4ad")
        ax.spines["bottom"].set_color("#b5b4ad")
        ax.tick_params(colors="#55554f", labelsize=9)
    for ax in axes[n:]:
        ax.axis("off")
    handles, labels = axes[0].get_legend_handles_labels()
    axes[-1].legend(handles, labels, loc="center", frameon=False, fontsize=11, title="Counterpart's message")
    for ax in list(axes[4:n]) + [axes[3]]:
        ax.set_xlabel("Offer (% of the pie)", color="#55554f")
        ax.xaxis.set_tick_params(labelbottom=True)
    for ax in (axes[0], axes[4]):
        ax.set_ylabel("Model's P(accept)", color="#55554f")
    fig.suptitle("Valuation curves from log-probabilities: probability of accepting an ultimatum offer",
                 x=.01, ha="left", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, .95))
    fig.savefig(OUT / "fig_value_curves.png", dpi=180, facecolor="white")
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    allrows, curves, cal_lines = [], [], []
    for folder, model, label, msgs in RUNS:
        d = load(folder, model)
        if d.empty:
            continue
        title = f"{label} ({msgs} messages)"
        print(f"[{title}] n={len(d)}", flush=True)
        m = fit(d)
        e = effects(m, d).assign(run=title, model=model, messages=msgs, converged=m.converged)
        allrows.append(e)
        c = d.groupby(["emotion", "offer_share"]).p_accept_lp.mean().reset_index()
        curves.append((title, c.rename(columns={"offer_share": "offer", "p_accept_lp": "p"}).assign(offer=lambda x: 100 * x.offer)))
        r = d[["p_accept_lp", "accept"]].corr().iloc[0, 1]
        cal_lines += [f"**{title}**: r(P(accept), sampled choice) = {r:.2f}", "", md_table(calibration(d).reset_index()), ""]
    res = pd.concat(allrows, ignore_index=True)
    fam = res.emotion != "none"
    for col, src in (("p_value_holm", "p_value"), ("p_gain_holm", "p_gain")):
        res[col] = np.nan
        res.loc[fam, col] = holm(res.loc[fam, src])
    res.to_csv(OUT / "value_signal.csv", index=False)
    figure(curves)

    def fmt(e, lo, hi, nd=2):
        return f"{e:+.{nd}f} [{lo:+.{nd}f}, {hi:+.{nd}f}]"

    tab = pd.DataFrame(dict(run=res.run, emotion=res.emotion,
                            value_shift_logit=[fmt(r.value_shift, r.value_lo, r.value_hi) for r in res.itertuples()],
                            p_value_holm=res.p_value_holm.round(3),
                            gain_shift=[fmt(r.gain_shift, r.gain_lo, r.gain_hi) for r in res.itertuples()],
                            p_gain_holm=res.p_gain_holm.round(3),
                            indifference_offer_pct=[f"{r.indiff_neutral:.0f} → {r.indiff:.0f}" if r.indiff_identified
                                                    else "not identified" for r in res.itertuples()],
                            indiff_shift_pp=[fmt(r.indiff_shift, r.shift_lo, r.shift_hi, 1) if r.indiff_identified
                                             else "" for r in res.itertuples()]))
    sig = res[fam & (res.p_value_holm < .05)]
    lines = ["# The model's valuation curve: log-probabilities as a value signal (exploratory, post hoc; P18)", "",
             "Each model's probability of answering \"accept\" in the ultimatum game (S1), read from its log-probabilities on "
             "the same prompts and seeds as the choices. Mixed model on logit P(accept) with message and message×paraphrase "
             "random intercepts; t with df = #messages − #emotions; Holm across all emotion×run tests (no-message rows "
             "excluded from the family).",
             "- **value shift**: change in logit P(accept) at a 30% offer vs a neutral message (> 0 = the same offer is more "
             "acceptable).",
             "- **gain shift**: change in the slope on the offer (logit per unit share; > 0 = more sensitive to fairness).",
             "- **indifference offer**: offer at which P(accept) = .5, the MAO analogue (neutral → emotion), and its shift "
             "(parametric bootstrap). Reported only when the neutral curve rises reliably with the offer and both crossings "
             "fall between 0% and 55%; otherwise \"not identified\" (flat or never-crossing curves).", "",
             "![valuation curves](fig_value_curves.png)", "",
             f"**Value shifts surviving Holm ({len(sig)} of {int(fam.sum())}):** " +
             ("; ".join(f"{r.run} {r.emotion} {r.value_shift:+.2f}" for r in sig.itertuples()) or "none"), "",
             md_table(tab), "",
             "## Is the signal valid? Calibration against the sampled choices", "",
             "At T = 1.0 a choice is a draw from the model's distribution, so the accept rate in each P(accept) bin should "
             "match the mean P(accept) if the log-probability reflects the decision.", ""] + cal_lines
    (OUT / "value_signal.md").write_text("\n".join(lines))
    print("\n".join(lines[:14]))


if __name__ == "__main__":
    main()
