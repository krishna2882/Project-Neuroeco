"""Data-collection runner (decision trials and manipulation/belief checks).

* Reads the frozen scenario bank built by build_scenarios.py.
* Appends one JSON record per API call to data/raw/<model_key>/<tag>.jsonl (never overwrites).
* Resumable: trials that already have a valid record, or have used all attempts, are skipped.
* Off-format / out-of-range / refused outputs are logged as such and re-asked up to
  MAX_ATTEMPTS times in total; every attempt is kept, so first-attempt failure rates can be reported.
* Trials are grouped by prompt variant (cell x paraphrase x message) and the group order is
  shuffled with a fixed seed, so time-of-run is not confounded with any condition.

Examples
  python -m run.runner --model llama31_8b --tag pilot --pilot
  python -m run.runner --model grok --model-name grok-4-fast-non-reasoning --tag main --workers 4
  python -m run.runner --model llama31_8b --bank checks --tag checks
"""
import argparse
import json
import math
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from config import DATA_DIR, MASTER_SEED, MODELS, RAW_DIR, TEMPERATURE
from run.clients import make_client

MAX_ATTEMPTS = 3
SCEN = DATA_DIR / "scenarios"
REFUSAL_RE = re.compile(r"\b(I can(?:no|')t|I'm unable|I am unable|I won't|as an AI)\b", re.I)


# ------------------------------------------------------------------ schemas and parsing
def decision_schema(t) -> dict:
    if t["json_key"] == "decision":
        props = {"decision": {"type": "string", "enum": t["option_order"].split("/")}}
    else:
        props = {t["json_key"]: {"type": "integer"}}
    if t["justify"]:
        props["reason"] = {"type": "string"}
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


def check_schema(t) -> dict:
    props = {}
    if not t["is_baseline"]:
        props["emotion"] = {"type": "string", "enum": t["emotion_options"].split("/")}
        props["intensity"] = {"type": "integer"}
    if t["sub_exp"] in ("S1", "S3a"):
        props["fairness"] = {"type": "integer"}
    props["p_retaliate"] = {"type": "integer"}
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


def comprehension_schema(t) -> dict:
    v = {"type": "integer"} if t["answer_type"] == "number" else {"type": "string", "enum": ["yes", "no"]}
    return {"type": "object", "properties": {"answer": v}, "required": ["answer"], "additionalProperties": False}


def parse_comprehension(t, content: str) -> dict:
    """Extension-2 game-comprehension items (C1-C7): exact numeric match, or yes/no case-insensitively."""
    out = dict(status="ok", answer=None, is_correct=None)
    obj = extract_json(content)
    if not isinstance(obj, dict) or "answer" not in obj:
        out["status"] = "refusal" if REFUSAL_RE.search(content or "") else "off_format"
        return out
    if t["answer_type"] == "number":
        x = to_number(obj["answer"])
        if x is None:
            out["status"] = "off_format"
            return out
        out["answer"] = x
        out["is_correct"] = float(x) == float(t["correct"])
    else:
        v = str(obj["answer"]).strip().lower()
        if v not in ("yes", "no"):
            out["status"] = "off_format"
            return out
        out["answer"] = v
        out["is_correct"] = v == str(t["correct"]).lower()
    return out


def extract_json(text: str):
    text = text.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.M).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                return None
    return None


