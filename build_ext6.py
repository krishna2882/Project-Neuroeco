"""Build the prompt bank for extension 6, probing and steering (docs/preregistration_extension6.md). All prompts reuse
the frozen study texts: system prompt, the four paraphrases, the main and follow-up messages and the mood inductions.

Every row is one prompt, run through the model's chat template with the start of the JSON answer pre-filled
(`{"send": ` or `{"decision": "`), so the last position is where the model produces its decision.

  set = msg     Player's message present: 4 emotions x 10 messages (5 main-study, 5 event-free follow-up) x 4 paraphrases
                x [S3b investor at INR 100; S1 responder, offer 30%, both option orders]                      = 480
  set = mood    incidental mood in the system prompt, no message: 8 calm + 8 angry (extension 5) + 4 sad + 4 happy
                (extension 4) inductions x 4 paraphrases x the same three prompts                              = 288
  set = target  no message, no mood (steering targets): S3b x 4 paraphrases x INR 100 / 10,000 (8);
                S1 x 4 paraphrases x offers 10% / 30% x both option orders (16)                               = 24
  split: main-study messages = "train" (the steering direction is estimated from these only); follow-up messages = "test"
         (the ablation test uses these only).

  python build_ext6.py  -> data/scenarios/ext6_prompts.jsonl
"""
from itertools import product

import pandas as pd

from build_ext4 import s1_fields
from config import DATA_DIR, STIM_DIR
from stimuli.ext4.templates import system_with_mood
from stimuli.paraphrases import SYSTEM_PROMPT, render

SCEN = DATA_DIR / "scenarios"
ORDERS = [("accept", "reject"), ("reject", "accept")]
PREFILL = {"S3b": '{"send": ', "S1": '{"decision": "'}


def s3b(p, stakes, text):
    f = dict(pie=stakes, endow=stakes, offer=0, keep=0, sent=0, kept=0, received=0, opt1="", opt2="")
    return render("S3b", p, f, text, False)


def variants(p, text, s3b_stakes=(100,), s1_offers=(0.30,)):
    """(game, stakes, offer, first, prompt) for one paraphrase and message."""
    out = [("S3b", st, None, None, s3b(p, st, text)) for st in s3b_stakes]
    for off, o in product(s1_offers, ORDERS):
        out.append(("S1", 100, off, o[0], render("S1", p, s1_fields(100, off, *o), text, False)))
    return out


def main():
    rows = []

    def add(set_, emotion, source_id, split, p, system, v):
        game, stakes, off, first, prompt = v
        pid = f"EXT6|{set_}|{game}|{source_id}|p{p}|st{stakes}|off{'' if off is None else round(off * 100)}|{first or ''}"
        rows.append(dict(prompt_id=pid, set=set_, game=game, emotion=emotion, source_id=source_id, split=split,
                         paraphrase=p, stakes=stakes, offer_share=off, first=first, max_amount=stakes,
                         system=system, prompt=prompt, prefill=PREFILL[game]))

    msgs = pd.concat([pd.read_csv(STIM_DIR / "messages_frozen.csv").assign(split="train"),
                      pd.read_csv(STIM_DIR / "followup" / "messages_frozen.csv").assign(split="test")])
    for m, p in product(msgs.itertuples(), range(4)):
        for v in variants(p, m.text):
            add("msg", m.emotion, m.msg_id, m.split, p, SYSTEM_PROMPT, v)

    ind = pd.concat([pd.read_csv(STIM_DIR / "ext5" / "inductions.csv"),
                     pd.read_csv(STIM_DIR / "ext4" / "inductions.csv").query("state in ['sad', 'happy']")])
    for i, p in product(ind.itertuples(), range(4)):
        for v in variants(p, None):
            add("mood", i.state, i.induction_id, "mood", p, system_with_mood(i.text), v)

    for p in range(4):
        for v in variants(p, None, s3b_stakes=(100, 10_000), s1_offers=(0.10, 0.30)):
            add("target", "none", "none", "target", p, SYSTEM_PROMPT, v)

    t = pd.DataFrame(rows)
    assert t.prompt_id.is_unique
    t.to_json(SCEN / "ext6_prompts.jsonl", orient="records", lines=True)
    print(t.groupby(["set", "game"]).size().to_string(), f"\ntotal {len(t)}")
    print(t.groupby(["set", "emotion"]).source_id.nunique().to_string())


if __name__ == "__main__":
    main()
