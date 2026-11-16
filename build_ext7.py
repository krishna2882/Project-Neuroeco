"""Build the extension-7 bank, module N: what kind of effect is the incidental angry mood?
(docs/preregistration_extension7.md). The generalisation part of extension 7 reuses the frozen extension-4 and
extension-5 banks unchanged; only module N is new.

One background paragraph is appended to the system prompt exactly as in extensions 4 and 5 (no partner message):
  calm          the 8 calm paragraphs of extension 5 (C1-C8)
  full          the 8 angry paragraphs of extension 5: an unrelated event + "You are still furious about it."
  event_only    the same event, without the sentence that states the feeling (the model has to infer it)
  label_only    the feeling without any event ("Right now, for no particular reason, you are furious.")
  other_person  the same event and feeling, but they happened to a character in a story the participant read
  mild          the same event + "You are slightly annoyed about it."
6 conditions x 8 items x 4 paraphrases x S1 offers 10/30% x both option orders x 2 samples = 1,536 decisions per model.
Mood probe ("how do you feel right now?"): 48 items x paraphrases 0-1 = 96.

  python build_ext7.py  -> data/scenarios/ext7_trials.jsonl, probe_ext7_mood.jsonl
"""
from itertools import product

import numpy as np
import pandas as pd

from build_ext4 import base_row, head, s1_fields
from build_scenarios import stable_int
from config import DATA_DIR, JUSTIFICATION_RATE, MASTER_SEED, STIM_DIR
from stimuli.ext4.templates import MOOD_FMT, MOOD_Q, option_map_json, system_with_mood
from stimuli.paraphrases import render

SCEN = DATA_DIR / "scenarios"
OFFERS = [0.10, 0.30]
ORDERS = [("accept", "reject"), ("reject", "accept")]


def items():
    return list(pd.read_csv(STIM_DIR / "ext7" / "inductions.csv").itertuples())


def trials():
    rows = []
    for i, p, off, o, s in product(items(), range(4), OFFERS, range(2), range(2)):
        opts = ORDERS[o]
        cell = f"N_S1_{i.condition}_off{round(off * 100):02d}"
        tid = f"EXT7|{cell}|p{p}|{i.item_id}|{opts[0][0]}{s}"
        justify = bool(np.random.default_rng(stable_int(MASTER_SEED, tid)).random() < JUSTIFICATION_RATE)
        r = base_row(tid, "N", cell, "S1", "S1", i.condition, 100, p, "none0", s, cond=i.condition, fmt="word",
                     first=opts[0], msg_set=None, state=i.condition, induction_id=i.item_id,
                     prompt=render("S1", p, s1_fields(100, off, *opts), None, justify))
        r.update(offer_share=off, option_order="/".join(opts), option_map=option_map_json({o: o for o in opts}),
                 justify=justify, system=system_with_mood(i.text), is_baseline=False, event_id=i.event_id)
        rows.append(r)
    return rows


def mood_probe():
    rows = []
    for i, p in product(items(), range(2)):
        tid = f"PROBE7|mood|p{p}|{i.item_id}"
        rng = np.random.default_rng(stable_int(MASTER_SEED, tid))
        opts = ["calm", "angry", "sad", "happy"]
        rng.shuffle(opts)
        alts = " or ".join(f'"{o}"' for o in opts)
        prompt = (head(render("S1", p, s1_fields(100, 0.30), None, False)) + "\n\n"
                  + MOOD_Q.format(opts=", ".join(opts)) + "\n\n" + MOOD_FMT.format(alts=alts))
        rows.append(dict(trial_id=tid, cell_id=f"PROBE7_{i.condition}", item="mood", sub_exp="S1", game_type="S1",
                         emotion=i.condition, state=i.condition, induction_id=i.item_id, event_id=i.event_id, stakes=100,
                         paraphrase=p, msg_id="none0", variant_id=f"PROBE7|p{p}|{i.item_id}", sample=0, is_baseline=False,
                         extension=False, answer_type="choice", options="/".join(opts),
                         correct="calm" if i.condition == "calm" else "angry", json_key="answer",
                         seed=stable_int(MASTER_SEED, "seed", tid) % (2**31), system=system_with_mood(i.text),
                         prompt=prompt))
    return rows


def main():
    t = pd.DataFrame(trials())
    assert t.trial_id.is_unique
    t.to_json(SCEN / "ext7_trials.jsonl", orient="records", lines=True)
    pr = pd.DataFrame(mood_probe())
    pr.to_json(SCEN / "probe_ext7_mood.jsonl", orient="records", lines=True)
    print(t.groupby("cond").size().to_string())
    print(f"total trials/model: {len(t)}; justification requested: {t.justify.mean():.1%}; mood probe: {len(pr)}")


if __name__ == "__main__":
    main()
