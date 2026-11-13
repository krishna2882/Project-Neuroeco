"""Qualitative coding of justifications.

  python -m analysis.qualitative sheet   -> results/qual_coding_sheet.csv (10% stratified sample of the
                                            main-study models' justifications; blank columns for coders 1 and 2)
  python -m analysis.qualitative split   -> results/qual_coding/coder1_devansh.xlsx, coder2_krishna.xlsx
                                            (row number + justification only: no model, trial id or condition)
  python -m analysis.qualitative merge   -> copies both coders' answers back into qual_coding_sheet.csv
  python -m analysis.qualitative kappa   -> Cohen's kappa per code (results/qual_coding/kappa.txt) and the
                                            rows the coders disagree on (results/qual_coding/disagreements.csv)
  python -m analysis.qualitative analyze -> final codes (both coders = primary, either = sensitivity) and an
                                            exploratory analysis by model/condition (results/qual_coding/analysis.md)

Codes (binary, 1 = mentioned): emotion (counterpart's feelings/state), fairness (equity, equal split,
deserving), strategy (anticipating the other's response, rejection risk, reciprocity, self-interest).
Definitions and decision rules: results/qual_coding/CODEBOOK.md. Coders work on separate files and do not
compare answers until both are merged.
"""
import sys

import numpy as np
import pandas as pd

from analysis.common import tidy_trials
from config import MASTER_SEED, RESULTS_DIR

CODES = ["emotion", "fairness", "strategy"]
MAIN_MODELS = ["llama31_8b", "qwen25_7b", "mistral"]  # extension-2 models share the `main` tag
SHEET = RESULTS_DIR / "qual_coding_sheet.csv"
QDIR = RESULTS_DIR / "qual_coding"
CODERS = {"coder1": "devansh", "coder2": "krishna"}


def make_sheet(tag="main"):
    df = tidy_trials(tag)
    df = df[df.model_key.isin(MAIN_MODELS)]
    j = df[df.reason.notna() & (df.reason.astype(str).str.len() > 0)]
    sample = (j.groupby(["model_key", "sub_exp", "emotion"], observed=True, group_keys=False)
              .apply(lambda g: g.sample(frac=0.10, random_state=MASTER_SEED) if len(g) >= 10
                     else g.sample(n=min(1, len(g)), random_state=MASTER_SEED)))
    sample = sample.sample(frac=1, random_state=MASTER_SEED)  # blind order
    sheet = sample[["model_key", "trial_id", "reason"]].copy()
    sheet.insert(0, "row_id", range(1, len(sheet) + 1))
    for c in CODES:
        sheet[f"{c}_coder1"] = ""
        sheet[f"{c}_coder2"] = ""
    RESULTS_DIR.mkdir(exist_ok=True)
    sheet.to_csv(SHEET, index=False)
    print(f"{len(sheet)} justifications ({len(sheet) / max(1, len(j)):.1%} of {len(j)}) -> {SHEET}")


def _coder_path(coder):
    return QDIR / f"{coder}_{CODERS[coder]}.xlsx"


def split():
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font
    from openpyxl.worksheet.datavalidation import DataValidation

    sheet = pd.read_csv(SHEET)
    QDIR.mkdir(exist_ok=True)
    for coder in CODERS:
        path = _coder_path(coder)
        if path.exists():
            sys.exit(f"{path} already exists; refusing to overwrite a coder's work")
        wb = Workbook()
        ws = wb.active
        ws.title = "coding"
        ws.append(["row", "justification"] + CODES + ["note"])
        for r in sheet.itertuples():
            ws.append([r.row_id, r.reason, None, None, None, None])
        for cell in ws[1]:
            cell.font = Font(bold=True)
        ws.freeze_panes = "C2"
        widths = {"A": 6, "B": 90, "C": 10, "D": 10, "E": 10, "F": 30}
        for col, w in widths.items():
            ws.column_dimensions[col].width = w
        for row in ws.iter_rows(min_row=2, min_col=2, max_col=2):
            row[0].alignment = Alignment(wrap_text=True, vertical="top")
        dv = DataValidation(type="whole", operator="between", formula1="0", formula2="1",
                            showErrorMessage=True, error="Enter 0 or 1")
        ws.add_data_validation(dv)
        dv.add(f"C2:E{len(sheet) + 1}")
        wb.save(path)
        print(f"{len(sheet)} rows -> {path}")


