"""Import the two anonymous rating forms (A and B).

In each form: Responses -> Link to Sheets -> File > Download > CSV. Then:
  python -m analysis.import_ratings formA.csv formB.csv

Writes stimuli/rating/human_ratings.csv (one row per rater x message) and results/peer_rating_summary.md.
These ratings are used ONLY for the pre-specified sensitivity analyses and the human benchmark; they never change the
frozen message sets (stimuli/freeze_messages.py does not read this file).
"""
import re
import sys

import pandas as pd

from analysis.common import EMO_ORDER, md_table
from config import RESULTS_DIR, STIM_DIR

EMO_MAP = {"neutral": "neutral", "angry": "angry", "sad": "sad", "happy": "happy", "something else": "other"}
GIVE_MAP = {"less": -1, "about the same": 0, "more": 1}


def parse(path, key_by_text, key_by_pos, rater_offset):
    resp = pd.read_csv(path)
    rows = []
    for i, r in resp.iterrows():
        rater = f"r{rater_offset + i + 1:03d}"
        threats = {}
        for col in resp.columns:
            m = re.search(r"threat or a promise.*\(page (\d+)\)", col)
            if m:
                ticked = re.findall(r"Message (\d+)", str(r[col]))
                threats[int(m.group(1))] = {int(t) for t in ticked}
        per_msg = {}
        for col in resp.columns:
            m = re.match(r'(.*)\(page (\d+)\)\s*\[(\d+)\. "(.*)"\]\s*$', col, re.S)
            if not m:
                continue
            q, page, num, text = m.group(1).lower(), int(m.group(2)), int(m.group(3)), m.group(4)
            k = key_by_text.get(text.strip())
            if k is None:
                continue
            d = per_msg.setdefault(k.msg_id, dict(rater=rater, form=k.form, msg_id=k.msg_id, set=k.set,
                                                   intended=k.emotion, page=page, number=num))
            val = str(r[col]).strip().lower()
            if "feeling" in q:
                d["perceived_emotion"] = EMO_MAP.get(val)
            elif "less money" in q:
                d["give_effect"] = GIVE_MAP.get(val)
        for d in per_msg.values():
            d["threat_or_promise"] = d["number"] in threats.get(d["page"], set())
            rows.append(d)
    return pd.DataFrame(rows), len(resp)


def main(paths):
    key = pd.read_csv(STIM_DIR / "rating" / "rating_key.csv")
    key_by_text = {t.strip(): r for t, r in zip(key.text, key.itertuples())}
    frames, offset = [], 0
    for p in paths:
        df, n = parse(p, key_by_text, None, offset)
        frames.append(df)
        offset += n
    df = pd.concat(frames, ignore_index=True)
    df.to_csv(STIM_DIR / "rating" / "human_ratings.csv", index=False)

    d = df.assign(hit=df.perceived_emotion == df.intended)
    per = d.groupby(["set", "intended", "msg_id"]).agg(raters=("rater", "nunique"), recognition=("hit", "mean"),
                                                        threat_or_promise=("threat_or_promise", "mean"),
                                                        give_effect=("give_effect", "mean")).round(2)
    per["flag"] = (per.recognition < 0.7) | (per.threat_or_promise >= 0.3)
    bench = d.groupby(["set", "intended"]).agg(recognition=("hit", "mean"), give_effect=("give_effect", "mean"),
                                               less=("give_effect", lambda s: (s == -1).mean()),
                                               more=("give_effect", lambda s: (s == 1).mean())).round(2)
    fl = per[per.flag].reset_index()
    flagged = {s: sorted(fl[fl.set == s].msg_id) for s in ["main", "followup"]}
    lines = ["# Human message ratings", "", f"{df.rater.nunique()} raters (anonymous), {df.msg_id.nunique()} messages.", "",
             "Flag = recognised as the intended emotion by < 70% of raters, or read as a threat/promise by >= 30%.",
             f"**Flagged, main set** (exclude in the main sensitivity analysis): {flagged['main'] or 'none'}",
             f"**Flagged, follow-up set**: {flagged['followup'] or 'none'}", "",
             "## Human benchmark: how each emotion would change people's giving (-1 less, 0 same, +1 more)", "",
             md_table(bench), "", "## Per message", "", md_table(per), ""]
    (RESULTS_DIR / "peer_rating_summary.md").write_text("\n".join(lines))
    print("\n".join(lines[:7]))


if __name__ == "__main__":
    main(sys.argv[1:])
