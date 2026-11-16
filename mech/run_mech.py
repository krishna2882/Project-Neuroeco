"""Extension 6: where is the partner's emotion represented, and does that representation drive the decision?
(docs/preregistration_extension6.md). Runs one open-weight model with Hugging Face transformers (fp16) on Ada.

  python -m mech.run_mech --model Qwen/Qwen2.5-3B-Instruct --key qwen25_3b_hf [--k 0 1 2 4 8] [--n-random 100]
  -> data/mech/<key>/behaviour.csv, probe.csv, steer.csv, sweep.csv, ablate.csv, meta.json

Stages (all in one run; nothing but the csv files is kept):
  acts    last-position residual stream at every layer for all 792 prompts of data/scenarios/ext6_prompts.jsonl, plus the
          unsteered behaviour (P(reject) from the next-token logits; amounts sampled as in the behavioural runs).
  probe   leave-messages-out linear probes for the partner's emotion at every layer; transfer between the partner's anger
          (message) and the model's own incidental anger (mood paragraph).
  steer   add k x (mean angry-message activation - mean neutral-message activation) at layer L* to every position of
          prompts that contain NO message, and read the decision. Null: random directions of the same norm.
  ablate  project the unit anger direction out of every layer's output on prompts with held-out angry and neutral
          messages, and measure what is left of the anger effect. Null: random unit directions.
"""
import argparse
import json
import re
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from transformers import AutoModelForCausalLM, AutoTokenizer, LogitsProcessor

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "data" / "scenarios" / "ext6_prompts.jsonl"
EMOS = ["neutral", "angry", "sad", "happy"]


# ------------------------------------------------------------------ model plumbing
def load_model(model_id):
    tok = AutoTokenizer.from_pretrained(model_id)
    tok.padding_side = "left"  # so that position -1 is the last real token of every prompt
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto")
    model.eval()
    return tok, model


def render(tok, df):
    return [tok.apply_chat_template([{"role": "system", "content": r.system}, {"role": "user", "content": r.prompt}],
                                    tokenize=False, add_generation_prompt=True) + r.prefill for r in df.itertuples()]


class Intervene:
    """add = {layer: vector}: added to the output of block `layer` (1-based: hidden_states[layer]) at every position.
    ablate = unit vector: projected out of the output of every block."""

    def __init__(self, model, add=None, ablate=None):
        self.blocks, self.add, self.ablate, self.handles = model.model.layers, add or {}, ablate, []

    def _hook(self, layer):
        def fn(module, inputs, output):
            h = output[0] if isinstance(output, tuple) else output
            if layer in self.add:
                h = h + self.add[layer].to(h.device, h.dtype)
            if self.ablate is not None:
                v = self.ablate.to(h.device, h.dtype)
                h = h - (h @ v).unsqueeze(-1) * v
            return (h,) + tuple(output[1:]) if isinstance(output, tuple) else h
        return fn

    def __enter__(self):
        for i, block in enumerate(self.blocks):
            if (i + 1) in self.add or self.ablate is not None:
                self.handles.append(block.register_forward_hook(self._hook(i + 1)))
        return self

    def __exit__(self, *a):
        for h in self.handles:
            h.remove()


def first_device(model):
    return next(model.parameters()).device


@torch.no_grad()
def forward_last(tok, model, txts, bs=24, hidden=False):
    """Next-token probabilities (and, optionally, every layer's residual stream) at the last position."""
    probs, hs = [], []
    for i in range(0, len(txts), bs):
        enc = tok(txts[i:i + bs], return_tensors="pt", padding=True, add_special_tokens=False).to(first_device(model))
        out = model(**enc, output_hidden_states=hidden)
        probs.append(torch.softmax(out.logits[:, -1, :].float(), -1).cpu())
        if hidden:
            hs.append(torch.stack([h[:, -1, :].float().cpu() for h in out.hidden_states], 1))
    return torch.cat(probs), (torch.cat(hs).numpy() if hidden else None)