def merge():
    sheet = pd.read_csv(SHEET)
    problems = []
    for coder in CODERS:
        got = pd.read_excel(_coder_path(coder))
        if list(got["row"]) != list(sheet["row_id"]):
            sys.exit(f"{_coder_path(coder).name}: rows were reordered, added or deleted; restore the original order")
        # A row left blank in all three codes = the coder could not decide: kept as missing and
        # excluded from kappa for that coder pair (counted and reported), never imputed.
        undecided = got[CODES].isna().all(axis=1)
        if undecided.any():
            print(f"{CODERS[coder]}: {int(undecided.sum())} undecided rows kept as missing: "
                  f"{got['row'][undecided].tolist()}")
        for c in CODES:
            raw = got[c]
            vals = pd.to_numeric(raw, errors="coerce")
            # Codebook data-entry rule: a blank cell in a row that has at least one 1 means 0.
            has_one = (got[CODES] == 1).any(axis=1)
            vals = vals.where(~(raw.isna() & has_one), 0)
            bad = got["row"][~vals.isin([0, 1]) & ~undecided].tolist()
            if bad:
                problems.append(f"{CODERS[coder]} / {c}: {len(bad)} rows not 0/1 (first: {bad[:10]})")
            sheet[f"{c}_{coder}"] = vals.values
    if problems:
        print("Not merged. Fix these first:\n  " + "\n  ".join(problems))
        sys.exit(1)
    sheet.to_csv(SHEET, index=False)
    print(f"merged both coders into {SHEET}")


def kappa(a, b):
    a, b = np.asarray(a, int), np.asarray(b, int)
    po = np.mean(a == b)
    pe = np.mean(a) * np.mean(b) + (1 - np.mean(a)) * (1 - np.mean(b))
    return (po - pe) / (1 - pe) if pe < 1 else np.nan


def score(path=None):
    sheet = pd.read_csv(path or SHEET)
    rows, disagree = [], []
    for c in CODES:
        s = sheet[["row_id", "reason", f"{c}_coder1", f"{c}_coder2"]].dropna()
        if len(s):
            a, b = s[f"{c}_coder1"].astype(int), s[f"{c}_coder2"].astype(int)
            rows.append(dict(code=c, n=len(s), agreement=float(np.mean(a == b)), kappa=kappa(a, b),
                             prevalence_c1=a.mean(), prevalence_c2=b.mean()))
            d = s[a != b].rename(columns={f"{c}_coder1": "devansh", f"{c}_coder2": "krishna"})
            disagree.append(d.assign(code=c))
    out = pd.DataFrame(rows)
    print(out.round(3).to_string(index=False))
    if rows:
        QDIR.mkdir(exist_ok=True)
        (QDIR / "kappa.txt").write_text(out.round(3).to_string(index=False) + "\n")
        pd.concat(disagree).to_csv(QDIR / "disagreements.csv", index=False)
        print(f"disagreements -> {QDIR / 'disagreements.csv'}")
    return out


def final_codes(sheet):
    """Consensus codes from the two coders, fixed before any code-by-condition result was seen.
    Primary (conservative): present only if both coders marked it. Sensitivity (liberal): either coder.
    A row either coder left undecided is excluded (NaN)."""
    out = sheet.copy()
    for c in CODES:
        a, b = sheet[f"{c}_coder1"], sheet[f"{c}_coder2"]
        ok = a.notna() & b.notna()
        out[f"{c}_both"] = ((a == 1) & (b == 1)).astype(float).where(ok)
        out[f"{c}_either"] = ((a == 1) | (b == 1)).astype(float).where(ok)
    return out


def _fmt_p(p):
    return "< .001" if p < 0.001 else f"{p:.3f}"


def _wilson(k, n):
    from statsmodels.stats.proportion import proportion_confint
    lo, hi = proportion_confint(k, n, method="wilson") if n else (np.nan, np.nan)
    return f"{k / n:.0%} [{lo:.0%}, {hi:.0%}]" if n else "n/a"


