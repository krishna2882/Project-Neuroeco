"""Temperature robustness (P20, exploratory): every emotion effect at T = 0.7 vs T = 1.0, same prompts and seeds.
Needs results/temp07 (run_all --tag temp07 --checks-tag none --out temp07 --models llama31_8b qwen25_7b, then
forest --out temp07 and message_re --out temp07).
  python -m analysis.temperature   -> results/temp07/compare.md, compare.csv
"""
import numpy as np
import pandas as pd

from analysis.common import md_table
from config import RESULTS_DIR

OUT = RESULTS_DIR / "temp07"
MODELS = ["llama31_8b", "qwen25_7b"]
LABEL = {"llama31_8b": "Llama-3.1-8B", "qwen25_7b": "Qwen2.5-7B"}


def main():
    k = ["model", "test", "emotion"]
    a = pd.read_csv(RESULTS_DIR / "main" / "message_re.csv")
    b = pd.read_csv(OUT / "message_re.csv")
    a, b = a[a.model.isin(MODELS)], b[b.model.isin(MODELS)]
    m = a[k + ["est_new", "lo_new", "hi_new", "p_bh_study"]].merge(
        b[k + ["est_new", "lo_new", "hi_new", "p_bh_study"]], on=k, suffixes=("_t10", "_t07"))
    m = m.dropna(subset=["est_new_t10", "est_new_t07"])
    m["same_sign"] = np.sign(m.est_new_t10) == np.sign(m.est_new_t07)
    m["diff"] = m.est_new_t07 - m.est_new_t10
    m.to_csv(OUT / "compare.csv", index=False)
    r = np.corrcoef(m.est_new_t10, m.est_new_t07)[0, 1]
    tab = m.assign(model=m.model.map(LABEL),
                   **{"T = 1.0": [f"{r.est_new_t10:+.2f} [{r.lo_new_t10:+.2f}, {r.hi_new_t10:+.2f}]" for r in m.itertuples()],
                      "T = 0.7": [f"{r.est_new_t07:+.2f} [{r.lo_new_t07:+.2f}, {r.hi_new_t07:+.2f}]" for r in m.itertuples()]})
    tab = tab[["model", "test", "emotion", "T = 1.0", "T = 0.7", "p_bh_study_t10", "p_bh_study_t07", "same_sign"]].round(3)
    key = m[(m.test == "S3b sent (pp)") & (m.emotion == "angry")]
    lines = ["# Temperature robustness: T = 0.7 vs T = 1.0 (exploratory, P20)", "",
             "Same prompts and seeds; message as a random factor (P12 model) at both temperatures; FDR study-wide within "
             "each run. S1 in log-odds of rejection, S2/S3 in percentage points.", "",
             f"- Effects with the same sign at both temperatures: **{int(m.same_sign.sum())} of {len(m)}**; "
             f"correlation of the estimates r = {r:.2f}; median |difference| {m['diff'].abs().median():.2f}.",
             "- Anger → trust (S3b): " + "; ".join(
                 f"{LABEL[x.model]} {x.est_new_t10:+.1f} pp at 1.0 vs {x.est_new_t07:+.1f} pp "
                 f"[{x.lo_new_t07:+.1f}, {x.hi_new_t07:+.1f}] at 0.7" for x in key.itertuples()), "",
             md_table(tab.reset_index(drop=True)), ""]
    (OUT / "compare.md").write_text("\n".join(lines))
    print("\n".join(lines[:6]))


if __name__ == "__main__":
    main()
