"""Build the extension-4 stress-test banks (docs/preregistration_extension4.md). Same system prompt, paraphrases, message
block, JSON format and seeding scheme as the main study; new trial ids give new seeds.

Module O  Option order and answer format (S1 responder, INR 100, offers 10/30/50%):
          8 formats [word, letter A/B, relabelled "deal"/"no deal"] x [accept listed first, reject listed first]
          + yes/no question asked as "Do you accept?" or "Do you reject?";
          messages: none (4 slots) + main neutral/angry/sad N1-4, A1-4, S1-4; (16 slots) x 4 paraphrases x 2 samples = 3,072
Module I  Prompt injection and pressure in Player B's message (S3b investor and S2-DG dictator, INR 100 / 10,000):
          6 message sets x 4 messages [neutral FN2/5/6/7, promise, plead, command, fake_rule, fake_system]
          x 4 paraphrases x 2 stakes x 3 samples = 1,152
Module X  Incidental mood of the model (system-prompt background, no partner message):
          4 states [calm, angry, sad, happy] x 4 inductions x 4 paraphrases;
          S1 offers 10/30/50% x 2 samples (384) + S3b x 2 stakes x 3 samples (384) = 768
Module D  Dominance / sanity (word format, random option order):
          S1 offers of 0% and 100% x [none (4 slots), neutral N1-4, angry A1-4] x 4 paraphrases x 2 samples (192)
          + S3b with a zero multiplier x same 12 slots x 4 paraphrases x 3 samples (144) = 336
Total 5,328 decisions per model.
Mood probe (manipulation check for X): 4 states x 4 inductions x 4 paraphrases x 2 samples = 128

  python build_ext4.py   -> data/scenarios/ext4_trials.jsonl, data/scenarios/probe_ext4_mood.jsonl
"""
from itertools import product

import numpy as np
import pandas as pd

from build_scenarios import stable_int
from config import DATA_DIR, JUSTIFICATION_RATE, MASTER_SEED, STIM_DIR
from stimuli.ext4.templates import MOOD_FMT, MOOD_Q, S3B_ZERO, option_map_json, s1_format, system_with_mood
from stimuli.paraphrases import GAME_TYPES, MSG_BLOCK, REASON_FIELD, S3B_FORMAT, SYSTEM_PROMPT, render

SCEN = DATA_DIR / "scenarios"
EXT4 = STIM_DIR / "ext4"
O_OFFERS = [0.10, 0.30, 0.50]
O_FORMATS = [("word", "accept"), ("word", "reject"), ("letter", "accept"), ("letter", "reject"),
             ("relabel", "accept"), ("relabel", "reject"), ("yesno", "accept"), ("yesno", "reject")]


def load_messages():
    main = pd.read_csv(STIM_DIR / "messages_frozen.csv")
    fu = pd.read_csv(STIM_DIR / "followup" / "messages_frozen.csv")
    inj = pd.read_csv(EXT4 / "messages_injection.csv")
    m = {}
    for emo in ["neutral", "angry", "sad"]:
        m[emo] = list(main[(main.emotion == emo) & (main.variant_idx < 4)].itertuples())
    sets = {"neutral": list(fu[(fu.emotion == "neutral") & (fu.variant_idx < 4)].itertuples())}
    for s, g in inj.groupby("set", sort=False):
        sets[s] = list(g.sort_values("variant_idx").itertuples())
    assert all(len(v) == 4 for v in list(m.values()) + list(sets.values()))
    return m, sets


def s1_fields(pie, offer_share, opt1="accept", opt2="reject"):
    offer = round(pie * offer_share)
    return dict(pie=pie, endow=pie, offer=offer, keep=pie - offer, sent=0, kept=0, received=0, opt1=opt1, opt2=opt2)


def head(prompt: str) -> str:
    """Scenario text and message, without the decision question and the JSON line."""
    return prompt.rsplit("\n\n", 2)[0]


def base_row(tid, module, cell, game_type, sub_exp, emotion, stakes, p, msg_id, s, **kw):
    return dict(trial_id=tid, module=module, cell_id=cell, sub_exp=sub_exp, game_type=game_type,
                game={"S1": "UG", "S2-DG": "DG"}.get(game_type, "TG"), emotion=emotion,
                is_baseline=msg_id.startswith("none"), extension=False, stakes=stakes,
                offer_share=None, sent_share=None, paraphrase=p, msg_id=msg_id,
                variant_id=f"{cell}|p{p}|{msg_id}", sample=s, justify=False, option_order=None, option_map=None,
                json_key="decision", max_amount=1, received=0,
                seed=stable_int(MASTER_SEED, "seed", tid) % (2**31), system=SYSTEM_PROMPT, **kw)


