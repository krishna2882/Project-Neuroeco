"""Simulate runner output with KNOWN effects, in exactly the format run/runner.py writes, so the
whole analysis pipeline can be validated before real data exist (Phase-1 deliverable).

Writes data/sim/raw/<simA|simB>/main.jsonl and checks.jsonl.
TRUTH (below) is imported by analysis/validate.py.
"""
import json

import numpy as np
import pandas as pd
from scipy.special import expit

from analysis.common import load_bank
from config import DATA_DIR

SIM_DIR = DATA_DIR / "sim" / "raw"

TRUTH = {
    "simA": dict(
        fs_alpha={"none": 0.30, "neutral": 0.30, "angry": 0.60, "sad": 0.15, "happy": 0.30}, fs_lambda=15.0,
        stakes_logit=0.6, sigma_variant=0.5,
        s2_base={"UG": 0.45, "DG": 0.25},
        s2_eff={("angry", "UG"): 0.06, ("angry", "DG"): 0.0, ("sad", "UG"): 0.05, ("sad", "DG"): 0.05},
        s3a_base=0.25, s3a_slope=0.15, s3a_eff={"angry": -0.04, "sad": 0.05, "happy": 0.02},
        s3b_base=0.50, s3b_eff={"angry": -0.08, "happy": 0.05},
        recog=0.90, offformat=0.02),
    "simB": dict(
        fs_alpha={"none": 0.30, "neutral": 0.30, "angry": 0.40, "sad": 0.25, "happy": 0.30}, fs_lambda=10.0,
        stakes_logit=0.0, sigma_variant=0.5,
        s2_base={"UG": 0.48, "DG": 0.35},
        s2_eff={("angry", "UG"): 0.02, ("angry", "DG"): 0.02, ("sad", "UG"): 0.03, ("sad", "DG"): 0.03},
        s3a_base=0.33, s3a_slope=0.05, s3a_eff={"sad": 0.03},
        s3b_base=0.60, s3b_eff={},
        recog=0.75, offformat=0.05),
}


def true_mao(alpha):
    return alpha / (1 + 2 * alpha)


def simulate_model(key, T, bank, checks, rng):
    var_u = {v: rng.normal(0, T["sigma_variant"]) for v in bank.variant_id.unique()}
    var_s = {v: rng.normal(0, 0.03) for v in bank.variant_id.unique()}
    recs = []
    for t in bank.itertuples():
        emo = t.emotion
        stakes_c = 0.5 if t.stakes == bank.stakes.max() else -0.5
        if t.sub_exp == "S1":
            x = t.offer_share
            a = T["fs_alpha"][emo]
            logit = T["fs_lambda"] * (x - a * max(0, 1 - 2 * x)) + T["stakes_logit"] * stakes_c + var_u[t.variant_id]
            pa = expit(logit)
            val = {"decision": "accept" if rng.random() < pa else "reject"}
            extra = {"p_accept_lp": float(expit(logit + rng.normal(0, 0.3)))}
        else:
            if t.sub_exp == "S2":
                m = T["s2_base"][t.game] + T["s2_eff"].get((emo, t.game), 0.0) + 0.02 * stakes_c
            elif t.sub_exp == "S3a":
                m = T["s3a_base"] + T["s3a_slope"] * (t.sent_share - 0.5667) + T["s3a_eff"].get(emo, 0.0)
            else:
                m = T["s3b_base"] + T["s3b_eff"].get(emo, 0.0)
            share = float(np.clip(m + var_s[t.variant_id] + rng.normal(0, 0.06), 0, 1))
            denom = t.received if t.sub_exp == "S3a" else t.max_amount
            val = {t.json_key: int(round(share * denom))}
            extra = {}
        if t.justify:
            val["reason"] = "Simulated justification."
        attempt = 1
        if rng.random() < T["offformat"]:
            recs.append(dict(trial_id=t.trial_id, attempt=1, model_key=key, bank="trials", status="off_format",
                             raw="I would rather not say.", model_version=f"sim:{key}"))
            attempt = 2
        rec = dict(trial_id=t.trial_id, attempt=attempt, model_key=key, bank="trials", status="ok",
                   raw=json.dumps(val), model_version=f"sim:{key}", reason=val.get("reason"))
        if t.sub_exp == "S1":
            rec["decision"] = val["decision"]
            rec.update(extra)
        else:
            amt = val[t.json_key]
            rec["amount"] = amt
            rec["share"] = amt / (t.received if t.sub_exp == "S3a" else t.max_amount)
        recs.append(rec)

    crecs = []
    emos = ["neutral", "angry", "sad", "happy"]
    for c in checks.itertuples():
        r = dict(trial_id=c.trial_id, attempt=1, model_key=key, bank="checks", status="ok",
                 model_version=f"sim:{key}")
        if not c.is_baseline:
            r["perceived_emotion"] = c.emotion if rng.random() < T["recog"] else rng.choice(
                [e for e in emos if e != c.emotion])
            r["intensity"] = int(np.clip(round(rng.normal(2 if c.emotion == "neutral" else 5, 1)), 1, 7))
        if c.sub_exp == "S1":
            r["fairness"] = int(np.clip(round(1 + 12 * c.offer_share + rng.normal(0, 0.7)), 1, 7))
        elif c.sub_exp == "S3a":
            r["fairness"] = int(np.clip(round(1 + 6 * c.sent_share + rng.normal(0, 0.7)), 1, 7))
        r["p_retaliate"] = int(np.clip(rng.normal(60 if c.emotion == "angry" else 30, 10), 0, 100))
        crecs.append(r)
    return recs, crecs


def main():
    bank, checks = load_bank("trials"), load_bank("checks")
    bank = bank[~bank.extension]
    rng = np.random.default_rng(7)
    for key, T in TRUTH.items():
        recs, crecs = simulate_model(key, T, bank, checks, rng)
        d = SIM_DIR / key
        d.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(recs).to_json(d / "main.jsonl", orient="records", lines=True)
        pd.DataFrame(crecs).to_json(d / "checks.jsonl", orient="records", lines=True)
        print(f"{key}: {len(recs)} trial records, {len(crecs)} check records -> {d}")


if __name__ == "__main__":
    main()
