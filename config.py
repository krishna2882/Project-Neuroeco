"""Design constants for the study. Source of truth: Team_10-1.pdf (approach paper).

Every number used by the scenario builder, runner and analysis lives here so
that the design can be audited in one place.
"""
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
MODELS = {
    "llama31_8b": {
        "provider": "ollama",
        "model": "llama3.1:8b-instruct-q4_K_M",
        "base_url": "http://127.0.0.1:11434",
    },
    "qwen25_7b": {
        "provider": "ollama",
        "model": "qwen2.5:7b-instruct-q4_K_M",
        "base_url": "http://127.0.0.1:11434",
    },
    # Extension 2 (docs/preregistration_extension2.md): Qwen size ladder and an 8-bit check
    "qwen25_3b": {
        "provider": "ollama",
        "model": "qwen2.5:3b-instruct-q4_K_M",
        "base_url": "http://127.0.0.1:11434",
    },
    "qwen25_14b": {
        "provider": "ollama",
        "model": "qwen2.5:14b-instruct-q4_K_M",
        "base_url": "http://127.0.0.1:11434",
    },
    "qwen25_7b_q8": {
        "provider": "ollama",
        "model": "qwen2.5:7b-instruct-q8_0",
        "base_url": "http://127.0.0.1:11434",
    },
    "mistral": {
        "provider": "mistral",
        "model": "mistral-large-4-0",  # Mistral Large 4 (~1T MoE, open weights Oct 2026; Medium/Small are 0 req/min on the free tier)
        "base_url": "https://api.mistral.ai/v1",
        "min_interval": 1.3,  # free tier: 50 req/min for Large 4
        "reasoning_effort": "low",  # reasoning cannot be disabled on Large 4; "low" is the minimum
        "max_tokens": 4000,  # room for thinking + the JSON answer
    },
    "grok": {
        "provider": "xai",
        "model": "grok-3-mini",  # overridden by --model-name if needed; pinned in logs
        "base_url": "https://api.x.ai/v1",
    },
}