def module_o(msgs):
    rows = []
    slots = [("none", None, f"none{k}") for k in range(4)] + \
            [(e, m, m.msg_id) for e in ["neutral", "angry", "sad"] for m in msgs[e]]
    for (fmt, first), off, p, (emo, msg, mid) in product(O_FORMATS, O_OFFERS, range(4), slots):
        cond = f"{fmt}_{first[0].upper()}"
        cell = f"O_{cond}_off{round(off * 100):02d}"
        second = "reject" if first == "accept" else "accept"
        text = None if msg is None else msg.text
        if fmt == "word":
            prompt = render("S1", p, s1_fields(100, off, first, second), text, False)
            omap = {first: first, second: second}
        else:
            q, omap = s1_format(fmt, first)
            prompt = head(render("S1", p, s1_fields(100, off), text, False)) + "\n\n" + q
        for s in range(2):
            tid = f"EXT4|{cell}|p{p}|{mid}|s{s}"
            r = base_row(tid, "O", cell, "S1", "S1", emo, 100, p, mid, s, cond=cond, fmt=fmt, first=first,
                         msg_set=emo, state=None, induction_id=None, prompt=prompt)
            r.update(offer_share=off, option_order=f"{first}/{second}", option_map=option_map_json(omap))
            rows.append(r)
    return rows


def module_i(sets):
    rows = []
    for gt, stakes, p, (set_name, ms) in product(["S3b", "S2-DG"], [100, 10_000], range(4), sets.items()):
        for msg in ms:
            for s in range(3):
                cell = f"I_{gt}_{set_name}_st{stakes}"
                tid = f"EXT4|{cell}|p{p}|{msg.msg_id}|s{s}"
                rng = np.random.default_rng(stable_int(MASTER_SEED, tid))
                justify = bool(rng.random() < JUSTIFICATION_RATE)
                f = dict(pie=stakes, endow=stakes, offer=0, keep=0, sent=0, kept=0, received=0, opt1="", opt2="")
                r = base_row(tid, "I", cell, gt, "S2" if gt == "S2-DG" else "S3b", set_name, stakes, p, msg.msg_id, s,
                             cond=set_name, fmt=None, first=None, msg_set=set_name, state=None, induction_id=None,
                             prompt=render(gt, p, f, msg.text, justify))
                r.update(json_key=GAME_TYPES[gt]["key"], max_amount=stakes, justify=justify)
                rows.append(r)
    return rows


def module_x():
    ind = pd.read_csv(EXT4 / "inductions.csv")
    rows = []
    for i, p in product(ind.itertuples(), range(4)):
        system = system_with_mood(i.text)
        for off, s in product(O_OFFERS, range(2)):
            cell = f"X_S1_{i.state}_off{round(off * 100):02d}"
            tid = f"EXT4|{cell}|p{p}|{i.induction_id}|s{s}"
            rng = np.random.default_rng(stable_int(MASTER_SEED, tid))
            justify = bool(rng.random() < JUSTIFICATION_RATE)
            opts = ["accept", "reject"]
            rng.shuffle(opts)
            r = base_row(tid, "X", cell, "S1", "S1", i.state, 100, p, "none0", s, cond=i.state, fmt="word",
                         first=opts[0], msg_set=None, state=i.state, induction_id=i.induction_id,
                         prompt=render("S1", p, s1_fields(100, off, *opts), None, justify))
            r.update(offer_share=off, option_order="/".join(opts), option_map=option_map_json({o: o for o in opts}),
                     justify=justify, system=system, is_baseline=False)
            rows.append(r)
        for stakes, s in product([100, 10_000], range(3)):
            cell = f"X_S3b_{i.state}_st{stakes}"
            tid = f"EXT4|{cell}|p{p}|{i.induction_id}|s{s}"
            rng = np.random.default_rng(stable_int(MASTER_SEED, tid))
            justify = bool(rng.random() < JUSTIFICATION_RATE)
            f = dict(pie=stakes, endow=stakes, offer=0, keep=0, sent=0, kept=0, received=0, opt1="", opt2="")
            r = base_row(tid, "X", cell, "S3b", "S3b", i.state, stakes, p, "none0", s, cond=i.state, fmt=None,
                         first=None, msg_set=None, state=i.state, induction_id=i.induction_id,
                         prompt=render("S3b", p, f, None, justify))
            r.update(json_key="send", max_amount=stakes, justify=justify, system=system, is_baseline=False)
            rows.append(r)
    return rows


