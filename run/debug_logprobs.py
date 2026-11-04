"""Diagnostic: dump raw token logprobs for a few S1 prompts, with and without the JSON schema,
to check how P(accept) should be read from the Ollama response.

  python -m run.debug_logprobs   (needs a running ollama serve)
"""
import json

import pandas as pd
import requests

from run.runner import decision_schema, p_accept_from_logprobs

URL = "http://127.0.0.1:11434/api/chat"
t = pd.read_json("data/scenarios/trials.jsonl", lines=True, dtype=False)
s1 = t[(t.sub_exp == "S1") & ~t.extension & ~t.justify].groupby("offer_share").head(1).head(3)

for r in s1.to_dict("records"):
    for fmt_name, fmt in [("schema", decision_schema(r)), ("json", "json"), ("none", None)]:
        body = {"model": "llama3.1:8b-instruct-q4_K_M", "stream": False, "logprobs": True, "top_logprobs": 10,
                "messages": [{"role": "system", "content": r["system"]}, {"role": "user", "content": r["prompt"]}],
                "options": {"temperature": 1.0, "seed": 1, "num_predict": 20}}
        if fmt is not None:
            body["format"] = fmt
        d = requests.post(URL, json=body, timeout=300).json()
        print(f"\n=== {r['trial_id']}  format={fmt_name}  options={r['option_order']}")
        print("content:", repr(d["message"]["content"]))
        print("top-level keys:", list(d))
        lp = d.get("logprobs")
        for i, tok in enumerate((lp or [])[:12]):
            alts = ", ".join(f"{a['token']!r}:{a['logprob']:.2f}" for a in (tok.get("top_logprobs") or [])[:6])
            print(f"  {i:2d} {tok.get('token')!r:>14} {tok.get('logprob', 0):7.2f} | {alts}")
        print("parser p_accept:", p_accept_from_logprobs(lp, r["option_order"]))
print(json.dumps({"done": True}))
