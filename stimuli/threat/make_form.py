"""Build the rating form for extension 3 (non-threatening anger): 8 new anger candidates + 12 already-rated anchors.
Writes stimuli/threat/create_form_threat.gs (paste into script.google.com, run createForm) and
stimuli/threat/rating_key_threat.csv (used by: python -m analysis.import_ratings --key ... --name threat <csv>).
Same questions, wording and layout as the 13 Nov form, so the threat ratings are directly comparable.
"""
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ANCHORS = ["FA2", "FA3", "FA6", "FN2", "FN5", "FN8", "FS1", "FS4", "FS7", "FH1", "FH5", "FH6"]


def main():
    nt = pd.read_csv(HERE / "candidates_nt.csv").assign(set="threat_nt")
    fu = pd.read_csv(ROOT / "stimuli" / "followup" / "messages_candidates.csv")
    anc = fu[fu.msg_id.isin(ANCHORS)].assign(set="anchor")
    msgs = pd.concat([nt, anc], ignore_index=True)
    rng = np.random.default_rng(20261114)
    msgs = msgs.iloc[rng.permutation(len(msgs))].reset_index(drop=True)
    msgs["page"] = msgs.index // 5 + 1
    msgs["number"] = msgs.index % 5 + 1
    msgs.insert(0, "form", "T")
    msgs[["form", "page", "number", "msg_id", "set", "emotion", "text"]].to_csv(HERE / "rating_key_threat.csv", index=False)
    pages = [dict(page=int(p), items=[dict(n=int(r.number), text=r.text) for r in g.itertuples()])
             for p, g in msgs.groupby("page")]
    src = (ROOT / "stimuli" / "rating" / "create_form_single.gs").read_text()
    logic = src[src.index("var INTRO ="):]
    logic = logic.replace("about 10 minutes", "about 5 minutes")
    header = ("/**\n * Project Neuroeco, extension 3 - ONE anonymous rating form, 20 messages (~5 minutes). Send to ~8-10 people\n"
              " * who did not do the 13 Nov form if possible. Same steps as before: script.google.com -> New project ->\n"
              " * paste -> Save -> run createForm -> Execution log shows the links. No names or emails are collected.\n */\n")
    (HERE / "create_form_threat.gs").write_text(header + "var PAGES = " + json.dumps(pages, indent=1) + ";\n\n" + logic)
    print(msgs.groupby(["set", "emotion"]).size().to_string())


if __name__ == "__main__":
    main()
