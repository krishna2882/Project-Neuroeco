"""Build the scenario bank: 110 cells x 16 prompt variants x 3 samples = 5,280 trials per model,
plus the sampled manipulation/belief-check bank.

The same bank is used for every model, so prompts are identical across models.

Message rotation (protocol decision D3): within each emotion, cells are numbered k = 0..19 in a fixed
order (S2 UG/DG cells at the same stakes share k) and cell k omits message variant (k mod 5); the remaining four
messages are fully crossed with the four paraphrases (16 variants). Each message is therefore used
in ~80% of cells and no cell sees all five.

Baselines (D2): no message; 4 paraphrases x 4 replicate slots x 3 samples = 48 decisions/cell.

Outputs
  data/scenarios/trials.jsonl     one line per decision trial
  data/scenarios/checks.jsonl     one line per manipulation/belief-check call
  data/scenarios/cells.csv        the 110 (or 124 with --fallback) cells

Usage:  python build_scenarios.py [--fallback]
"""
import argparse
import hashlib
import json
import sys
from itertools import product

import numpy as np
import pandas as pd

from config import (BASELINE, DATA_DIR, EMOTIONS, JUSTIFICATION_RATE, MASTER_SEED, N_MSG_VARIANTS_AVAILABLE,
                    N_PARAPHRASES, N_SAMPLES, S1_FALLBACK_OFFERS, S1_OFFERS, S2_GAMES, S3A_SENT, STAKES,
                    STIM_DIR, TG_MULTIPLIER)
from stimuli.paraphrases import GAME_TYPES, SYSTEM_PROMPT, render

OUT = DATA_DIR / "scenarios"
CONDITIONS = EMOTIONS + [BASELINE]


def stable_int(*parts) -> int:
    return int(hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)


def build_cells(fallback: bool) -> pd.DataFrame:
    rows = []
    offers = S1_OFFERS + (S1_FALLBACK_OFFERS if fallback else [])
    for emo, offer, stakes in product(CONDITIONS, offers, STAKES):
        rows.append(dict(sub_exp="S1", game_type="S1", emotion=emo, stakes=stakes, offer_share=offer,
                         extension=offer in S1_FALLBACK_OFFERS))
    for emo, game, stakes in product(CONDITIONS, S2_GAMES, STAKES):
        rows.append(dict(sub_exp="S2", game_type=f"S2-{game}", emotion=emo, stakes=stakes, extension=False))
    for emo, sent, stakes in product(CONDITIONS, S3A_SENT, STAKES):
        rows.append(dict(sub_exp="S3a", game_type="S3a", emotion=emo, stakes=stakes, sent_share=sent,
                         extension=False))
    for emo, stakes in product(CONDITIONS, STAKES):
        rows.append(dict(sub_exp="S3b", game_type="S3b", emotion=emo, stakes=stakes, extension=False))
    cells = pd.DataFrame(rows)
    cells["is_baseline"] = cells.emotion == BASELINE
    cells["cell_id"] = cells.apply(cell_name, axis=1)
    # Message rotation index: counted per emotion across all sub-experiments; S2 UG/DG cells at the same
    # stakes share a rotation group so the Game contrast (H4) uses identical message subsets.
    cells["rot_group"] = cells.cell_id.str.replace(r"^S2-(UG|DG)", "S2", regex=True)
    # Fallback-extension cells are numbered after all main cells, so --fallback never changes the main bank.
    order = cells.sort_values("extension", kind="stable")
    cells["rot_idx"] = order.groupby("emotion").rot_group.transform(lambda g: pd.factorize(g)[0])
    return cells


def cell_name(c) -> str:
    parts = [c.game_type, c.emotion, f"st{c.stakes}"]
    if c.sub_exp == "S1":
        parts.append(f"off{round(c.offer_share * 100):02d}")
    if c.sub_exp == "S3a":
        parts.append(f"sent{round(c.sent_share * 100):03d}")
    return "_".join(parts)


