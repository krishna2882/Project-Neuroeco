"""Extension 3 (docs/preregistration_extension3.md): does NON-threatening anger still lower trust?

Confirmatory (one-sided, Holm over the three models):
  T1 qwen25_7b, T2 qwen25_14b, T3 llama31_8b: S3b share sent, non-threatening angry message vs neutral, lower.
  Model = P12 stricter model (analysis/message_re.lmm_effects): share ~ emotion + stakes + C(paraphrase)
  + (1 | message) + (1 | message:paraphrase), t with df = #messages - #emotions.
Secondary (fixed in advance, not in the Holm family):
  D  non-threatening minus threatening anger (follow-up FA messages, same neutral messages), Qwen 7B and Llama.
Exploratory: original model; manipulation check (emotion recognition); model threat probe; human ratings.
  python -m analysis.ext3   -> results/ext3/confirmatory.md
"""
import numpy as np
import pandas as pd
from scipy import stats

from analysis.common import fit_mixedlm, holm, load_raw, md_table, tidy_checks, tidy_trials
from analysis.ext2 import wilson
from analysis.message_re import lmm_effects
from analysis.s2s3 import SPECS
from config import RAW_DIR, RESULTS_DIR, STIM_DIR

OUT = RESULTS_DIR / "ext3"
HYP = [("T1", "qwen25_7b"), ("T2", "qwen25_14b"), ("T3", "llama31_8b")]
LABEL = {"qwen25_7b": "Qwen2.5-7B", "qwen25_14b": "Qwen2.5-14B", "llama31_8b": "Llama-3.1-8B"}
MAIN_EST = {"qwen25_7b": -11.08, "qwen25_14b": -16.47, "llama31_8b": -14.26}  # threatening-anger estimates (P12)


def ci(e, lo, hi):
    return f"{e:+.1f} [{lo:+.1f}, {hi:+.1f}]"


def original_model(g):
    d = g[g.sub_exp == "S3b"].copy()
    d["emotion"] = d.emotion.astype(str)
    m = fit_mixedlm(SPECS["S3b"]["formula"], d, d.variant_id)
    k = "C(emotion, Treatment('neutral'))[T.angry]"
    est, se = 100 * m.fe_params[k], 100 * m.bse_fe[k]
    return est, est - 1.96 * se, est + 1.96 * se


def confirmatory(df):
    rows = []
    for hid, m in HYP:
        g = df[df.model_key == m]
        if g.empty:
            rows.append(dict(id=hid, model=LABEL[m], ran=False))
            continue
        r = [x for x in lmm_effects(g, m, "S3b") if x["emotion"] == "angry"][0]
        t = r["est_new"] / r["se_new"]
        lo, hi = r["est_new"] - stats.t.ppf(.975, r["df"]) * r["se_new"], r["est_new"] + stats.t.ppf(.975, r["df"]) * r["se_new"]
        oe, olo, ohi = original_model(g)
        rows.append(dict(id=hid, model=LABEL[m], ran=True, est=r["est_new"], se=r["se_new"], df=r["df"], lo=lo, hi=hi,
                         p_one_sided=stats.t.cdf(t, r["df"]), original=ci(oe, olo, ohi),
                         threatening_anger_est=MAIN_EST[m]))
    c = pd.DataFrame(rows)
    c["p_holm"] = np.nan
    ran = c.ran.fillna(False).astype(bool)
    if ran.any():
        c.loc[ran, "p_holm"] = holm(c.loc[ran, "p_one_sided"])
    out = []
    for r in c.itertuples():
        if not r.ran:
            out.append("not run")
        elif r.p_holm < .05:
            out.append("**Supported**: non-threatening anger lowers trust")
        else:
            q90 = stats.t.ppf(.95, r.df)
            if -5 < r.est - q90 * r.se and r.est + q90 * r.se < 5:
                out.append("Not supported; **equivalent to zero** (90% CI inside ±5 pp)")
            elif r.lo > r.threatening_anger_est:
                out.append("Not supported; reliably smaller than with the original anger messages")
            else:
                out.append("Not supported; inconclusive")
    c["outcome"] = out
    return c