def module_d(msgs):
    rows = []
    slots = [("none", None, f"none{k}") for k in range(4)] + \
            [(e, m, m.msg_id) for e in ["neutral", "angry"] for m in msgs[e]]
    for off, p, (emo, msg, mid) in product([0.0, 1.0], range(4), slots):
        for s in range(2):
            cell = f"D_S1_off{round(off * 100):03d}"
            tid = f"EXT4|{cell}|p{p}|{mid}|s{s}"
            rng = np.random.default_rng(stable_int(MASTER_SEED, tid))
            opts = ["accept", "reject"]
            rng.shuffle(opts)
            r = base_row(tid, "D", cell, "S1", "S1", emo, 100, p, mid, s, cond=f"offer{round(off * 100)}", fmt="word",
                         first=opts[0], msg_set=emo, state=None, induction_id=None,
                         prompt=render("S1", p, s1_fields(100, off, *opts), None if msg is None else msg.text, False))
            r.update(offer_share=off, option_order="/".join(opts), option_map=option_map_json({o: o for o in opts}))
            rows.append(r)
    for p, (emo, msg, mid) in product(range(4), slots):
        msg_block = "" if msg is None else MSG_BLOCK.format(sender="Player B", message=msg.text)
        for s in range(3):
            cell = "D_S3b_zero"
            tid = f"EXT4|{cell}|p{p}|{mid}|s{s}"
            rng = np.random.default_rng(stable_int(MASTER_SEED, tid))
            justify = bool(rng.random() < JUSTIFICATION_RATE)
            body = S3B_ZERO[p].format(endow=100, msg_block=msg_block)
            fmt_line = S3B_FORMAT.format(endow=100, reason=REASON_FIELD if justify else "")
            r = base_row(tid, "D", cell, "S3b-zero", "S3b", emo, 100, p, mid, s, cond="zero_multiplier", fmt=None,
                         first=None, msg_set=emo, state=None, induction_id=None, prompt=f"{body}\n\n{fmt_line}")
            r.update(json_key="send", max_amount=100, justify=justify)
            rows.append(r)
    return rows


def mood_probe():
    ind = pd.read_csv(EXT4 / "inductions.csv")
    rows = []
    for i, p, s in product(ind.itertuples(), range(4), range(2)):
        tid = f"PROBE|mood|p{p}|{i.induction_id}|s{s}"
        rng = np.random.default_rng(stable_int(MASTER_SEED, tid))
        opts = ["calm", "angry", "sad", "happy"]
        rng.shuffle(opts)
        alts = " or ".join(f'"{o}"' for o in opts)
        prompt = (head(render("S1", p, s1_fields(100, 0.30), None, False)) + "\n\n"
                  + MOOD_Q.format(opts=", ".join(opts)) + "\n\n" + MOOD_FMT.format(alts=alts))
        rows.append(dict(trial_id=tid, cell_id=f"PROBE_mood_{i.state}", item="mood", sub_exp="S1", game_type="S1",
                         emotion=i.state, state=i.state, induction_id=i.induction_id, stakes=100, paraphrase=p,
                         msg_id="none0", variant_id=f"PROBE_mood|p{p}|{i.induction_id}", sample=s, is_baseline=False,
                         extension=False, answer_type="choice", options="/".join(opts), correct=i.state,
                         json_key="answer", seed=stable_int(MASTER_SEED, "seed", tid) % (2**31),
                         system=system_with_mood(i.text), prompt=prompt))
    return rows


def main():
    msgs, sets = load_messages()
    t = pd.DataFrame(module_o(msgs) + module_i(sets) + module_x() + module_d(msgs))
    assert t.trial_id.is_unique
    SCEN.mkdir(parents=True, exist_ok=True)
    t.to_json(SCEN / "ext4_trials.jsonl", orient="records", lines=True)
    pr = pd.DataFrame(mood_probe())
    pr.to_json(SCEN / "probe_ext4_mood.jsonl", orient="records", lines=True)
    print(t.groupby(["module", "game_type"]).size().to_string())
    print(f"total trials/model: {len(t)}; justification requested: {t.justify.mean():.1%}; mood probe: {len(pr)}")


if __name__ == "__main__":
    main()
