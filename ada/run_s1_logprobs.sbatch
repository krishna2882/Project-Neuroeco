#!/usr/bin/env bash
# Re-collect S1 token log-probabilities (graded DV) with the fixed parser; same prompts and seeds as
# the main run, stored under tag main_lp and merged into the main data at analysis time.
#
#   cd ~/projects/neuroeco && sbatch ada/run_s1_logprobs.sbatch
#
#SBATCH --job-name=neuroeco-s1lp
#SBATCH --partition=u22
#SBATCH --account=research
#SBATCH --qos=medium
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=0-06:00:00
#SBATCH --output=slurm-%x-%j.out

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
export OLLAMA_MODELS="$HOME/ollama_models" OLLAMA_HOST=127.0.0.1:11434 OLLAMA_KEEP_ALIVE=60m
"$HOME/ollama/bin/ollama" serve > "slurm-ollama-$SLURM_JOB_ID.log" 2>&1 &
OPID=$!
trap 'kill $OPID 2>/dev/null || true' EXIT
for i in $(seq 90); do curl -sf localhost:11434/api/version >/dev/null && break; sleep 2; done
.venv/bin/python -m run.runner --model llama31_8b --tag main_lp --sub-exp S1 --logprobs
echo "S1 LOGPROB PASS COMPLETE"