def analyze():
    """Exploratory: code prevalence by model and condition, joined back to the design."""
    from scipy.stats import fisher_exact
    from statsmodels.stats.multitest import multipletests

    sheet = final_codes(pd.read_csv(SHEET))
    t = tidy_trials("main")[["model_key", "trial_id", "sub_exp", "game", "emotion", "decision"]]
    d = sheet.merge(t, on=["model_key", "trial_id"], how="left")
    assert d.sub_exp.notna().all(), "coded rows not found in the design"
    d = d.dropna(subset=[f"{c}_both" for c in CODES])
    d["emotional_msg"] = d.emotion.isin(["angry", "sad", "happy"])
    d.to_csv(QDIR / "final_codes.csv", index=False)

    lines = ["# Qualitative coding: final codes and exploratory analysis", "",
             f"{len(d)} justifications coded by both authors (rows either coder left undecided are excluded).",
             "Inter-rater agreement (before any consensus): see `kappa.txt`.",
             "**Final codes (fixed in advance):** a code is present only if *both* coders marked it (primary);",
             "*either* coder marking it is reported as a sensitivity check. Everything below is exploratory.", ""]

    for ver, label in [("both", "Primary: both coders"), ("either", "Sensitivity: either coder")]:
        lines += [f"## {label}", "", "### Prevalence by model (95% Wilson CI)", "",
                  "| Model | n | emotion | fairness | strategy |", "|---|---|---|---|---|"]
        for m, g in d.groupby("model_key"):
            lines.append(f"| {m} | {len(g)} | " + " | ".join(
                _wilson(int(g[f'{c}_{ver}'].sum()), len(g)) for c in CODES) + " |")
        lines += ["", "### Emotion mentions by message condition", "",
                  "| Model | " + " | ".join(["none", "neutral", "angry", "sad", "happy"]) + " |",
                  "|---|---|---|---|---|---|"]
        for m, g in d.groupby("model_key"):
            cells = []
            for e in ["none", "neutral", "angry", "sad", "happy"]:
                h = g[g.emotion == e]
                cells.append(f"{int(h[f'emotion_{ver}'].sum())}/{len(h)}")
            lines.append(f"| {m} | " + " | ".join(cells) + " |")

        tests = []

        def fisher(name, grp_a, grp_b, code):
            ka, na = int(grp_a[f"{code}_{ver}"].sum()), len(grp_a)
            kb, nb = int(grp_b[f"{code}_{ver}"].sum()), len(grp_b)
            p = fisher_exact([[ka, na - ka], [kb, nb - kb]])[1] if na and nb else np.nan
            tests.append(dict(test=name, a=f"{ka}/{na}", b=f"{kb}/{nb}", p=p))

        for m, g in d.groupby("model_key"):
            fisher(f"{m}: emotion code, emotional msg (a) vs neutral/none (b)",
                   g[g.emotional_msg], g[~g.emotional_msg], "emotion")
        s2 = d[d.sub_exp == "S2"]
        fisher("all models, S2: strategy code, UG (a) vs DG (b)", s2[s2.game == "UG"], s2[s2.game == "DG"], "strategy")
        s1 = d[d.sub_exp == "S1"]
        for m in ["llama31_8b", "qwen25_7b"]:
            g = s1[s1.model_key == m]
            fisher(f"{m}, S1: fairness code, reject (a) vs accept (b)",
                   g[g.decision == "reject"], g[g.decision == "accept"], "fairness")
        tt = pd.DataFrame(tests)
        tt["p_holm"] = multipletests(tt.p, method="holm")[1]
        lines += ["", "### Exploratory tests (Fisher's exact, two-sided; Holm across these 6)", "",
                  "| Test | a | b | p | p (Holm) |", "|---|---|---|---|---|"]
        for r in tt.itertuples():
            lines.append(f"| {r.test} | {r.a} | {r.b} | {_fmt_p(r.p)} | {_fmt_p(r.p_holm)} |")
        lines.append("")

    lines += ["Note: Mistral accepted every S1 offer in this sample, so the fairness-by-decision test is not run for it.",
              "Cells are small (e.g. 11 DG rows per model); treat these results as descriptive."]
    (QDIR / "analysis.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    {"sheet": make_sheet, "split": split, "merge": merge, "kappa": score, "analyze": analyze}[
        sys.argv[1] if len(sys.argv) > 1 else "sheet"]()