def difference(c):
    """D: (non-threatening - neutral) minus (threatening FA - neutral, follow-up), P12 model, independent samples."""
    fu = pd.read_csv(RESULTS_DIR / "followup" / "message_re.csv")
    rows = []
    for r in c[c.ran.fillna(False).astype(bool)].itertuples():
        m = [k for k, v in LABEL.items() if v == r.model][0]
        f = fu[(fu.model == m) & (fu.test == "S3b sent (pp)") & (fu.emotion == "angry")]
        if f.empty:
            continue
        f = f.iloc[0]
        d, se = r.est - f.est_new, np.hypot(r.se, f.se_new)
        dfw = min(r.df, f.df)
        q = stats.t.ppf(.975, dfw)
        rows.append(dict(model=r.model, nonthreat=round(r.est, 1), threat_followup=round(f.est_new, 1),
                         difference=ci(d, d - q * se, d + q * se), p_two_sided=2 * stats.t.sf(abs(d / se), dfw)))
    return pd.DataFrame(rows)


def checks():
    try:
        ck = tidy_checks("threat_checks", bank="threat_checks")
    except FileNotFoundError:
        return pd.DataFrame()
    ck = ck[ck.emotion == "angry"]
    col = "perceived_emotion" if "perceived_emotion" in ck else "emotion_answer"
    g = ck.groupby("model_key")[col].apply(lambda s: (s == "angry").mean())
    return g.rename("recognised_as_angry").reset_index()


def probe():
    try:
        raw = load_raw("probe_threat", "probe_threat")
    except FileNotFoundError:
        return pd.DataFrame()
    bank = pd.read_json(RAW_DIR.parent / "scenarios" / "probe_threat.jsonl", lines=True, dtype=False)[["trial_id", "set"]]
    ok = raw[raw.status == "ok"].sort_values("attempt").groupby(["model_key", "trial_id"]).head(1).merge(bank, on="trial_id")
    ok["yes"] = ok.answer.astype(str).str.lower().eq("yes")
    rows = []
    for (m, s), g in ok.groupby(["model_key", "set"]):
        lo, hi = wilson(g.yes.sum(), len(g))
        rows.append(dict(model=LABEL.get(m, m), set=s, n=len(g), says_threat=g.yes.mean(), ci_lo=lo, ci_hi=hi))
    return pd.DataFrame(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        df = tidy_trials("threat", bank="threat_trials")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["model_key"])
    c = confirmatory(df)
    c.to_csv(OUT / "confirmatory.csv", index=False)
    show = c[c.ran.fillna(False).astype(bool)].copy()
    if not show.empty:
        show["estimate [95% CI]"] = [ci(r.est, r.lo, r.hi) for r in show.itertuples()]
        show = show[["id", "model", "estimate [95% CI]", "original", "threatening_anger_est", "p_one_sided", "p_holm", "outcome"]].reset_index(drop=True)
    lines = ["# Extension 3: does non-threatening anger lower trust? (pre-registered)", "",
             "Pre-registration: `docs/preregistration_extension3.md`. S3b share sent (pp), non-threatening angry message vs "
             "neutral; primary = message as a random factor (P12); one-sided t, Holm over T1-T3. `threatening_anger_est` = "
             "the earlier estimate for the same model with the original main-study anger messages (P12 model).", "",
             md_table(show) if not show.empty else "No data yet.", ""]
    d = difference(c)
    lines += ["## Secondary (fixed in advance): non-threatening minus threatening anger", "",
              "Threatening = the follow-up anger messages FA2-FA7 (same neutral messages, paraphrases and game). "
              "Negative = non-threatening anger lowers trust *more*.", "",
              md_table(d) if not d.empty else "No data yet.", ""]
    k = checks()
    lines += ["## Manipulation check: are the new messages read as angry? (models)", "",
              md_table(k) if not k.empty else "No data yet.", ""]
    p = probe()
    lines += ["## Exploratory: does the model itself say the message sounds like a threat?", "",
              md_table(p) if not p.empty else "No data yet.", ""]
    hr = STIM_DIR / "rating" / "human_ratings_threat.csv"
    if hr.exists():
        h = pd.read_csv(hr)
        hs = h.assign(rec=h.perceived_emotion == h.intended).groupby(["set", "intended"]).agg(
            raters=("rater", "nunique"), recognition=("rec", "mean"), threat=("threat_or_promise", "mean")).round(2)
        lines += ["## Human ratings of the new form", "", md_table(hs.reset_index()), ""]
    (OUT / "confirmatory.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
