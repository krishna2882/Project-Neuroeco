#!/usr/bin/env bash
# Pre-registered follow-up (event-free messages; docs/preregistration_followup.md) for one local model. Resumable.
# Only submit AFTER the pre-registration is approved (stimuli/followup/messages_frozen.csv is the frozen set),
# and the bank rebuilt:  python build_scenarios.py --fallback --messages stimuli/followup/messages_frozen.csv \
#                          --name followup --sub-exp S1 S2 S3b --no-baseline
#   sbatch --export=ALL,MODEL_KEY=qwen25_7b ada/run_followup.sbatch
#
#SBATCH --job-name=neuroeco-fu
#SBATCH --partition=u22
#SBATCH --account=research
#SBATCH --qos=medium
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=0-08:00:00
#SBATCH --output=slurm-%x-%j.out

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
: "${MODEL_KEY:?set MODEL_KEY}"
export OLLAMA_MODELS="$HOME/ollama_models" OLLAMA_HOST=127.0.0.1:11434 OLLAMA_KEEP_ALIVE=60m
"$HOME/ollama/bin/ollama" serve > "slurm-ollama-$SLURM_JOB_ID.log" 2>&1 &
OPID=$!
trap 'kill $OPID 2>/dev/null || true' EXIT
for i in $(seq 90); do curl -sf localhost:11434/api/version >/dev/null && break; sleep 2; done
R=".venv/bin/python -m run.runner --model $MODEL_KEY"
$R --bank followup_trials --tag followup --sub-exp S1 --logprobs
$R --bank followup_trials --tag followup --sub-exp S2 S3b
$R --bank followup_trials --tag followup --extension-only --logprobs
$R --bank followup_checks --tag followup_checks
$R --bank followup_checks --tag followup_checks --extension-only
echo "FOLLOW-UP COMPLETE FOR $MODEL_KEY"
