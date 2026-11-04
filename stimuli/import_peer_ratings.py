"""Convert the Google Form responses CSV (Responses > Download CSV) into stimuli/peer_ratings.csv.

  .venv/bin/python stimuli/import_peer_ratings.py ~/Downloads/"Rating short messages.csv"
"""
import re
import sys
from pathlib import Path

import pandas as pd

raw = pd.read_csv(sys.argv[1])
codes = dict(pd.read_csv(Path(__file__).parent / "peer_form_codes.csv").values)  # M01 -> real msg_id
init = next(c for c in raw.columns if "initials" in c.lower())
rows = []
for i, r in raw.iterrows():
    for col in raw.columns:
        m = re.match(r"\[(\w+)\] Which emotion", col)
        if not m:
            continue
        mid = m.group(1)
        inten = next(c for c in raw.columns if c.startswith(f"[{mid}] How strongly"))
        intent = next(c for c in raw.columns if c.startswith(f"[{mid}] Does the message"))
        rows.append(dict(rater=f"{r[init]}_{i}", msg_id=codes[mid], perceived_emotion=str(r[col]).lower(),
                         intensity=r[inten], implies_intent=str(r[intent]).lower()))
out = Path(__file__).parent / "peer_ratings.csv"
pd.DataFrame(rows).to_csv(out, index=False)
print(f"{raw.shape[0]} raters x {len(rows) // max(1, raw.shape[0])} messages -> {out}")
