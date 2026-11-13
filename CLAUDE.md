# Project Neuroeco — notes for Claude

Study: does a counterpart's expressed emotion (Neutral/Angry/Sad/Happy or no message) shift LLM decisions in
Ultimatum / Dictator / Trust games at fixed payoffs? Authors: Krishna Goel, Devansh Magotra. Presentation Nov 10, 2026.

- **Source of truth for the design:** `Team_10-1.pdf`. Gaps it leaves are filled in `docs/protocol_decisions.md`;
  every deviation from it is logged in `docs/plan_update.md` — add to that table if you change the plan.
- **Current results:** `docs/results_summary.md` (one page), `results/main/report.md` (full).
- **Layout:** `config.py` (all design constants + model registry) · `stimuli/` (messages, paraphrases) ·
  `build_scenarios.py` → `data/scenarios/` · `run/runner.py` (resumable, append-only collector; `run/clients.py`)
  · `analysis/` (`run_all.py` drives everything) · `ada/` (cluster scripts) · `README.md` (commands).
- **Python:** always use `.venv/bin/python` (laptop) — system Python lacks statsmodels.

## Data collection (open-weight models run on Ada, not the laptop)
- Ada general setup: see `~/.claude/CLAUDE.md`. This project lives at `~/projects/neuroeco` on Ada.
- New local model: add it to `MODELS` in `config.py`, `bash ada/sync.sh push`, then on the gateway
  `setsid nohup bash ada/pull_model_gw.sh <ollama-tag> <model_key> > pull_<key>.log 2>&1 < /dev/null & disown`
  (pulls the model, then submits `ada/run_model.sbatch`: pilot → D11 → S1 (logprobs) → S2 → S3 → checks → T=0.7 S1).
- Rerun / resume a model: `sbatch --export=ALL,MODEL_KEY=<key> ada/run_model.sbatch` (completed trials are skipped).
- Bring data back: `bash ada/sync.sh pull`; then `.venv/bin/python -m analysis.run_all --tag main --checks-tag checks --out main`.
- Do NOT `sync.sh push` while a job is running from `~/projects/neuroeco`.

## Things to know
- Models done (all 6,240 decisions each): `llama31_8b`, `qwen25_7b` (Ada; incl. `temp07`), `mistral` (Mistral Large 4 via
  free API from the laptop: `bash run/run_api_model.sh mistral 22`; reasoning model; 20k tokens/min cap; free budget ran
  out during checks → 106/468 checks). Llama's S1 logprobs live in tag `main_lp` (first-run values mis-parsed, ignored).
- xAI key in `.env` is valid but the team has no credits (403); `--model grok` works once topped up.
- Secrets live only in `.env` (gitignored-by-convention, chmod 600, excluded from Ada sync). Never print or write keys
  yourself; ask the user to add them (e.g. `read -rsp` one-liner).
- Message set is a *provisional* freeze (human peer rating pending); changing `stimuli/messages_frozen.csv` requires
  rebuilding the bank and re-collecting — don't do it casually.
- **Follow-up study (pre-registered, not yet run):** event-free messages in `stimuli/followup/`; pre-registration
  `docs/preregistration_followup.md` must be approved (and its SHA-256 recorded) BEFORE running. Order: peer ratings
  (`stimuli/PEER_RATING_INSTRUCTIONS.md`, `analysis/import_ratings.py`) → `freeze_messages.py --dir stimuli/followup` →
  rebuild `followup_*` bank (command in `ada/run_followup.sbatch`) → `sync.sh push` → sbatch per model → analyse with
  `run_all --bank-prefix followup --tag followup --checks-tag followup_checks --out followup`.
- Sensitivity analysis for messages flagged by raters: `run_all --exclude-msgs <ids> --out main_excl`.
- Study-wide correction and forest plot: `python -m analysis.forest`; stricter refit with message as a random factor (preferred for claims, P12): `python -m analysis.message_re --out main` (and `--out followup`), then equivalence tests + pooled estimates (P14): `python -m analysis.equivalence`; draft pre-registration for extension 2 (scale/comprehension/Q8): `docs/preregistration_extension2.md` (needs both sign-offs before any run); Mistral reasoning-text coding: `python -m analysis.thinking`.
- Extension 2 done (13 Nov): `qwen25_3b`, `qwen25_14b` (full bank), `qwen25_7b_q8` (S1, S3b), comprehension for 4 models; `python -m analysis.ext2` → `results/ext2/confirmatory.md`.
- Peer ratings imported (13 Nov, 9 raters): `results/peer_rating_summary.md`; sensitivity `results/main_excl`, `results/followup_excl` (Ada: `PART=main|followup sbatch ada/run_sensitivity.sbatch`); threat check `python -m analysis.threat`.
- Extension 3 (non-threatening anger): pre-registration FROZEN 13 Nov but NOT RUN (P17; decided before any ratings/data). If ever run, order: rating form `stimuli/threat/create_form_threat.gs` (>= 8 raters) → `import_ratings --key stimuli/threat/rating_key_threat.csv --name threat <csv>` → `python stimuli/threat/select_nt.py` → build banks (commands in `ada/run_ext3.sbatch`) → push → sbatch → `python -m analysis.ext3`.
- Valuation curves from log-probs (P18): `python -m analysis.value_signal` → `results/value_signal/`; neuro analogy table for slides: `docs/neuro_mapping.md`.
- Still open for the humans: peer rating, qualitative coding (`python -m analysis.qualitative sheet|kappa`),
  sign-off on protocol decisions, verifying † citations in `docs/literature_review.md`.