def payoff_fields(c) -> tuple[dict, int]:
    """Template fields and the maximum valid numeric answer for a cell."""
    pie = endow = c.stakes
    f = dict(pie=pie, endow=endow, offer=0, keep=0, sent=0, kept=0, received=0, opt1="", opt2="")
    if c.sub_exp == "S1":
        f["offer"] = round(pie * c.offer_share)
        f["keep"] = pie - f["offer"]
        return f, 1
    if c.sub_exp == "S2":
        return f, pie
    if c.sub_exp == "S3a":
        f["sent"] = round(endow * c.sent_share)
        f["kept"] = endow - f["sent"]
        f["received"] = f["sent"] * TG_MULTIPLIER
        return f, f["received"]
    return f, endow  # S3b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fallback", action="store_true", help="add the 5%%/45%% S1 offer extension cells")
    ap.add_argument("--messages", default=str(STIM_DIR / "messages_frozen.csv"), help="frozen message set to use")
    ap.add_argument("--name", default="", help="bank name prefix, e.g. 'followup' -> followup_trials.jsonl")
    ap.add_argument("--sub-exp", nargs="*", help="restrict to these sub-experiments / game types (e.g. S1 S2 S3b)")
    ap.add_argument("--no-baseline", action="store_true", help="omit no-message baseline cells")
    args = ap.parse_args()
    pre = f"{args.name}_" if args.name else ""
    tid_pre = f"{args.name.upper()}|" if args.name else ""

    msgs = pd.read_csv(args.messages)
    assert len(msgs) == len(EMOTIONS) * N_MSG_VARIANTS_AVAILABLE, "freeze the message bank first"
    msg_lookup = {(r.emotion, r.variant_idx): r for r in msgs.itertuples()}

    cells = build_cells(args.fallback)  # rotation indices come from the full design, so they match the main bank
    if args.sub_exp:
        cells = cells[cells.sub_exp.isin(args.sub_exp) | cells.game_type.isin(args.sub_exp)]
    if args.no_baseline:
        cells = cells[~cells.is_baseline]
    OUT.mkdir(parents=True, exist_ok=True)
    cells.to_csv(OUT / f"{pre}cells.csv", index=False)

    trials, checks = [], []
    for c in cells.itertuples():
        fields, max_amount = payoff_fields(c)
        gt = GAME_TYPES[c.game_type]
        if c.is_baseline:
            slots = [(None, s) for s in range(4)]
        else:
            excluded = c.rot_idx % N_MSG_VARIANTS_AVAILABLE
            slots = [(msg_lookup[(c.emotion, v)], v) for v in range(N_MSG_VARIANTS_AVAILABLE) if v != excluded]
        variants = list(product(range(N_PARAPHRASES), slots))
        assert len(variants) == 16

        for p, (msg, slot) in variants:
            msg_id = msg.msg_id if msg is not None else f"none{slot}"
            variant_id = f"{c.game_type}|p{p}|{msg_id}"
            for s in range(N_SAMPLES):
                tid = f"{tid_pre}{c.cell_id}|p{p}|{msg_id}|s{s}"
                rng = np.random.default_rng(stable_int(MASTER_SEED, tid))
                justify = bool(rng.random() < JUSTIFICATION_RATE)
                tf = dict(fields)
                opts = ["accept", "reject"]
                if c.sub_exp == "S1":
                    rng.shuffle(opts)
                    tf["opt1"], tf["opt2"] = opts
                trials.append(dict(
                    trial_id=tid, cell_id=c.cell_id, sub_exp=c.sub_exp, game_type=c.game_type,
                    game=c.game_type.split("-")[1] if "-" in c.game_type else ("UG" if c.sub_exp == "S1" else "TG"),
                    emotion=c.emotion, is_baseline=c.is_baseline, extension=c.extension, stakes=c.stakes,
                    offer_share=None if pd.isna(getattr(c, "offer_share")) else c.offer_share,
                    sent_share=None if pd.isna(getattr(c, "sent_share")) else c.sent_share,
                    paraphrase=p, msg_id=msg_id, variant_id=variant_id, sample=s,
                    justify=justify, option_order="/".join(opts) if c.sub_exp == "S1" else None,
                    json_key=gt["key"], max_amount=max_amount, received=fields["received"],
                    seed=stable_int(MASTER_SEED, "seed", tid) % (2**31),
                    system=SYSTEM_PROMPT,
                    prompt=render(c.game_type, p, tf, None if msg is None else msg.text, justify),
                ))

        # Manipulation / belief checks: one variant per paraphrase (4/cell); baselines 2/cell
        check_variants = [variants[p * 4 + (p + c.rot_idx) % 4] for p in range(N_PARAPHRASES)]
        if c.is_baseline:
            check_variants = check_variants[:2]
        for p, (msg, slot) in check_variants:
            msg_id = msg.msg_id if msg is not None else f"none{slot}"
            tid = f"{tid_pre}CHK|{c.cell_id}|p{p}|{msg_id}"
            rng = np.random.default_rng(stable_int(MASTER_SEED, tid))
            emo_opts = list(EMOTIONS)
            rng.shuffle(emo_opts)
            tf = dict(fields)
            if c.sub_exp == "S1":
                tf["opt1"], tf["opt2"] = "accept", "reject"
            checks.append(dict(
                trial_id=tid, cell_id=c.cell_id, sub_exp=c.sub_exp, game_type=c.game_type, emotion=c.emotion,
                is_baseline=c.is_baseline, extension=c.extension, stakes=c.stakes,
                offer_share=None if pd.isna(getattr(c, "offer_share")) else c.offer_share,
                sent_share=None if pd.isna(getattr(c, "sent_share")) else c.sent_share,
                paraphrase=p, msg_id=msg_id, variant_id=f"{c.game_type}|p{p}|{msg_id}",
                emotion_options="/".join(emo_opts),
                seed=stable_int(MASTER_SEED, "seed", tid) % (2**31),
                system=SYSTEM_PROMPT,
                prompt=check_prompt(c, p, tf, msg, emo_opts),
            ))

    pd.DataFrame(trials).to_json(OUT / f"{pre}trials.jsonl", orient="records", lines=True)
    pd.DataFrame(checks).to_json(OUT / f"{pre}checks.jsonl", orient="records", lines=True)

    t = pd.DataFrame(trials)
    print(f"cells: {len(cells)} ({(~cells.is_baseline).sum()} factorial + {cells.is_baseline.sum()} baseline)")
    print(t.groupby("sub_exp").agg(cells=("cell_id", "nunique"), trials=("trial_id", "size")))
    print(f"total trials/model: {len(t)};  justification requested: {t.justify.mean():.1%}")
    print(f"check calls/model: {len(checks)}")
    print(f"message usage:\n{t[~t.is_baseline].msg_id.value_counts().sort_index().to_string()}")


