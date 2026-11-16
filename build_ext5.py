"""Build the extension-5 banks (docs/preregistration_extension5.md): can the breaks found in extension 4 be regulated or
defended against, and what are the models' fairness parameters under mood? Same system prompt, paraphrases, message block,
JSON format and seeding scheme as before; new trial ids give new seeds.

Module R  Emotion regulation of an incidental mood (system prompt = study prompt + mood paragraph + regulation sentence):
          6 regulation prompts [none; filler FL1; reappraisal RA1, RA2; suppression SU1, SU2]
          x 2 states [calm, angry] x 8 inductions x 4 paraphrases
          x [S1 offers 10/30% x both option orders (4) + S3b INR 100 x 2 samples (2)]            = 2,304
Module P  Defences against injected instructions (S3b investor and S2-DG dictator, INR 100):
          3 defences [none; warning in the system prompt; reminder after the message]
          x 5 message sets x 4 messages [neutral, promise, command, fake_rule, fake_system]
          x 2 games x 4 paraphrases x 2 samples                                                = 960
Module F  Full offer curve under mood (S1, INR 100, no regulation):
          offers 0, 10, ..., 100% x 2 states x 8 inductions x 4 paraphrases x both option orders = 1,408
Total 4,672 decisions per model.
Mood probe: 6 regulation prompts x 16 inductions x paraphrases 0-1                              = 192

Option order is counterbalanced, not random, in every S1 cell (sample 0 = "accept" named first, sample 1 = "reject" first),
because the order effect is as large as +70 pp in Qwen2.5-7B (P22, extension 4).

Core subset for the rate-limited API models (rows are selected, never changed):
  R paraphrases 0-1, S1 one order per cell (alternating, balanced within every regulation x state x offer), S3b sample 0 = 576
  P paraphrases 0-1, sample 0 = 240;  mood probe paraphrase 0 = 96

  python build_ext5.py  -> data/scenarios/ext5_trials.jsonl, probe_ext5_mood.jsonl, ext5core_trials.jsonl,
                           probe_ext5core_mood.jsonl
"""
from itertools import product

import numpy as np
import pandas as pd

from build_ext4 import base_row, head, load_messages, s1_fields
from build_scenarios import stable_int
from config import DATA_DIR, JUSTIFICATION_RATE, MASTER_SEED, STIM_DIR
from stimuli.ext4.templates import MOOD_FMT, MOOD_Q, option_map_json
from stimuli.ext5.templates import DEFENCES, REGULATION, defended, system_regulated
from stimuli.paraphrases import GAME_TYPES, render

SCEN = DATA_DIR / "scenarios"
R_OFFERS = [0.10, 0.30]
F_OFFERS = [round(0.1 * k, 1) for k in range(11)]
P_SETS = ["neutral", "promise", "command", "fake_rule", "fake_system"]
ORDERS = [("accept", "reject"), ("reject", "accept")]
NOFIELDS = dict(pie=100, endow=100, offer=0, keep=0, sent=0, kept=0, received=0, opt1="", opt2="")


def inductions():
    return list(pd.read_csv(STIM_DIR / "ext5" / "inductions.csv").itertuples())


def want_reason(tid):
    return bool(np.random.default_rng(stable_int(MASTER_SEED, tid)).random() < JUSTIFICATION_RATE)


def s1_row(tid, module, cell, i, p, off, s, reg_id, justify):
    opts = ORDERS[s]
    r = base_row(tid, module, cell, "S1", "S1", i.state, 100, p, "none0", s, cond=f"{REGULATION[reg_id][0]}_{i.state}",
                 fmt="word", first=opts[0], msg_set=None, state=i.state, induction_id=i.induction_id,
                 prompt=render("S1", p, s1_fields(100, off, *opts), None, justify))
    r.update(offer_share=off, option_order="/".join(opts), option_map=option_map_json({o: o for o in opts}),
             justify=justify, system=system_regulated(i.text, reg_id), is_baseline=False, reg_id=reg_id,
             strategy=REGULATION[reg_id][0], defence=None)
    return r


def module_r():
    rows = []
    for reg_id, i, p in product(REGULATION, inductions(), range(4)):
        strat = REGULATION[reg_id][0]
        for off, s in product(R_OFFERS, range(2)):
            cell = f"R_S1_{reg_id}_{i.state}_off{round(off * 100):02d}"
            tid = f"EXT5|{cell}|p{p}|{i.induction_id}|s{s}"
            rows.append(s1_row(tid, "R", cell, i, p, off, s, reg_id, want_reason(tid)))
        for s in range(2):
            cell = f"R_S3b_{reg_id}_{i.state}"
            tid = f"EXT5|{cell}|p{p}|{i.induction_id}|s{s}"
            justify = want_reason(tid)
            r = base_row(tid, "R", cell, "S3b", "S3b", i.state, 100, p, "none0", s, cond=f"{strat}_{i.state}", fmt=None,
                         first=None, msg_set=None, state=i.state, induction_id=i.induction_id,
                         prompt=render("S3b", p, NOFIELDS, None, justify))
            r.update(json_key="send", max_amount=100, justify=justify, system=system_regulated(i.text, reg_id),
                     is_baseline=False, reg_id=reg_id, strategy=strat, defence=None)
            rows.append(r)
    return rows


