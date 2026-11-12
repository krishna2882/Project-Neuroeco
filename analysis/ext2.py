"""Extension 2 analysis, exactly as pre-registered (docs/preregistration_extension2.md, frozen 12 Nov 2026).

  python -m analysis.ext2            # runs run_all / forest / message_re for the Qwen family into results/ext2/,
                                     # then writes results/ext2/confirmatory.md (+ .csv tables)
  python -m analysis.ext2 --skip-fit # only rebuild confirmatory.md from existing results/ext2 files

Confirmatory: X1 (14B), X2 (3B), X3 (7B Q8_0): S3b angry trustee lowers share sent vs neutral; one-sided t from the
stricter model (message as a random factor, P12), Holm over X1-X3; the original model is shown alongside.
Fixed in advance as well: E3 Q8 - Q4 difference with a 95% CI and TOST vs +-10 pp; E2 comprehension accuracy with
Wilson CIs and the 80% / 90% interpretation rule for Llama (C1-C3).
"""
import argparse
import subprocess
import sys

import numpy as np
import pandas as pd
from scipy import stats

from analysis.common import holm, load_raw, md_table
from analysis.equivalence import add_classes
from config import DATA_DIR, RAW_DIR, RESULTS_DIR

OUT = RESULTS_DIR / "ext2"
QWEN = ["qwen25_3b", "qwen25_7b", "qwen25_14b", "qwen25_7b_q8"]
LABEL = {"qwen25_3b": "Qwen2.5-3B", "qwen25_7b": "Qwen2.5-7B (Q4)", "qwen25_14b": "Qwen2.5-14B",
         "qwen25_7b_q8": "Qwen2.5-7B (Q8)", "llama31_8b": "Llama-3.1-8B"}
S3B = "S3b sent (pp)"


def fit_all():
    py = sys.executable
    present = [m for m in QWEN if (RAW_DIR / m / "main.jsonl").exists()]
    for cmd in (["-m", "analysis.run_all", "--tag", "main", "--checks-tag", "checks", "--out", "ext2", "--models", *present],
                ["-m", "analysis.forest", "--out", "ext2"],
                ["-m", "analysis.message_re", "--out", "ext2"]):
        print("+", " ".join(cmd), flush=True)
        subprocess.run([py, *cmd], check=True)


def wilson(k, n, z=1.96):
    if n == 0:
        return np.nan, np.nan
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h


def confirmatory(mre, old):
    rows = []
    for xid, model in [("X1", "qwen25_14b"), ("X2", "qwen25_3b"), ("X3", "qwen25_7b_q8")]:
        r = mre[(mre.model == model) & (mre.test == S3B) & (mre.emotion == "angry")]
        if r.empty:
            rows.append(dict(id=xid, model=LABEL[model], status="not run"))
            continue
        r = r.iloc[0]
        o = old[(old.model == model) & (old.test == S3B) & (old.emotion == "angry")]
        rows.append(dict(id=xid, model=LABEL[model], estimate_pp=r.est_new, ci_lo=r.lo_new, ci_hi=r.hi_new,
                         p_one_sided=stats.t.cdf(r.est_new / r.se_new, r.df), df=r.df,
                         original_model=f"{o.est.iat[0]:+.1f} [{o.lo.iat[0]:+.1f}, {o.hi.iat[0]:+.1f}]" if len(o) else "",
                         se=r.se_new, status="run"))
    c = pd.DataFrame(rows)
    ran = c.status == "run"
    c["p_holm"] = np.nan
    for col in ("estimate_pp", "ci_lo", "ci_hi", "p_one_sided", "df", "se", "original_model"):
        if col not in c:
            c[col] = np.nan
    if ran.any():
        c.loc[ran, "p_holm"] = holm(c.loc[ran, "p_one_sided"])
    q4_main = -11.08  # Qwen2.5-7B Q4, main study, stricter model (results/main/message_re.csv)

    def verdict(r):
        if r.status != "run":
            return "not run"
        if r.p_holm < .05:
            return "**Replicated**"
        tc = stats.t.ppf(.95, r.df)
        lo90, hi90 = r.estimate_pp - tc * r.se, r.estimate_pp + tc * r.se
        if -5 < lo90 and hi90 < 5:
            v = "Not replicated: equivalent to zero (90% CI inside ±5 pp)"
        else:
            v = "Not replicated: inconclusive"
        if r.ci_lo > q4_main:
            v += "; reliably smaller than the 7B-Q4 estimate (CI excludes −11.1 pp)"
        return v
    c["outcome"] = c.apply(verdict, axis=1)
    return c


