#!/usr/bin/env bash
# Temperature-0.7 robustness for the WHOLE main bank (P20, exploratory): completes tag temp07 with the S1 5%/45% cells,
# S2, S3a and S3b, same prompts and seeds as the T = 1.0 main run. Resumable; the S1 10-50% cells done earlier are skipped.
#   sbatch --export=ALL,MODEL_KEY=qwen25_7b ada/run_temp07_full.sbatch
#
#SBATCH --job-name=neuroeco-t07
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
: "${MODEL_KEY:?set MODEL_KEY}"
export OLLAMA_MODELS="$HOME/ollama_models" OLLAMA_HOST=127.0.0.1:11434 OLLAMA_KEEP_ALIVE=60m
"$HOME/ollama/bin/ollama" serve > "slurm-ollama-$SLURM_JOB_ID.log" 2>&1 &
OPID=$!
trap 'kill $OPID 2>/dev/null || true' EXIT
for i in $(seq 90); do curl -sf localhost:11434/api/version >/dev/null && break; sleep 2; done
R=".venv/bin/python -m run.runner --model $MODEL_KEY --tag temp07 --temperature 0.7"
$R --sub-exp S1 --logprobs
$R --extension-only --logprobs
$R --sub-exp S2
$R --sub-exp S3a S3b
echo "TEMP07 FULL COMPLETE FOR $MODEL_KEY"
