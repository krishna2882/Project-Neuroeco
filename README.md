# Project Neuroeco — Emotional framing and reciprocity in LLM economic decisions

Krishna Goel · Devansh Magotra. Design: `Team_10-1.pdf` (source of truth). Handoff notes: `PROJECT_STATUS.md`.

Does a counterpart's expressed emotion (Neutral / Angry / Sad / Happy, or no message) change an LLM's
decisions in the Ultimatum, Dictator and Trust games when payoffs are identical, and does the
direction of the change match human neuroeconomic findings?

## Layout

| Path | What |
|---|---|
| `config.py` | Every design constant (cells, stakes, offers, sampling depth, models, seeds) |
| `stimuli/messages_candidates.csv` | 32 candidate messages (8 per emotion) |
| `stimuli/freeze_messages.py` | Automatic screen + selection of 5/emotion → `messages_frozen.csv`; writes the peer-rating form |
| `stimuli/paraphrases.py` | 4 paraphrases × 5 game types (S1, S2-UG, S2-DG, S3a, S3b) + system prompt |
| `build_scenarios.py` | 110 cells × 16 variants × 3 samples = 5,280 trials/model, plus 396 check calls/model |
| `run/clients.py`, `run/runner.py` | Ollama and xAI clients; resumable, append-only data collector |
| `analysis/` | GLMM (`glmm.py`), S1 MAO and Fehr–Schmidt (`s1.py`), S2/S3 LMMs (`s2s3.py`), checks, qualitative coding, H5, human benchmarks (`run_all.py`) |
| `analysis/simulate.py`, `analysis/validate.py` | Simulated data with known effects and a recovery check |
| `docs/literature_review.md` | Phase-1 literature review |
| `docs/protocol_decisions.md` | Protocol decisions D1–D14 that fill the paper's gaps (need joint sign-off) |
| `data/scenarios/` | Frozen scenario bank (JSONL) |
| `data/raw/<model>/<tag>.jsonl` | Raw call logs, one line per attempt |
| `results/<run>/report.md` | Generated tables, figures and the report |

## Reproduce

```bash
uv venv .venv -p 3.10 && uv pip install -p .venv pandas numpy scipy statsmodels matplotlib requests
```

```bash
.venv/bin/python stimuli/freeze_messages.py && .venv/bin/python build_scenarios.py
```

Validate the analysis pipeline on simulated data:

```bash
.venv/bin/python -m analysis.simulate && .venv/bin/python -m analysis.run_all --raw-dir data/sim/raw --out sim && .venv/bin/python -m analysis.validate
```

Data collection. The local model needs `ollama serve` with `llama3.1:8b-instruct-q4_K_M` pulled. The xAI
model needs `XAI_API_KEY=...` in `.env`.

```bash
.venv/bin/python -m run.runner --model llama31_8b --tag pilot --pilot
```

```bash
.venv/bin/python -m run.runner --model grok --tag main --workers 4
```

```bash
.venv/bin/python -m run.runner --model llama31_8b --bank checks --tag checks
```

Analysis of real data:

```bash
.venv/bin/python -m analysis.run_all --tag main --checks-tag checks --out main
```

Every runner command is resumable. Re-running the same command skips trials that already have a
valid record. If collection runs behind, run sub-experiments in priority order with `--sub-exp S1`,
then `S2`, then `S3a S3b`.
