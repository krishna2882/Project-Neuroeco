"""Automated (keyword) coding of Mistral Large 4's reasoning text, by game and emotion condition.

Descriptive and exploratory: regex coding is a first pass, not a substitute for the two-author human coding.
  python -m analysis.thinking
Writes results/main/thinking_codes.csv and thinking.md.
"""
import json
import re

import numpy as np
import pandas as pd

from analysis.common import EMO_ORDER, load_bank, md_table
from config import RAW_DIR, RESULTS_DIR

CODES = {
    "empathy": r"empath|sympath|compassion|kindness|condolen|comfort|console|feel (?:bad|sorry)|heartfelt|cheer (?:them|him|her) up",
    "fairness": r"\bfair|equal(?:ly)?\b|50/50|50-50|\bhalf\b|equit|even split",
    "self_interest": r"self-interest|selfish|maximi[sz]|better than nothing|nash|subgame|purely (?:economic|monetary)|"
                     r"homo economicus|rational(?:ly)? (?:choice|actor|player|decision|agent|self)",
    "strategic_veto": r"\bveto|might reject|could reject|would reject|risk of rejection|retaliat|punish",
    # naming the game ("dictator game") is NOT counted; only reasoning about being studied / what is expected
    "study_awareness": r"\bstudy\b|experiment|researcher|expected (?:answer|response|behaviou?r)|typical (?:human|participant)|"
                       r"participants|behaviou?ral econom",
    "ai_identity": r"as an ai|i(?:'m| am) an ai|ai without|i don't have (?:real )?(?:feelings|emotions|money)",
    "counterpart_emotion": r"\bangry|anger|frustrat|upset|annoy|hostile|\bsad\b|sadness|grie[fv]|mourning|"
                           r"\bhappy\b|excited|joy|celebrat",  # ("loss" excluded: also used for money)
    "appeal_or_irrelevant": r"manipulat|emotional appeal|guilt[- ]trip|trying to (?:influence|get)|irrelevant to the (?:economic|decision)",
}


def main():
    bank = load_bank("trials").set_index("trial_id")
    recs = []
    with open(RAW_DIR / "mistral" / "main.jsonl") as f:
        for line in f:
            r = json.loads(line)
            if r["status"] == "ok" and r.get("thinking"):
                recs.append(r)
    seen, rows = set(), []
    for r in sorted(recs, key=lambda r: r["attempt"]):
        if r["trial_id"] in seen:
            continue
        seen.add(r["trial_id"])
        t = r["thinking"].lower()
        b = bank.loc[r["trial_id"]]
        row = dict(trial_id=r["trial_id"], game_type=b.game_type, emotion=b.emotion, extension=b.extension,
                   share=r.get("share"), decision=r.get("decision"), n_chars=len(t))
        row.update({k: bool(re.search(v, t)) for k, v in CODES.items()})
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(RESULTS_DIR / "main" / "thinking_codes.csv", index=False)

    lines = ["# Mistral Large 4 reasoning text: automated keyword coding (exploratory)", "",
             f"{len(df)} trials with reasoning text (mean {df.n_chars.mean():.0f} characters). Each cell = % of trials whose "
             "reasoning mentions the theme. Keyword coding is a first pass; validate with the human coding.", ""]
    overall = (100 * df[list(CODES)].mean()).round(1).to_frame("% of all trials")
    lines += ["## Overall", "", md_table(overall), ""]
    for code in ["empathy", "study_awareness", "self_interest", "strategic_veto", "appeal_or_irrelevant", "fairness"]:
        t = (100 * df.pivot_table(index="game_type", columns="emotion", values=code, aggfunc="mean")).round(1)
        t = t[[e for e in EMO_ORDER if e in t.columns]]
        lines += [f"## {code} by game x emotion (%)", "", md_table(t), ""]
    # Does mentioning empathy go with giving more? (S2-DG and S3a, sad condition and all)
    for gt in ["S2-DG", "S3a"]:
        g = df[df.game_type == gt]
        m = g.groupby("empathy").share.agg(["mean", "count"]).round(3)
        lines += [f"## {gt}: share given/returned when empathy is mentioned vs not", "", md_table(m), ""]
    g = df[df.game_type == "S1"]
    m = g.groupby("appeal_or_irrelevant").decision.apply(lambda s: (s == "reject").mean()).round(3).to_frame("P(reject)")
    lines += ["## S1: rejection rate when the reasoning frames the message as an emotional appeal / irrelevant vs not", "", md_table(m), ""]
    (RESULTS_DIR / "main" / "thinking.md").write_text("\n".join(lines))
    print("\n".join(lines[:6]))


if __name__ == "__main__":
    main()
