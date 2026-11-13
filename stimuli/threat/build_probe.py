"""Extension 3 (exploratory): do the models themselves read the messages as threats?
Each item is a trust-game (S3b) prompt with a message, exactly as in the decision trials, but the decision question is
replaced by: "Does Player B's message sound like a threat to you? Answer yes or no."
Messages: main anger (A), follow-up anger (FA), the 5 frozen non-threatening anger messages (NT), follow-up neutral (FN).
Each message x paraphrase x stakes combination that occurs in the S3b decision trials, x 3 samples = 384 items per model.
Run after the threat bank is built:  python stimuli/threat/build_probe.py -> data/scenarios/probe_threat.jsonl
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SCEN = ROOT / "data" / "scenarios"
Q = "Does Player B's message sound like a threat to you? Answer yes or no."
YN = 'Respond with JSON: {"answer": "yes" or "no"}'


def items(bank, emotions, tag):
    d = pd.read_json(SCEN / bank, lines=True, dtype=False)
    d = d[(d.sub_exp == "S3b") & d.emotion.isin(emotions) & ~d.is_baseline & (d["sample"] == 0)]
    d = d.drop_duplicates(["msg_id", "paraphrase", "stakes"])
    return d.assign(set=tag)


def main():
    parts = [items("trials.jsonl", ["angry"], "main_anger"),
             items("followup_trials.jsonl", ["angry"], "followup_anger"),
             items("followup_trials.jsonl", ["neutral"], "followup_neutral"),
             items("threat_trials.jsonl", ["angry"], "nonthreat_anger")]
    rows = []
    for r in pd.concat(parts, ignore_index=True).itertuples():
        head = r.prompt.split("\n\nHow many")[0]
        assert "sent you this message" in head
        for s in range(3):
            tid = f"PROBE|{r.set}|st{r.stakes}|p{r.paraphrase}|{r.msg_id}|s{s}"
            rows.append(dict(trial_id=tid, cell_id=f"PROBE_{r.set}_st{r.stakes}", item="threat", set=r.set,
                             sub_exp="S3b", game_type="S3b", emotion=r.emotion, stakes=r.stakes, paraphrase=r.paraphrase,
                             msg_id=r.msg_id, variant_id=f"PROBE|p{r.paraphrase}|{r.msg_id}", sample=s,
                             is_baseline=False, extension=False, answer_type="yesno", correct="no", json_key="answer",
                             seed=(r.seed + 7919 * (s + 1)) % (2**31), system=r.system, prompt=f"{head}\n\n{Q}\n\n{YN}"))
    df = pd.DataFrame(rows)
    df.to_json(SCEN / "probe_threat.jsonl", orient="records", lines=True)
    print(df.groupby("set").msg_id.nunique().to_dict(), "items", len(df))


if __name__ == "__main__":
    main()