class DecisionTokens:
    """Token ids for reading the answer after the pre-filled start of the JSON object."""

    def __init__(self, tok):
        pre = tok('{"decision": "', add_special_tokens=False).input_ids
        self.first = {}
        for w in ("accept", "reject"):
            full = tok('{"decision": "' + w, add_special_tokens=False).input_ids
            assert full[:len(pre)] == pre, "the pre-fill is not a token prefix of the answer"
            self.first[w] = full[len(pre)]
        assert self.first["accept"] != self.first["reject"]
        vocab = tok.batch_decode([[i] for i in range(len(tok))])
        self.digits = [i for i, s in enumerate(vocab) if s.isascii() and s.isdigit()]
        self.ends = [i for i, s in enumerate(vocab) if s.strip()[:1] in ("}", ",") and not any(c.isdigit() for c in s)]

    def p_reject(self, probs):
        a, r = probs[:, self.first["accept"]], probs[:, self.first["reject"]]
        return (r / (a + r)).numpy(), (a + r).numpy()


class Only(LogitsProcessor):
    def __init__(self, ids):
        self.ids = torch.tensor(ids)

    def __call__(self, input_ids, scores):
        mask = torch.full_like(scores, float("-inf"))
        mask[:, self.ids.to(scores.device)] = 0
        return scores + mask


@torch.no_grad()
def sample_amounts(tok, model, dt, txts, max_amounts, n=8, seed=0, bs=64):
    """n sampled amounts per prompt (T = 1, top-k 40, top-p 0.9 as in the Ollama runs; digits only, as under the JSON
    schema). Returns mean share and the share of valid samples per prompt."""
    rep = [t for t in txts for _ in range(n)]
    mx = np.repeat(np.asarray(max_amounts, float), n)
    vals = []
    torch.manual_seed(seed)  # the same random numbers under every intervention (common random numbers)
    for i in range(0, len(rep), bs):
        enc = tok(rep[i:i + bs], return_tensors="pt", padding=True, add_special_tokens=False).to(first_device(model))
        gen = model.generate(**enc, do_sample=True, temperature=1.0, top_k=40, top_p=0.9, max_new_tokens=7,
                             logits_processor=[Only(dt.digits + dt.ends)], eos_token_id=dt.ends,
                             pad_token_id=tok.pad_token_id)
        for s in tok.batch_decode(gen[:, enc.input_ids.shape[1]:], skip_special_tokens=True):
            m = re.match(r"\s*(\d+)", s)
            vals.append(float(m.group(1)) if m else np.nan)
    v = np.array(vals)
    v[v > mx] = np.nan
    share = (v / mx).reshape(-1, n)
    return np.nanmean(share, 1), np.mean(~np.isnan(share), 1)


def behave(tok, model, dt, df, txts, n, tag=None):
    """Decision for every prompt in df under whatever intervention is active. Returns rows."""
    rows = []
    s1, s3 = (df.game == "S1").values, (df.game == "S3b").values
    if s1.any():
        probs, _ = forward_last(tok, model, [t for t, k in zip(txts, s1) if k])
        pr, mass = dt.p_reject(probs)
        rows += [dict(prompt_id=p, game="S1", outcome=float(o), valid=float(m))
                 for p, o, m in zip(df.prompt_id[s1], pr, mass)]
    if s3.any():
        mean, valid = sample_amounts(tok, model, dt, [t for t, k in zip(txts, s3) if k], df.max_amount[s3].values, n)
        rows += [dict(prompt_id=p, game="S3b", outcome=float(o), valid=float(v))
                 for p, o, v in zip(df.prompt_id[s3], mean, valid)]
    return [dict(r, **(tag or {})) for r in rows]


