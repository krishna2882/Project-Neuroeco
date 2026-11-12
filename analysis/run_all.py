"""Run every analysis and write results/<outname>/report.md plus tables and figures.

  python -m analysis.run_all                      # real data: data/raw/*/main.jsonl + checks.jsonl
  python -m analysis.run_all --tag pilot --checks-tag none --out pilot
  python -m analysis.run_all --raw-dir data/sim/raw --out sim   # simulated data (validation)
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import patsy

from analysis import checks, robustness, s1, s2s3
from analysis.common import fit_mixedlm, load_raw, md_table, quality_table, tidy_checks, tidy_trials
from analysis.glmm import fit_glmm
from config import RAW_DIR, RESULTS_DIR

# Human meta-analytic benchmarks quoted in the approach paper
HUMAN = [
    ("UG proposer offer (share of pie)", "S2", "UG", 0.40, "Oosterbeek et al., 2004"),
    ("DG giving (share of pie)", "S2", "DG", 0.28, "Engel, 2011"),
    ("TG share of endowment sent", "S3b", None, 0.50, "Johnson & Mislin, 2011"),
    ("TG share of tripled amount returned", "S3a", None, 0.37, "Johnson & Mislin, 2011"),
]


def human_comparison(df):
    rows = []
    base = df[df.emotion.astype(str) == "none"]
    for model, g in base.groupby("model_key"):
        for label, sub, game, human, src in HUMAN:
            s = g[(g.sub_exp == sub) & ((g.game == game) if game else True)].share
            if len(s):
                rows.append(dict(model=model, measure=label, llm_mean=s.mean(), llm_sd=s.std(), n=len(s),
                                 human=human, source=src))
        s1b = g[g.sub_exp == "S1"]
        if len(s1b):
            rows.append(dict(model=model, measure="UG rejection rate (all grid offers; human ~16% at typical offers)",
                             llm_mean=s1b.reject.mean(), llm_sd=np.nan, n=len(s1b), human=0.16,
                             source="Oosterbeek et al., 2004"))
    return pd.DataFrame(rows)


def h5_pooled(df):
    """Emotion x Model interaction (model as fixed factor)."""
    lines = ["## H5: cross-model robustness (Emotion x Model)", ""]
    if df.model_key.nunique() < 2:
        return "\n".join(lines + ["Only one model has data; H5 not testable yet.", ""])
    d = df[df.sub_exp == "S1"].copy()
    d["emotion"] = d.emotion.astype(str)
    d["offer_c"] = d.offer_share - 0.3
    if d.reject.nunique() == 2:
        f = "C(emotion, Treatment('neutral')) * C(model_key) + offer_c * stakes_c * C(model_key)"
        X = patsy.dmatrix(f, d, return_type="dataframe")
        r = fit_glmm(X, d.reject.values, (d.model_key + "|" + d.variant_id).values)
        terms = [c for c in X.columns if c.startswith("C(emotion") and "model_key" in c]
        chi, k, p = r.wald(terms)
        lines.append(f"- S1 GLMM, Emotion x Model on rejection: chi2({k})={chi:.2f}, p={p:.4g}")
    for sub, extra in [("S2", " * C(game)"), ("S3a", " + sent_share"), ("S3b", "")]:
        g = df[df.sub_exp == sub].copy()
        if g.empty:
            continue
        g["emotion"] = g.emotion.astype(str)
        f = f"share ~ C(emotion, Treatment('neutral')) * C(model_key){extra} + stakes_c"
        m = fit_mixedlm(f, g, g.model_key + "|" + g.variant_id)
        terms = [n for n in m.params.index if n.startswith("C(emotion") and "model_key" in n and n.count(":") == 1]
        if terms:
            R = np.array([[1.0 if n == t else 0.0 for n in m.params.index] for t in terms])
            w = m.wald_test(R, scalar=True)
            lines.append(f"- {sub} LMM, Emotion x Model on share: chi2({len(terms)})={float(w.statistic):.2f}, "
                         f"p={float(w.pvalue):.4g}")
    return "\n".join(lines + [""])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="main")
    ap.add_argument("--checks-tag", default="checks")
    ap.add_argument("--raw-dir", default=str(RAW_DIR))
    ap.add_argument("--out", default="main")
    ap.add_argument("--n-boot", type=int, default=500)
    ap.add_argument("--bank-prefix", default="", help="e.g. 'followup' to analyse followup_trials / followup_checks")
    ap.add_argument("--models", nargs="*", default=[], help="restrict to these model keys")
    ap.add_argument("--exclude-msgs", nargs="*", default=[], help="sensitivity analysis: drop these message ids")
    args = ap.parse_args()
    raw_dir = Path(args.raw_dir)
    out = RESULTS_DIR / args.out
    out.mkdir(parents=True, exist_ok=True)

    tb = f"{args.bank_prefix}_trials" if args.bank_prefix else "trials"
    cb = f"{args.bank_prefix}_checks" if args.bank_prefix else "checks"
    raw = load_raw(args.tag, tb, raw_dir)
    df = tidy_trials(args.tag, raw_dir, bank=tb)
    if args.models:
        raw = raw[raw.model_key.isin(args.models)]
        df = df[df.model_key.isin(args.models)]
    if args.exclude_msgs:
        df = df[~df.msg_id.isin(args.exclude_msgs)]
    rep = [f"# Results ({args.out})", "",
           (f"**Sensitivity analysis: messages excluded: {', '.join(args.exclude_msgs)}**\n" if args.exclude_msgs else ""),
           "Generated by `python -m analysis.run_all`. Model versions: "
           + "; ".join(sorted(df.model_version.dropna().unique())), "",
           "## Data quality (first attempt; refusals/off-format are re-asked up to 3x, all attempts logged)", "",
           md_table(quality_table(raw, tb)), ""]
    df.to_csv(out / "tidy_trials.csv", index=False)

    for model, g in df.groupby("model_key"):
        txt, _ = s1.run(g, out, model, n_boot=args.n_boot)
        rep.append(txt)
        txt, _ = s2s3.run(g, out, model)
        rep.append(txt)

    rep += [h5_pooled(df)]
    if args.tag == "main" and not args.bank_prefix:
        rep += [robustness.run(raw_dir)]
    hc = human_comparison(df)
    if len(hc):
        hc.to_csv(out / "human_comparison.csv", index=False)
        rep += ["## Baseline (no-message) behaviour vs human meta-analytic benchmarks", "",
                md_table(hc), "", "Comparisons are of broad pattern only, not equality of effect sizes.", ""]

    if args.checks_tag != "none":
        try:
            ck = tidy_checks(args.checks_tag, raw_dir, bank=cb)
            ck = ck[~ck.msg_id.isin(args.exclude_msgs)]
            if args.models:
                ck = ck[ck.model_key.isin(args.models)]
            for model, g in ck.groupby("model_key"):
                txt, _ = checks.run(g, out, model)
                rep.append(txt)
        except FileNotFoundError:
            rep.append("_No manipulation-check data found._")

    (out / "report.md").write_text("\n\n".join(rep))
    print(f"report -> {out / 'report.md'}")


if __name__ == "__main__":
    main()