def to_number(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        m = re.search(r"-?\d[\d,]*\.?\d*", v)
        if m:
            return float(m.group(0).replace(",", ""))
    return None


def parse_decision(t, content: str) -> dict:
    out = dict(status="ok", decision=None, amount=None, share=None, reason=None)
    obj = extract_json(content)
    if not isinstance(obj, dict):
        out["status"] = "refusal" if REFUSAL_RE.search(content or "") else "off_format"
        return out
    out["reason"] = obj.get("reason")
    if t["json_key"] == "decision":
        v = str(obj.get("decision", "")).strip().lower()
        if v.startswith("accept"):
            out["decision"] = "accept"
        elif v.startswith("reject"):
            out["decision"] = "reject"
        else:
            out["status"] = "off_format"
        return out
    x = to_number(obj.get(t["json_key"]))
    if x is None:
        out["status"] = "off_format"
    elif not (0 <= x <= t["max_amount"]):
        out["status"] = "out_of_range"
        out["amount"] = x
    else:
        out["amount"] = x
        denom = t["received"] if t["sub_exp"] == "S3a" else t["max_amount"]
        out["share"] = x / denom
    return out


def parse_check(t, content: str) -> dict:
    out = dict(status="ok")
    obj = extract_json(content)
    if not isinstance(obj, dict):
        out["status"] = "refusal" if REFUSAL_RE.search(content or "") else "off_format"
        return out
    if not t["is_baseline"]:
        emo = str(obj.get("emotion", "")).strip().lower()
        out["perceived_emotion"] = emo if emo in t["emotion_options"].split("/") else None
        out["intensity"] = to_number(obj.get("intensity"))
        if out["perceived_emotion"] is None or out["intensity"] is None or not 1 <= out["intensity"] <= 7:
            out["status"] = "off_format"
    if t["sub_exp"] in ("S1", "S3a"):
        out["fairness"] = to_number(obj.get("fairness"))
        if out["fairness"] is None or not 1 <= out["fairness"] <= 7:
            out["status"] = "off_format"
    out["p_retaliate"] = to_number(obj.get("p_retaliate"))
    if out["p_retaliate"] is None or not 0 <= out["p_retaliate"] <= 100:
        out["status"] = "off_format"
    return out


def decision_token(lp) -> dict | None:
    """The first token of the decision *value*: the first token after `"decision":` whose text is
    not just whitespace/quotes. Handles Ollama (list of tokens) and OpenAI-style ({"content": [...]})."""
    if not lp:
        return None
    toks = lp.get("content") if isinstance(lp, dict) else lp
    text = ""
    for tok in toks or []:
        t = tok.get("token", "")
        if re.search(r'"decision"\s*:', text) and t.strip().strip('"').strip():
            return tok
        text += t
    return None


def p_accept_from_logprobs(lp, option_order=None) -> float | None:
    """P(accept) / (P(accept) + P(reject)) over the top alternatives at the decision token."""
    tok = decision_token(lp)
    if tok is None:
        return None
    pa = pr = 0.0
    for alt in tok.get("top_logprobs") or []:
        s = alt["token"].strip().strip('"').strip().lower()
        if s and "accept".startswith(s):
            pa += math.exp(alt["logprob"])
        elif s and "reject".startswith(s):
            pr += math.exp(alt["logprob"])
    return pa / (pa + pr) if pa + pr > 0 else None


# ------------------------------------------------------------------ run loop
def load_done(path) -> tuple[set, dict]:
    done, attempts = set(), {}
    if path.exists():
        with open(path) as f:
            for line in f:
                r = json.loads(line)
                attempts[r["trial_id"]] = max(attempts.get(r["trial_id"], 0), r["attempt"])
                if r["status"] == "ok":
                    done.add(r["trial_id"])
    for tid, a in attempts.items():
        if a >= MAX_ATTEMPTS:
            done.add(tid)
    return done, attempts


def pilot_subset(df: pd.DataFrame) -> pd.DataFrame:
    """~160 trials/model: every cell, one variant; S1 cells get two (to see the offer curve)."""
    rng = np.random.default_rng(MASTER_SEED + 1)
    picks = []
    for cid, g in df[df["sample"] == 0].groupby("cell_id", sort=True):
        n = 2 if g.sub_exp.iat[0] == "S1" else 1
        picks.append(g.iloc[rng.choice(len(g), n, replace=False)])
    return pd.concat(picks)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, choices=list(MODELS))
    ap.add_argument("--model-name", help="override the provider model id")
    ap.add_argument("--bank", default="trials", help="trials | checks | followup_trials | followup_checks | comprehension")
    ap.add_argument("--tag", default="main")
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--sub-exp", nargs="*", help="restrict to these sub-experiments (priority order S1,S2,S3a,S3b)")
    ap.add_argument("--extension-only", action="store_true", help="only the 5%%/45%% fallback cells")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--temperature", type=float, default=TEMPERATURE)
    ap.add_argument("--logprobs", action="store_true", help="request token logprobs (S1 graded DV)")
    args = ap.parse_args()

    df = pd.read_json(SCEN / f"{args.bank}.jsonl", lines=True, dtype=False)
    if args.pilot:
        df = pilot_subset(df)
    if args.sub_exp:
        df = df[df.sub_exp.isin(args.sub_exp)]
    if args.extension_only:
        df = df[df.extension]
    elif "extension" in df:
        df = df[~df.extension]

    # Shuffle prompt-variant groups, keep the samples of one variant adjacent (prefix-cache friendly)
    rng = np.random.default_rng(MASTER_SEED + 2)
    groups = df.variant_id + "@" + df.cell_id
    order = {g: i for i, g in enumerate(rng.permutation(groups.unique()))}
    df = df.assign(_o=groups.map(order)).sort_values(["_o", "trial_id"]).drop(columns="_o")

    out_path = RAW_DIR / args.model / f"{args.tag}.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    done, attempts = load_done(out_path)
    todo = [r for r in df.to_dict("records") if r["trial_id"] not in done]
    if args.limit:  # at most this many *new* trials this invocation (used for chunked runs)
        todo = todo[:args.limit]
    print(f"[{args.model}] bank={args.bank} tag={args.tag}: {len(df)} trials, {len(done & set(df.trial_id))} done, "
          f"{len(todo)} to run", flush=True)
    if not todo:
        return

    client = make_client(MODELS[args.model], args.model_name)
    lock = threading.Lock()
    is_check = args.bank.endswith("checks")
    is_comp = args.bank.startswith(("comprehension", "probe"))  # yes/no or number items with an "answer" key
    stats = dict(n=0, ok=0, t0=time.time())

    def run_one(t):
        a0 = attempts.get(t["trial_id"], 0)
        schema = comprehension_schema(t) if is_comp else check_schema(t) if is_check else decision_schema(t)
        for attempt in range(a0 + 1, MAX_ATTEMPTS + 1):
            rec = dict(trial_id=t["trial_id"], attempt=attempt, model_key=args.model, bank=args.bank,
                       temperature=args.temperature, ts=datetime.now(timezone.utc).isoformat())
            try:
                # Re-asks use a different seed so a deterministic failure is not simply repeated
                res = client.chat(t["system"], t["prompt"], schema, int(t["seed"]) + 7919 * (attempt - 1),
                                  args.temperature, logprobs=args.logprobs and not (is_check or is_comp))
                rec["raw"] = res["content"]
                meta = res["meta"]
                lp = meta.pop("logprobs", None)
                rec.update(meta)
                if is_comp:
                    rec.update(parse_comprehension(t, res["content"]))
                else:
                    rec.update(parse_check(t, res["content"]) if is_check else parse_decision(t, res["content"]))
                if not (is_check or is_comp) and t["json_key"] == "decision" and lp:
                    rec["p_accept_lp"] = p_accept_from_logprobs(lp)
                    dt = decision_token(lp)  # keep the raw alternatives so P(accept) can be re-derived
                    rec["decision_top_logprobs"] = dt.get("top_logprobs") if dt else None
            except Exception as e:  # network / server errors: logged, retried next attempt
                rec.update(status="error", error=f"{type(e).__name__}: {e}"[:500])
                time.sleep(5)
            with lock:
                with open(out_path, "a") as f:
                    f.write(json.dumps(rec) + "\n")
            if rec["status"] == "ok":
                return True
        return False

    def report():
        el = time.time() - stats["t0"]
        rate = stats["n"] / el if el else 0
        eta = (len(todo) - stats["n"]) / rate / 3600 if rate else float("nan")
        print(f"  {stats['n']}/{len(todo)}  ok={stats['ok']}  {rate * 60:.1f}/min  ETA {eta:.1f} h", flush=True)

    if args.workers == 1:
        for t in todo:
            stats["ok"] += run_one(t)
            stats["n"] += 1
            if stats["n"] % 25 == 0:
                report()
    else:
        with ThreadPoolExecutor(args.workers) as ex:
            for fut in as_completed([ex.submit(run_one, t) for t in todo]):
                stats["ok"] += fut.result()
                stats["n"] += 1
                if stats["n"] % 100 == 0:
                    report()
    report()
    print(f"done -> {out_path}")


if __name__ == "__main__":
    sys.exit(main())