# ------------------------------------------------------------------ probes
def probe_layers(H, bank):
    msg = (bank.set == "msg").values
    mood = bank.set.eq("mood").values & bank.emotion.isin(["angry", "calm"]).values
    y4 = bank.emotion[msg].map({e: i for i, e in enumerate(EMOS)}).values
    ids = bank.source_id[msg]
    order = {m: k for e in EMOS for k, m in enumerate(sorted(ids[bank.emotion[msg] == e].unique()))}
    groups = ids.map(order).values % 5  # each fold holds out two messages per emotion (never seen in training)
    rng = np.random.default_rng(6)
    bin_msg = msg & bank.emotion.isin(["angry", "neutral"]).values
    yb = (bank.emotion[bin_msg] == "angry").astype(int).values
    ym = (bank.emotion[mood] == "angry").astype(int).values
    clf = lambda: make_pipeline(StandardScaler(), LogisticRegression(C=0.1, max_iter=300))  # noqa: E731
    rows = []
    for layer in range(H.shape[1]):
        X = H[msg, layer]

        def cv_acc(y):
            hit = 0
            for tr, te in GroupKFold(5).split(X, y, groups):
                hit += (clf().fit(X[tr], y[tr]).predict(X[te]) == y[te]).sum()
            return hit / len(y)

        acc = cv_acc(y4)
        shuf = []
        for _ in range(3):  # null: emotion labels shuffled across messages
            perm = dict(zip(ids.unique(), rng.permutation([bank.emotion[msg][ids == m].iloc[0] for m in ids.unique()])))
            shuf.append(cv_acc(ids.map(perm).map({e: i for i, e in enumerate(EMOS)}).values))
        to_mood = clf().fit(H[bin_msg, layer], yb)
        to_msg = clf().fit(H[mood, layer], ym)
        v = H[bin_msg, layer][yb == 1].mean(0) - H[bin_msg, layer][yb == 0].mean(0)
        u = H[mood, layer][ym == 1].mean(0) - H[mood, layer][ym == 0].mean(0)
        rows.append(dict(layer=layer, acc_emotion4=acc, acc_shuffled=float(np.mean(shuf)),
                         transfer_msg_to_mood_auc=roc_auc_score(ym, to_mood.decision_function(H[mood, layer])),
                         transfer_mood_to_msg_auc=roc_auc_score(yb, to_msg.decision_function(H[bin_msg, layer])),
                         cos_msg_mood=float(v @ u / (np.linalg.norm(v) * np.linalg.norm(u) + 1e-9)),
                         norm_anger_dir=float(np.linalg.norm(v)), norm_resid=float(np.linalg.norm(X, axis=1).mean())))
    return pd.DataFrame(rows)


