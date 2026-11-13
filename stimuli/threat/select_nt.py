"""Extension 3: freeze the 5 non-threatening anger messages by the pre-registered rule
(docs/preregistration_extension3.md, section 2). Needs stimuli/rating/human_ratings_threat.csv (>= 8 raters).

Eligible: recognised as angry by >= 70% of raters AND read as a threat/promise by < 30%.
Rank: lowest threat share, then highest recognition, then closest to 22 words, then msg_id. Take the top 5.
If fewer than 5 are eligible the study is NOT run (pre-registered stopping rule).

Writes stimuli/threat/messages_frozen.csv: the frozen follow-up set with the angry messages replaced by the 5 selected.
  python stimuli/threat/select_nt.py
"""
import re
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    r = pd.read_csv(ROOT / "stimuli" / "rating" / "human_ratings_threat.csv")
    r = r[r.set == "threat_nt"]
    n_raters = r.rater.nunique()
    per = r.groupby("msg_id").agg(recognition=("perceived_emotion", lambda s: (s == "angry").mean()),
                                  threat=("threat_or_promise", "mean"))
    cand = pd.read_csv(HERE / "candidates_nt.csv").set_index("msg_id")
    per["n_words"] = cand.text.map(lambda t: len(re.findall(r"[A-Za-z']+", t)))
    per["eligible"] = (per.recognition >= 0.70) & (per.threat < 0.30)
    per["len_gap"] = (per.n_words - 22).abs()
    per = per.reset_index().sort_values(["eligible", "threat", "recognition", "len_gap", "msg_id"],
                                        ascending=[False, True, False, True, True])
    print(f"{n_raters} raters\n" + per.round(2).to_string(index=False))
    if n_raters < 8:
        sys.exit("STOP: fewer than 8 raters; collect more ratings before freezing.")
    sel = per[per.eligible].head(5)
    if len(sel) < 5:
        sys.exit(f"STOP: only {len(sel)} eligible messages; by the pre-registered rule extension 3 is not run.")
    fu = pd.read_csv(ROOT / "stimuli" / "followup" / "messages_frozen.csv")
    new = []
    for i, m in enumerate(sorted(sel.msg_id)):
        t = cand.loc[m, "text"]
        new.append(dict(msg_id=m, emotion="angry", variant_idx=i, text=t, n_words=len(re.findall(r"[A-Za-z']+", t)),
                        n_chars=len(t), selection_basis="ext3_rule_low_threat"))
    out = pd.concat([fu[fu.emotion != "angry"], pd.DataFrame(new)], ignore_index=True)
    out.to_csv(HERE / "messages_frozen.csv", index=False)
    per.to_csv(HERE / "selection.csv", index=False)
    print("selected:", sorted(sel.msg_id), "-> stimuli/threat/messages_frozen.csv")


if __name__ == "__main__":
    main()