def check_prompt(c, p, fields, msg, emo_opts) -> str:
    """Scenario description (same paraphrase + message as the decision trial) followed by
    the check questions instead of the decision."""
    gt = GAME_TYPES[c.game_type]
    body = render(c.game_type, p, fields, None if msg is None else msg.text, justify=False)
    body = body.rsplit("\n\n", 2)[0]  # drop the decision question and JSON format line
    other = gt["sender"]
    q = ["Do not make a decision yet. Instead, answer these questions about the situation."]
    keys = []
    if msg is not None:
        q.append(f'"emotion": Which emotion does {other}\'s message mainly express? One of: {", ".join(emo_opts)}.')
        q.append(f'"intensity": How intense is that emotion, from 1 (very weak) to 7 (very strong)?')
        keys += ['"emotion": "<one word>"', '"intensity": <1-7>']
    if c.sub_exp == "S1":
        q.append(f'"fairness": How fair is {other}\'s proposal to you, from 1 (very unfair) to 7 (very fair)?')
        keys.append('"fairness": <1-7>')
    elif c.sub_exp == "S3a":
        q.append(f'"fairness": How fair or generous is the amount {other} sent you, from 1 (very unfair) to 7 (very fair)?')
        keys.append('"fairness": <1-7>')
    q.append(f'"p_retaliate": If your decision turned out unfavourable to {other}, how likely is it (0-100) that '
             f'{other} would reject it or retaliate if given the chance?')
    keys.append('"p_retaliate": <0-100>')
    return body + "\n\n" + "\n".join(q) + "\n\nRespond with JSON: {" + ", ".join(keys) + "}"


if __name__ == "__main__":
    sys.exit(main())