def direction(H, bank, emotion, layer, set_="msg", base="neutral", split="train"):
    s = (bank.set == set_).values & (bank.split == split).values
    a = H[s & (bank.emotion == emotion).values, layer].mean(0)
    b = H[s & (bank.emotion == base).values, layer].mean(0)
    return torch.tensor(a - b)


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--key", required=True)
    ap.add_argument("--k", nargs="*", type=float, default=[0, 1, 2, 4, 8])
    ap.add_argument("--n-random", type=int, default=100)
    ap.add_argument("--n-samples", type=int, default=8)
    ap.add_argument("--sweep-random", type=int, default=10)
    ap.add_argument("--out", default=str(ROOT / "data" / "mech"))
    ap.add_argument("--limit", type=int, help="development only: use every n-th prompt")
    a = ap.parse_args()
    out = Path(a.out) / a.key
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    log = lambda *m: print(f"[{time.time() - t0:6.0f}s]", *m, flush=True)  # noqa: E731

    bank = pd.read_json(BANK, lines=True, dtype=False)
    if a.limit:
        bank = bank.iloc[::a.limit].reset_index(drop=True)
    tok, model = load_model(a.model)
    dt = DecisionTokens(tok)
    n_layers = len(model.model.layers)
    L = round(n_layers / 2)  # pre-specified steering layer: the middle of the network
    txts = render(tok, bank)
    log(f"model {a.model}: {n_layers} layers, steering layer L*={L}; {len(bank)} prompts; "
        f"{len(dt.digits)} digit tokens, {len(dt.ends)} end tokens")

    # ---- acts + unsteered behaviour
    _, H = forward_last(tok, model, txts, hidden=True)
    beh = pd.DataFrame(behave(tok, model, dt, bank, txts, a.n_samples))
    bank.drop(columns=["system", "prompt"]).merge(beh, on=["prompt_id", "game"]).to_csv(out / "behaviour.csv", index=False)
    log("activations", H.shape, "behaviour saved")

    # ---- probes
    probe_layers(H, bank).to_csv(out / "probe.csv", index=False)
    log("probes saved")

    # ---- steering on prompts with no message and no mood
    tg = bank[bank.set == "target"]
    tg_txt = [txts[i] for i in tg.index]
    gen = torch.Generator().manual_seed(6)
    v = direction(H, bank, "angry", L)

    def randoms(n, norm, d):
        r = torch.randn(n, d, generator=gen)
        return r / r.norm(dim=1, keepdim=True) * norm

    def steer(layer, name, vec, ks):
        rows = []
        for k in ks:
            with Intervene(model, add={layer: k * vec}):
                rows += behave(tok, model, dt, tg, tg_txt, a.n_samples, dict(layer=layer, direction=name, k=k))
        return rows

    ks = [k for k in a.k if k != 0]
    rows = behave(tok, model, dt, tg, tg_txt, a.n_samples, dict(layer=L, direction="none", k=0.0))
    dirs = {"anger": v, "sad": direction(H, bank, "sad", L), "happy": direction(H, bank, "happy", L),
            "own_anger": direction(H, bank, "angry", L, set_="mood", base="calm", split="mood")}
    for name, vec in dirs.items():
        rows += steer(L, name, vec, ks)
    log("steering: named directions done")
    for j, r in enumerate(randoms(a.n_random, v.norm(), v.shape[0])):
        rows += steer(L, f"random{j:03d}", r, ks)
        if j % 20 == 19:
            log(f"steering: {j + 1} random directions")
    pd.DataFrame(rows).to_csv(out / "steer.csv", index=False)

    # ---- exploratory layer sweep: anger direction of each layer vs a few random directions
    rows = []
    for layer in range(2, n_layers + 1, 2):
        vl = direction(H, bank, "angry", layer)
        rows += steer(layer, "anger", vl, ks)
        for j, r in enumerate(randoms(a.sweep_random, vl.norm(), vl.shape[0])):
            rows += steer(layer, f"random{j:03d}", r, ks)
    pd.DataFrame(rows).to_csv(out / "sweep.csv", index=False)
    log("layer sweep saved")

    # ---- ablation on held-out messages (angry and neutral follow-up messages)
    ab = bank[(bank.set == "msg") & (bank.split == "test") & bank.emotion.isin(["angry", "neutral"])]
    ab_txt = [txts[i] for i in ab.index]
    unit = lambda x: x / x.norm()  # noqa: E731
    rows = behave(tok, model, dt, ab, ab_txt, a.n_samples, dict(direction="none"))
    with Intervene(model, ablate=unit(v)):
        rows += behave(tok, model, dt, ab, ab_txt, a.n_samples, dict(direction="anger"))
    for j, r in enumerate(randoms(a.n_random, 1.0, v.shape[0])):
        with Intervene(model, ablate=r):
            rows += behave(tok, model, dt, ab, ab_txt, a.n_samples, dict(direction=f"random{j:03d}"))
        if j % 20 == 19:
            log(f"ablation: {j + 1} random directions")
    pd.DataFrame(rows).merge(ab[["prompt_id", "emotion", "source_id", "paraphrase"]], on="prompt_id") \
        .to_csv(out / "ablate.csv", index=False)

    json.dump(dict(model=a.model, key=a.key, n_layers=n_layers, steer_layer=L, k=a.k, n_random=a.n_random,
                   n_samples=a.n_samples, n_prompts=len(bank), seconds=round(time.time() - t0),
                   torch=torch.__version__, dtype="float16", limit=a.limit), open(out / "meta.json", "w"), indent=1)
    log("done ->", out)


if __name__ == "__main__":
    main()