def q8_vs_q4(mre):
    a = mre[(mre.model == "qwen25_7b_q8") & (mre.test == S3B) & (mre.emotion == "angry")]
    b = mre[(mre.model == "qwen25_7b") & (mre.test == S3B) & (mre.emotion == "angry")]
    if a.empty or b.empty:
        return None
    a, b = a.iloc[0], b.iloc[0]
    d = a.est_new - b.est_new
    se = np.sqrt(a.se_new ** 2 + b.se_new ** 2)  # treated as independent estimates (conservative for paired seeds)
    df = min(a.df, b.df)
    tc95, tc90 = stats.t.ppf(.975, df), stats.t.ppf(.95, df)
    p_tost = max(stats.t.sf((d + 10) / se, df), stats.t.cdf((d - 10) / se, df))
    return dict(q8=a.est_new, q4=b.est_new, diff=d, lo95=d - tc95 * se, hi95=d + tc95 * se,
                lo90=d - tc90 * se, hi90=d + tc90 * se, p_tost=p_tost, equivalent=bool(p_tost < .05))


def agreement():
    """Exploratory: % identical decisions/amounts for Q8 vs Q4 on identical prompts and seeds (first valid attempt)."""
    try:
        raw = load_raw("main", "trials", RAW_DIR)
    except FileNotFoundError:
        return None
    ok = raw[(raw.status == "ok") & raw.model_key.isin(["qwen25_7b", "qwen25_7b_q8"])]
    ok = ok.sort_values("attempt").groupby(["model_key", "trial_id"]).head(1)
    w = ok.pivot_table(index="trial_id", columns="model_key", values="decision", aggfunc="first")
    amt = ok.pivot_table(index="trial_id", columns="model_key", values="amount", aggfunc="first")
    rows = []
    if {"qwen25_7b", "qwen25_7b_q8"} <= set(w.columns):
        s1 = w.dropna()
        rows.append(dict(sub_exp="S1", n=len(s1), identical=(s1.qwen25_7b == s1.qwen25_7b_q8).mean()))
    if {"qwen25_7b", "qwen25_7b_q8"} <= set(amt.columns):
        s3 = amt.dropna()
        rows.append(dict(sub_exp="S3b", n=len(s3), identical=(s3.qwen25_7b == s3.qwen25_7b_q8).mean(),
                         mean_abs_diff=(s3.qwen25_7b - s3.qwen25_7b_q8).abs().mean()))
    return pd.DataFrame(rows)


def comprehension():
    try:
        raw = load_raw("comprehension", "comprehension", RAW_DIR)
    except FileNotFoundError:
        return None, None, None
    bank = pd.read_json(DATA_DIR / "scenarios" / "comprehension.jsonl", lines=True, dtype=False)
    first = raw.sort_values("attempt").groupby(["model_key", "trial_id"]).head(1)  # quality: first attempt
    ok = raw[raw.status == "ok"].sort_values("attempt").groupby(["model_key", "trial_id"]).head(1)
    d = ok.merge(bank[["trial_id", "item", "paraphrase", "stakes"]], on="trial_id")
    rows = []
    for (m, it), g in d.groupby(["model_key", "item"]):
        k, n = int(g.is_correct.sum()), len(g)
        lo, hi = wilson(k, n)
        rows.append(dict(model=LABEL.get(m, m), model_key=m, item=it, n=n, accuracy=k / n, ci_lo=lo, ci_hi=hi,
                         flag="game not reliably understood" if k / n < .80 else ""))
    acc = pd.DataFrame(rows)
    by_para = d.groupby(["model_key", "paraphrase"]).is_correct.mean().unstack()
    qual = first.groupby("model_key").status.apply(lambda s: (s == "ok").mean()).rename("first_attempt_ok")
    return acc, by_para, qual


def llama_rule(acc):
    g = acc[(acc.model_key == "llama31_8b") & acc.item.isin(["C1", "C2", "C3"])]
    if g.empty:
        return "Llama comprehension data not available."
    a = (g.accuracy * g.n).sum() / g.n.sum()
    lo, hi = wilson(round(a * g.n.sum()), g.n.sum())
    if a < .80:
        v = "**misunderstanding**: Llama's flat acceptance curve is attributed to not understanding the payoff rules"
    elif a >= .90:
        v = ("**preference**: Llama understands the payoff rules, so its flat acceptance curve reflects not using "
             "fairness, not a misunderstanding")
    else:
        v = "**inconclusive** (between 80% and 90%)"
    return f"Llama C1-C3 accuracy {a:.1%} [{lo:.1%}, {hi:.1%}] → {v} (rule fixed in the pre-registration)."


