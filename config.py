"""Design constants for the study. Source of truth: Team_10-1.pdf (approach paper).

Every number used by the scenario builder, runner and analysis lives here so
that the design can be audited in one place.
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STIM_DIR = ROOT / "stimuli"
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROC_DIR = DATA_DIR / "processed"
RESULTS_DIR = ROOT / "results"

MASTER_SEED = 20260912  # project start date; every RNG derives from this

EMOTIONS = ["neutral", "angry", "sad", "happy"]
BASELINE = "none"  # no-message baseline condition label

STAKES = [100, 10_000]  # INR

# S1 UG-responder: offer as share of pie
S1_OFFERS = [0.10, 0.20, 0.30, 0.40, 0.50]
S1_FALLBACK_OFFERS = [0.05, 0.45]  # pre-registered ceiling/floor extension

# S2 UG vs DG proposer
S2_GAMES = ["UG", "DG"]

# S3a TG-trustee: share of investor endowment sent (multiplied by 3)
S3A_SENT = [0.20, 0.50, 1.00]
TG_MULTIPLIER = 3

N_PARAPHRASES = 4
N_MSG_VARIANTS_AVAILABLE = 5
N_MSG_VARIANTS_PER_CELL = 4
N_SAMPLES = 3
JUSTIFICATION_RATE = 0.20

TEMPERATURE = 1.0
ROBUSTNESS_TEMPERATURE = 0.7

# Models (exact version strings are also logged per call)
OLLAMA_URL = os.environ.get("NEUROECO_OLLAMA_URL", "http://127.0.0.1:11434")  # per-job port on shared nodes
MODELS = {
    "llama31_8b": {
        "provider": "ollama",
        "model": "llama3.1:8b-instruct-q4_K_M",
        "base_url": OLLAMA_URL,
    },
    "qwen25_7b": {
        "provider": "ollama",
        "model": "qwen2.5:7b-instruct-q4_K_M",
        "base_url": OLLAMA_URL,
    },
    # Extension 2 (docs/preregistration_extension2.md): Qwen size ladder and an 8-bit check
    "qwen25_3b": {
        "provider": "ollama",
        "model": "qwen2.5:3b-instruct-q4_K_M",
        "base_url": OLLAMA_URL,
    },
    "qwen25_14b": {
        "provider": "ollama",
        "model": "qwen2.5:14b-instruct-q4_K_M",
        "base_url": OLLAMA_URL,
    },
    "qwen25_7b_q8": {
        "provider": "ollama",
        "model": "qwen2.5:7b-instruct-q8_0",
        "base_url": OLLAMA_URL,
    },
    "mistral": {
        "provider": "mistral",
        "model": "mistral-large-4-0",  # Mistral Large 4 (~1T MoE, open weights Oct 2026; Medium/Small are 0 req/min on the free tier)
        "base_url": "https://api.mistral.ai/v1",
        "min_interval": 1.3,  # free tier: 50 req/min for Large 4
        "reasoning_effort": "low",  # reasoning cannot be disabled on Large 4; "low" is the minimum
        "max_tokens": 4000,  # room for thinking + the JSON answer
    },
    # Extension 4 on larger API models (free tiers; see docs/plan_update.md P24)
    "gptoss_120b": {
        "provider": "groq",
        "model": "openai/gpt-oss-120b",  # 120B open-weight MoE (OpenAI), always reasons
        "base_url": "https://api.groq.com/openai/v1",
        "min_interval": 3.5,  # 8,000 tokens/min on the free tier
        "reasoning_effort": "low",
        "max_tokens": 2000,
    },
    "qwen38_27b": {
        "provider": "groq",
        "model": "qwen/qwen3.8-27b",
        "base_url": "https://api.groq.com/openai/v1",
        "min_interval": 3.5,
        "max_tokens": 2000,
    },
    "gemini_flash": {
        "provider": "gemini",
        "model": "gemini-3.6-flash",  # closed model (Google); exact version logged per call
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "min_interval": 6.5,  # free-tier requests/minute
        "reasoning_effort": "low",
        "max_tokens": 2000,
    },
    # Extension 7: new model families on Ada (docs/preregistration_extension7.md); 4-bit builds like the others
    "gemma3_12b": {"provider": "ollama", "model": "gemma3:12b-it-q4_K_M", "base_url": OLLAMA_URL},       # Google
    "gemma3_4b": {"provider": "ollama", "model": "gemma3:4b-it-q4_K_M", "base_url": OLLAMA_URL},         # Google
    "mistral_nemo_12b": {"provider": "ollama", "model": "mistral-nemo:12b-instruct-2407-q4_K_M", "base_url": OLLAMA_URL},
    "phi4_14b": {"provider": "ollama", "model": "phi4:14b-q4_K_M", "base_url": OLLAMA_URL},              # Microsoft
    "granite33_8b": {"provider": "ollama", "model": "granite3.3:8b", "base_url": OLLAMA_URL},            # IBM
    "llama32_3b": {"provider": "ollama", "model": "llama3.2:3b-instruct-q4_K_M", "base_url": OLLAMA_URL},  # Meta
    "grok": {
        "provider": "xai",
        "model": "grok-3-mini",  # overridden by --model-name if needed; pinned in logs
        "base_url": "https://api.x.ai/v1",
    },
}