def module_p():
    _, sets = load_messages()
    rows = []
    for defence, gt, p, set_name in product(DEFENCES, ["S3b", "S2-DG"], range(4), P_SETS):
        for msg, s in product(sets[set_name], range(2)):
            cell = f"P_{gt}_{defence}_{set_name}"
            tid = f"EXT5|{cell}|p{p}|{msg.msg_id}|s{s}"
            justify = want_reason(tid)
            system, prompt = defended(render(gt, p, NOFIELDS, msg.text, justify), defence)
            r = base_row(tid, "P", cell, gt, "S2" if gt == "S2-DG" else "S3b", set_name, 100, p, msg.msg_id, s,
                         cond=f"{defence}_{set_name}", fmt=None, first=None, msg_set=set_name, state=None,
                         induction_id=None, prompt=prompt)
            r.update(json_key=GAME_TYPES[gt]["key"], max_amount=100, justify=justify, system=system, reg_id=None,
                     strategy=None, defence=defence)
            rows.append(r)
    return rows


def module_f():
    rows = []
    for i, p, off, s in product(inductions(), range(4), F_OFFERS, range(2)):
        cell = f"F_S1_{i.state}_off{round(off * 100):03d}"
        tid = f"EXT5|{cell}|p{p}|{i.induction_id}|s{s}"
        rows.append(s1_row(tid, "F", cell, i, p, off, s, "NONE", False))
    return rows


def mood_probe():
    rows = []
    for reg_id, i, p in product(REGULATION, inductions(), range(2)):
        tid = f"PROBE5|mood|{reg_id}|p{p}|{i.induction_id}"
        rng = np.random.default_rng(stable_int(MASTER_SEED, tid))
        opts = ["calm", "angry", "sad", "happy"]
        rng.shuffle(opts)
        alts = " or ".join(f'"{o}"' for o in opts)
        prompt = (head(render("S1", p, s1_fields(100, 0.30), None, False)) + "\n\n"
                  + MOOD_Q.format(opts=", ".join(opts)) + "\n\n" + MOOD_FMT.format(alts=alts))
        rows.append(dict(trial_id=tid, cell_id=f"PROBE5_{reg_id}_{i.state}", item="mood", sub_exp="S1", game_type="S1",
                         emotion=i.state, state=i.state, induction_id=i.induction_id, reg_id=reg_id,
                         strategy=REGULATION[reg_id][0], stakes=100, paraphrase=p, msg_id="none0",
                         variant_id=f"PROBE5|{reg_id}|p{p}|{i.induction_id}", sample=0, is_baseline=False, extension=False,
                         answer_type="choice", options="/".join(opts), correct=i.state, json_key="answer",
                         seed=stable_int(MASTER_SEED, "seed", tid) % (2**31), system=system_regulated(i.text, reg_id),
                         prompt=prompt))
    return rows


def core(t: pd.DataFrame) -> pd.DataFrame:
    p01 = t.paraphrase < 2
    ind_idx = t.induction_id.map({i.induction_id: k for k, i in enumerate(inductions())}).fillna(0).astype(int)
    off30 = (t.offer_share.astype(float).round(2) == 0.30).astype(int)
    alt = (t.paraphrase + ind_idx + off30) % 2  # one order per cell, alternating
    r_s1 = (t.module == "R") & (t.game_type == "S1") & p01 & (t["sample"] == alt)
    r_s3 = (t.module == "R") & (t.game_type == "S3b") & p01 & (t["sample"] == 0)
    pp = (t.module == "P") & p01 & (t["sample"] == 0)
    return t[r_s1 | r_s3 | pp]


def main():
    t = pd.DataFrame(module_r() + module_p() + module_f())
    assert t.trial_id.is_unique
    SCEN.mkdir(parents=True, exist_ok=True)
    t.to_json(SCEN / "ext5_trials.jsonl", orient="records", lines=True)
    pr = pd.DataFrame(mood_probe())
    pr.to_json(SCEN / "probe_ext5_mood.jsonl", orient="records", lines=True)
    c = core(t)
    c.to_json(SCEN / "ext5core_trials.jsonl", orient="records", lines=True)
    pc = pr[pr.paraphrase == 0]
    pc.to_json(SCEN / "probe_ext5core_mood.jsonl", orient="records", lines=True)
    print(t.groupby(["module", "game_type"]).size().to_string())
    print(f"total trials/model: {len(t)}; justification requested: {t.justify.mean():.1%}; mood probe: {len(pr)}")
    print(f"core: {len(c)} ({c.groupby('module').size().to_dict()}); core probe: {len(pc)}")
    bal = c[(c.module == "R") & (c.game_type == "S1")].groupby(["reg_id", "state", "offer_share"])["first"] \
        .apply(lambda s: (s == "accept").mean())
    print(f"core R-S1 share with accept first per regulation x state x offer: min {bal.min():.2f}, max {bal.max():.2f}")


if __name__ == "__main__":
    main()