def size_trend(mre):
    keep = mre[mre.model.isin(["qwen25_3b", "qwen25_7b", "qwen25_14b"])]
    keep = keep.assign(cell=keep.apply(lambda r: f"{r.est_new:+.2f}" + ("*" if r.p_bh_study < .05 else "")
                                       if r.estimable else "n.e.", axis=1))
    t = keep.pivot_table(index=["test", "emotion"], columns="model", values="cell", aggfunc="first")
    return t[[c for c in ["qwen25_3b", "qwen25_7b", "qwen25_14b"] if c in t.columns]].rename(columns=LABEL)


def recognition():
    rows = []
    for m in QWEN:
        f = OUT / f"checks_confusion_{m}.csv"
        if f.exists():
            cm = pd.read_csv(f, index_col=0)
            rows.append(dict(model=LABEL[m], recognition=np.trace(cm.values) / cm.values.sum(), n=int(cm.values.sum())))
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-fit", action="store_true")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if not args.skip_fit:
        fit_all()
    mre = pd.read_csv(OUT / "message_re.csv")
    old = pd.read_csv(OUT / "all_effects.csv")
    c = confirmatory(mre, old)
    c.to_csv(OUT / "confirmatory.csv", index=False)
    q = q8_vs_q4(mre)
    ag = agreement()
    acc, by_para, qual = comprehension()
    eq = add_classes(mre[mre.estimable == True].rename(columns={"est_new": "est", "se_new": "se"}))  # noqa: E712
    eqc = eq.groupby("model").class_lenient.value_counts().unstack(fill_value=0)

    show = c.copy()
    show["estimate [95% CI]"] = [f"{e:+.1f} [{lo:+.1f}, {hi:+.1f}]" if s == "run" else "" for e, lo, hi, s in
                                 show[["estimate_pp", "ci_lo", "ci_hi", "status"]].values]
    lines = ["# Extension 2: pre-registered results (scale, comprehension, quantisation)", "",
             "Pre-registration: `docs/preregistration_extension2.md` (frozen 12 Nov 2026, approved by both authors before "
             "data collection, SHA-256 dcf5acc4…). Primary model: message as a random factor (P12); one-sided t, Holm "
             "over X1-X3.", "",
             "## Confirmatory: does anger lower trust (S3b) in each new model?", "",
             md_table(show[["id", "model", "estimate [95% CI]", "original_model", "p_one_sided", "p_holm", "outcome"]]
                      .rename(columns={"original_model": "original model [95% CI]"}), floatfmt=4), ""]
    lines += ["## E3: is the anger effect a 4-bit artefact? (fixed in advance; not in the Holm family)", ""]
    if q:
        lines += [f"Q8 {q['q8']:+.1f} pp vs Q4 {q['q4']:+.1f} pp; difference {q['diff']:+.1f} pp "
                  f"[95% CI {q['lo95']:+.1f}, {q['hi95']:+.1f}; 90% CI {q['lo90']:+.1f}, {q['hi90']:+.1f}], "
                  f"TOST vs ±10 pp p = {q['p_tost']:.3f} → "
                  + ("**not a 4-bit artefact** (difference within ±10 pp)" if q["equivalent"]
                     else "**cannot rule out** a quantisation difference of 10 pp"), ""]
    else:
        lines += ["Not available yet.", ""]
    if ag is not None and len(ag):
        lines += ["Exploratory: identical decisions on identical prompts and seeds (Q8 vs Q4):", "", md_table(ag), ""]
    lines += ["## E2: do the models understand the games?", ""]
    if acc is not None:
        lines += [llama_rule(acc), "",
                  md_table(acc.pivot_table(index="item", columns="model", values="accuracy").round(3)), "",
                  "Wilson 95% CIs and flags (< 80% = game not reliably understood):", "",
                  md_table(acc[["model", "item", "n", "accuracy", "ci_lo", "ci_hi", "flag"]], floatfmt=3), "",
                  "First-attempt valid-output rate: " + ", ".join(f"{LABEL.get(k, k)} {v:.1%}" for k, v in qual.items()),
                  "", "Exploratory: accuracy by paraphrase", "", md_table(by_para.round(3)), ""]
    else:
        lines += ["Not available yet.", ""]
    lines += ["## Exploratory: size trend within Qwen (3B → 7B → 14B), stricter model; * = study-wide FDR < .05 in "
              "this analysis", "", md_table(size_trend(mre)), "",
              "## Exploratory: emotion recognition in the manipulation checks", "", md_table(recognition()), "",
              "## Exploratory: equivalence classes (lenient bounds ±10 pp / OR 2)", "", md_table(eqc), "",
              "Full tables: `report.md`, `forest.md`, `message_re.md` in this folder."]
    (OUT / "confirmatory.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
