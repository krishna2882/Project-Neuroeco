"""Every planned emotion-vs-neutral effect, for every model and sub-experiment, in one table and one forest plot,
with multiplicity correction across the WHOLE study (not only within a sub-experiment).

Inputs are the CSVs written by analysis/run_all.py (results/<out>/).
  python -m analysis.forest [--out main]
Writes results/<out>/all_effects.csv, fig_forest.png and forest.md.
"""
import argparse

import matplotlib
import numpy as np
import pandas as pd
from scipy import stats

from analysis.common import holm, md_table
from config import RESULTS_DIR

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

EMOS = ["angry", "sad", "happy"]
MODELS = ["llama31_8b", "qwen25_7b", "mistral"]  # default order; collect() also picks up any other model in <out>
LABEL = {"llama31_8b": "Llama-3.1-8B", "qwen25_7b": "Qwen2.5-7B", "mistral": "Mistral Large 4",
         "qwen25_3b": "Qwen2.5-3B", "qwen25_14b": "Qwen2.5-14B", "qwen25_7b_q8": "Qwen2.5-7B (8-bit)"}


def models_in(out):
    found = {f.stem.split("_", 2)[-1] for f in out.glob("s1_glmm_*.csv")} | \
            {f.stem.split("_contrasts_")[-1] for f in out.glob("*_contrasts_*.csv")}
    return [m for m in MODELS if m in found] + sorted(found - set(MODELS))
COLORS = {"angry": "#d62728", "sad": "#9467bd", "happy": "#2ca02c"}


def bh(p):
    p = np.asarray(p, float)
    n = len(p)
    order = np.argsort(p)
    adj = np.empty(n)
    prev = 1.0
    for rank in range(n - 1, -1, -1):
        i = order[rank]
        prev = min(prev, p[i] * n / (rank + 1))
        adj[i] = prev
    return adj


def collect(out):
    rows = []
    for m in models_in(out):
        p = out / f"s1_glmm_{m}.csv"
        if p.exists():
            g = pd.read_csv(p, index_col=0)
            for e in EMOS:
                k = f"C(emotion, Treatment('neutral'))[T.{e}]"
                if k in g.index:
                    r = g.loc[k]
                    estimable = r.se < 5  # ceiling/separation gives huge SEs (Mistral)
                    rows.append(dict(model=m, test="S1 rejection (log-OR)", scale="logOR", emotion=e,
                                     est=r.coef, lo=r.coef - 1.96 * r.se, hi=r.coef + 1.96 * r.se,
                                     p=r.p if estimable else np.nan, estimable=estimable))
        for sub, name in [("s2", "S2 giving"), ("s3a", "S3a returned"), ("s3b", "S3b sent")]:
            p = out / f"{sub}_contrasts_{m}.csv"
            if not p.exists():
                continue
            c = pd.read_csv(p)
            c = c[c.planned]
            for r in c.itertuples():
                e = r.contrast.split(" ")[0]
                label = f"{name} ({r.stratum})" if sub == "s2" else name
                rows.append(dict(model=m, test=f"{label} (pp)", scale="pp", emotion=e, est=r.diff_pp,
                                 lo=r.ci_lo_pp, hi=r.ci_hi_pp, p=r.p, estimable=True))
    df = pd.DataFrame(rows)
    ok = df.p.notna()
    df["p_holm_study"] = np.nan
    df["p_bh_study"] = np.nan
    df.loc[ok, "p_holm_study"] = holm(df.loc[ok, "p"])
    df.loc[ok, "p_bh_study"] = bh(df.loc[ok, "p"])
    return df


def plot(df, path):
    tests = list(dict.fromkeys(df.test))
    models = list(dict.fromkeys(df.model))
    fig, axes = plt.subplots(1, len(models), figsize=(13, 0.55 * len(tests) * 3 / 2 + 1.5), sharey=True)
    ypos = {t: i for i, t in enumerate(tests[::-1])}
    axes = np.atleast_1d(axes)
    for ax, m in zip(axes, models):
        sub = df[df.model == m]
        for j, e in enumerate(EMOS):
            s = sub[sub.emotion == e]
            for r in s.itertuples():
                y = ypos[r.test] + (j - 1) * 0.22
                if not r.estimable:
                    ax.text(0, y, "n.e.", fontsize=6, color=COLORS[e], va="center", ha="center")
                    continue
                # put pp and log-OR on one axis by scaling log-OR x10 (labelled)
                k = 10 if r.scale == "logOR" else 1
                filled = r.p_holm_study < 0.05
                ax.errorbar(r.est * k, y, xerr=[[(r.est - r.lo) * k], [(r.hi - r.est) * k]], fmt="o",
                            color=COLORS[e], mfc=COLORS[e] if filled else "white", ms=5, lw=1, capsize=2,
                            label=e if r.Index == s.index[0] and ax is axes[0] else None)
        ax.axvline(0, color="k", lw=0.8)
        ax.set_title(LABEL.get(m, m), fontsize=10)
        ax.set_xlabel("effect vs neutral message\n(pp; S1 row = log-odds ×10)", fontsize=8)
    axes[0].set_yticks(list(ypos.values()), list(ypos.keys()), fontsize=8)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, frameon=False, fontsize=8, loc="lower center", ncol=3)
    fig.suptitle("All planned emotion effects (filled = significant after Holm correction across the whole study; "
                 "n.e. = not estimable, ceiling)", fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, dpi=160)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="main")
    out = RESULTS_DIR / ap.parse_args().out
    df = collect(out)
    df.to_csv(out / "all_effects.csv", index=False)
    plot(df, out / "fig_forest.png")
    sig_h = df[df.p_holm_study < 0.05]
    sig_b = df[(df.p_bh_study < 0.05) & ~(df.p_holm_study < 0.05)]
    n = int(df.p.notna().sum())
    lines = ["# All planned emotion effects, corrected across the whole study", "",
             f"{n} estimable planned emotion-vs-neutral tests (3 emotions x sub-experiments x models). "
             f"{len(sig_h)} survive Holm (family-wise, whole study); {len(sig_h) + len(sig_b)} survive "
             "Benjamini-Hochberg FDR 5%.", "", "## Survive Holm across the whole study", "",
             md_table(sig_h[["model", "test", "emotion", "est", "lo", "hi", "p", "p_holm_study"]].round(4)), ""]
    if len(sig_b):
        lines += ["## Additionally survive FDR (not Holm)", "",
                  md_table(sig_b[["model", "test", "emotion", "est", "lo", "hi", "p", "p_bh_study"]].round(4)), ""]
    # Direction consistency across models
    piv = df[df.estimable].assign(sign=lambda x: np.sign(x.est).where(x.p_bh_study < 0.05, 0)).pivot_table(
        index=["test", "emotion"], columns="model", values="sign")
    lines += ["## Direction of FDR-significant effects by model (+1 up, -1 down, 0 n.s.)", "",
              md_table(piv.fillna(np.nan)), ""]
    (out / "forest.md").write_text("\n".join(lines))
    print("\n".join(lines[:4]))


if __name__ == "__main__":
    main()
