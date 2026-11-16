"""Extension-4 core subset for rate-limited free API models (P24): ~960 decisions + 32 mood probes, small enough for one
day of a 1,000-requests/day free tier. Same trial ids, prompts and seeds as data/scenarios/ext4_trials.jsonl (rows are
selected, never changed), so analysis/ext4.py reads the output unchanged.

  O  8 formats x offers 10/50% x 4 paraphrases x slots none0, N1, A1, S1, sample 0          = 256
  I  6 message sets x 4 messages x 2 games x 2 stakes x 4 paraphrases, sample 0             = 384
  X  S1: 4 states x 4 inductions x 4 paraphrases x offers 10/30%, sample 0 (128);
     S3b: same x INR 100, sample 0 (64)                                                    = 192
  D  S1 offer of 100% and S3b zero multiplier, 12 message slots x 4 paraphrases, sample 0   = 96
  Mood probe: 4 states x 4 inductions x paraphrases 0-1, sample 0                          = 32

  python build_ext4_core.py  -> data/scenarios/ext4core_trials.jsonl, probe_ext4core_mood.jsonl
"""
import pandas as pd

from config import DATA_DIR

SCEN = DATA_DIR / "scenarios"


def main():
    t = pd.read_json(SCEN / "ext4_trials.jsonl", lines=True, dtype=False)
    off = t.offer_share.astype(float).round(2)
    s0 = t["sample"] == 0
    o = (t.module == "O") & s0 & off.isin([0.10, 0.50]) & t.msg_id.isin(["none0", "N1", "A1", "S1"])
    i = (t.module == "I") & s0
    x = (t.module == "X") & s0 & ((t.game_type == "S3b") & (t.stakes == 100) | (t.game_type == "S1") & off.isin([0.10, 0.30]))
    d = (t.module == "D") & s0 & t.cell_id.isin(["D_S1_off100", "D_S3b_zero"])
    core = t[o | i | x | d]
    core.to_json(SCEN / "ext4core_trials.jsonl", orient="records", lines=True)
    p = pd.read_json(SCEN / "probe_ext4_mood.jsonl", lines=True, dtype=False)
    p = p[(p["sample"] == 0) & (p.paraphrase < 2)]
    p.to_json(SCEN / "probe_ext4core_mood.jsonl", orient="records", lines=True)
    print(core.groupby(["module", "game_type"]).size().to_string(), f"\ntotal {len(core)}; mood probes {len(p)}")


if __name__ == "__main__":
    main()
