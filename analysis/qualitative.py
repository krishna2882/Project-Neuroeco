"""Qualitative coding of justifications.

  python -m analysis.qualitative sheet   -> results/qual_coding_sheet.csv (10% stratified sample of
                                            justifications; blank columns for coder 1 and coder 2)
  python -m analysis.qualitative kappa   -> Cohen's kappa per code from the filled-in sheet

Codes (binary, 1 = mentioned): emotion (counterpart's feelings/state), fairness (equity, equal split,
deserving), strategy (anticipating the other's response, rejection risk, reciprocity, self-interest).
The sheet hides the condition label so coding is blind to emotion condition.
"""
import sys

import numpy as np
import pandas as pd

from analysis.common import tidy_trials
from config import MASTER_SEED, RESULTS_DIR

CODES = ["emotion", "fairness", "strategy"]


def make_sheet(tag="main"):
    df = tidy_trials(tag)
    j = df[df.reason.notna() & (df.reason.astype(str).str.len() > 0)]
    sample = (j.groupby(["model_key", "sub_exp", "emotion"], observed=True, group_keys=False)
              .apply(lambda g: g.sample(frac=0.10, random_state=MASTER_SEED) if len(g) >= 10
                     else g.sample(n=min(1, len(g)), random_state=MASTER_SEED)))
    sample = sample.sample(frac=1, random_state=MASTER_SEED)  # blind order
    sheet = sample[["model_key", "trial_id", "reason"]].copy()
    for c in CODES:
        sheet[f"{c}_coder1"] = ""
        sheet[f"{c}_coder2"] = ""
    path = RESULTS_DIR / "qual_coding_sheet.csv"
    RESULTS_DIR.mkdir(exist_ok=True)
    sheet.to_csv(path, index=False)
    print(f"{len(sheet)} justifications ({len(sheet) / max(1, len(j)):.1%} of {len(j)}) -> {path}")


def kappa(a, b):
    a, b = np.asarray(a, int), np.asarray(b, int)
    po = np.mean(a == b)
    pe = np.mean(a) * np.mean(b) + (1 - np.mean(a)) * (1 - np.mean(b))
    return (po - pe) / (1 - pe) if pe < 1 else np.nan


def score(path=None):
    sheet = pd.read_csv(path or RESULTS_DIR / "qual_coding_sheet.csv")
    rows = []
    for c in CODES:
        s = sheet[[f"{c}_coder1", f"{c}_coder2"]].dropna()
        if len(s):
            rows.append(dict(code=c, n=len(s), kappa=kappa(s.iloc[:, 0], s.iloc[:, 1]),
                             prevalence_c1=s.iloc[:, 0].mean(), prevalence_c2=s.iloc[:, 1].mean()))
    out = pd.DataFrame(rows)
    print(out.round(3).to_string(index=False))
    return out


if __name__ == "__main__":
    {"sheet": make_sheet, "kappa": score}[sys.argv[1] if len(sys.argv) > 1 else "sheet"]()
