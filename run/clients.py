"""Thin model clients with a common interface:

    client.chat(system, prompt, schema, seed, temperature) -> dict(content, meta)

Both clients ask for schema-constrained JSON output. Exact model identifiers are returned in
`meta` and logged per call.
"""
import os
import threading
import time

import requests

from config import ROOT


def load_env():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


class OllamaClient:
    def __init__(self, model, base_url, num_ctx=2048, num_predict=160):
        self.model, self.base_url = model, base_url.rstrip("/")
        self.num_ctx, self.num_predict = num_ctx, num_predict
        info = requests.post(f"{self.base_url}/api/show", json={"model": model}, timeout=60).json()
        tags = requests.get(f"{self.base_url}/api/tags", timeout=60).json()
        digest = next((m["digest"] for m in tags.get("models", []) if m["name"] == model), None)
        ver = requests.get(f"{self.base_url}/api/version", timeout=10).json().get("version")
        self.version_string = f"ollama:{model}@{(digest or '')[:12]} (runtime {ver}, " \
                              f"{info.get('details', {}).get('quantization_level')})"

    def chat(self, system, prompt, schema, seed, temperature, logprobs=False):
        body = {
            "model": self.model, "stream": False, "format": schema, "keep_alive": "60m",
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            "options": {"temperature": temperature, "seed": seed, "num_ctx": self.num_ctx,
                        "num_predict": self.num_predict},
        }
        if logprobs:  # supported from Ollama 0.12.11; silently ignored by older runtimes
            body.update(logprobs=True, top_logprobs=10)
        t0 = time.time()
        r = requests.post(f"{self.base_url}/api/chat", json=body, timeout=900)
        r.raise_for_status()
        d = r.json()
        return dict(content=d["message"]["content"], meta=dict(
            model_version=self.version_string, latency_s=round(time.time() - t0, 3),
            prompt_tokens=d.get("prompt_eval_count"), completion_tokens=d.get("eval_count"),
            finish_reason=d.get("done_reason"), logprobs=d.get("logprobs")))


PROVIDERS = {
    # provider: (env var holding the key, name of the sampling-seed parameter)
    "xai": ("XAI_API_KEY", "seed"),
    "mistral": ("MISTRAL_API_KEY", "random_seed"),
}


class APIClient:
    """Hosted model behind an OpenAI-compatible chat-completions API (xAI, Mistral).

    min_interval: minimum seconds between request starts across all threads (free-tier rate limits)."""

    def __init__(self, provider, model, base_url, min_interval=0.0, reasoning_effort=None, max_tokens=400):
        load_env()
        env, self.seed_param = PROVIDERS[provider]
        key = os.environ.get(env)
        if not key:
            raise SystemExit(f"{env} not set: add it to Project Neuroeco/.env")
        self.provider, self.model, self.base_url = provider, model, base_url.rstrip("/")
        self.s = requests.Session()
        self.s.headers.update({"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        self.min_interval, self._next = min_interval, 0.0
        self.reasoning_effort, self.max_tokens = reasoning_effort, max_tokens
        self._lock = threading.Lock()

    def list_models(self):
        r = self.s.get(f"{self.base_url}/models", timeout=30)
        r.raise_for_status()
        return [m["id"] for m in r.json()["data"]]

    def _throttle(self):
        with self._lock:
            now = time.time()
            wait = self._next - now
            self._next = max(now, self._next) + self.min_interval
        if wait > 0:
            time.sleep(wait)

    def chat(self, system, prompt, schema, seed, temperature, logprobs=False):
        body = {
            "model": self.model, "temperature": temperature, self.seed_param: seed, "max_tokens": self.max_tokens,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            "response_format": {"type": "json_schema",
                                "json_schema": {"name": "answer", "schema": schema, "strict": True}},
        }
        if self.reasoning_effort:
            body["reasoning_effort"] = self.reasoning_effort
        if logprobs and self.provider == "xai":
            body.update(logprobs=True, top_logprobs=8)
        t0 = time.time()
        for attempt in range(8):  # transport-level retries (rate limits / 5xx); logged as one call
            self._throttle()
            r = self.s.post(f"{self.base_url}/chat/completions", json=body, timeout=120)
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(min(90, 2 ** attempt * 2))
                continue
            break
        if r.status_code >= 400:
            raise requests.HTTPError(f"{r.status_code}: {r.text[:300]}")
        d = r.json()
        ch = d["choices"][0]
        usage = d.get("usage", {})
        content, thinking = _split_content(ch["message"].get("content"))
        return dict(content=content, meta=dict(
            thinking=thinking,
            model_version=f"{self.provider}:{d.get('model', self.model)}"
                          + (f" fp={d['system_fingerprint']}" if d.get("system_fingerprint") else ""),
            latency_s=round(time.time() - t0, 3),
            prompt_tokens=usage.get("prompt_tokens"), completion_tokens=usage.get("completion_tokens"),
            reasoning_tokens=(usage.get("completion_tokens_details") or {}).get("reasoning_tokens"),
            finish_reason=ch.get("finish_reason"), logprobs=ch.get("logprobs")))


def _split_content(c):
    """Mistral reasoning models return a list of chunks ({type: thinking|text}); others a plain string.
    Returns (answer text, thinking text or None)."""
    if c is None:
        return "", None
    if isinstance(c, str):
        return c, None
    text, think = [], []
    for ch in c:
        if ch.get("type") == "text":
            text.append(ch.get("text", ""))
        elif ch.get("type") == "thinking":
            for t in ch.get("thinking") or []:
                think.append(t.get("text", "") if isinstance(t, dict) else str(t))
    return "".join(text), ("".join(think) or None)


def make_client(cfg, model_override=None):
    model = model_override or cfg["model"]
    if cfg["provider"] == "ollama":
        return OllamaClient(model, cfg["base_url"])
    if cfg["provider"] in PROVIDERS:
        return APIClient(cfg["provider"], model, cfg["base_url"], cfg.get("min_interval", 0.0),
                         cfg.get("reasoning_effort"), cfg.get("max_tokens", 400))
    raise ValueError(cfg["provider"])
