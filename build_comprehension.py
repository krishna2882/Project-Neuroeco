"""Build the extension-2 game-comprehension bank (docs/preregistration_extension2.md, part E2; items C1-C7).

Each item reuses the exact no-message scenario text of the frozen main bank (same 4 paraphrases, same system prompt) and
replaces the final decision question with one comprehension question. 240 items per model:
  C1-C3  S1 responder   x offers {10%, 40%} x stakes {100, 10000} x 4 paraphrases x 3 samples = 144
  C4     S2-UG proposer x stakes x paraphrases x samples = 24     C5 S2-DG proposer = 24
  C6-C7  S3b investor   x stakes x paraphrases x samples = 48

  python build_comprehension.py      -> data/scenarios/comprehension.jsonl
"""
import pandas as pd

from build_scenarios import stable_int
from config import DATA_DIR, MASTER_SEED, N_SAMPLES, TG_MULTIPLIER

SCEN = DATA_DIR / "scenarios"
NUM = 'Respond with JSON: {"answer": <whole number>}'
YN = 'Respond with JSON: {"answer": "yes" or "no"}'


def items(game_type, stakes, offer_share):
    pie = stakes
    if game_type == "S1":
        offer = round(pie * offer_share)
        return [("C1", "If you reject the proposal, how many rupees do you receive?", "number", 0),
                ("C2", "If you accept the proposal, how many rupees do you receive?", "number", offer),
                ("C3", "If you accept the proposal, how many rupees does Player A receive?", "number", pie - offer)]
    if game_type == "S2-UG":
        return [("C4", "If Player B rejects your proposal, how many rupees do you receive?", "number", 0)]
    if game_type == "S2-DG":
        return [("C5", "Can Player B change how the money is divided? Answer yes or no.", "yesno", "no")]
    if game_type == "S3b":
        half = pie // 2
        return [("C6", f"If you send INR {half}, how many rupees does Player B receive?", "number", TG_MULTIPLIER * half),
                ("C7", "Does Player B have to send any money back to you? Answer yes or no.", "yesno", "no")]
    return []


def main():
    bank = pd.read_json(SCEN / "trials.jsonl", lines=True, dtype=False)
    base = bank[bank.is_baseline & bank.game_type.isin(["S1", "S2-UG", "S2-DG", "S3b"])]
    base = base[(base.game_type != "S1") | base.offer_share.isin([0.10, 0.40])]
    # one scenario text per (game, stakes, offer, paraphrase); the no-message text does not depend on msg_id
    base = base.drop_duplicates(["game_type", "stakes", "offer_share", "paraphrase"])
    rows = []
    for r in base.itertuples():
        scenario = r.prompt.split("\n\n")[0]
        off = r.offer_share if r.game_type == "S1" else None
        for item, q, kind, correct in items(r.game_type, r.stakes, off):
            for s in range(N_SAMPLES):
                cell = f"COMP_{item}_{r.game_type}_st{r.stakes}" + (f"_off{round(100 * off)}" if off else "")
                tid = f"{cell}|p{r.paraphrase}|s{s}"
                rows.append(dict(
                    trial_id=tid, cell_id=cell, item=item, sub_exp=r.sub_exp, game_type=r.game_type,
                    stakes=r.stakes, offer_share=off, paraphrase=r.paraphrase, msg_id="none",
                    variant_id=f"COMP|{r.game_type}|p{r.paraphrase}", sample=s, is_baseline=True, extension=False,
                    answer_type=kind, correct=correct, json_key="answer",
                    seed=stable_int(MASTER_SEED, "seed", tid) % (2**31), system=r.system,
                    prompt=f"{scenario}\n\n{q}\n\n{NUM if kind == 'number' else YN}"))
    df = pd.DataFrame(rows)
    df.to_json(SCEN / "comprehension.jsonl", orient="records", lines=True)
    print(df.groupby("item").size().to_dict(), "total", len(df))


if __name__ == "__main__":
    main()
