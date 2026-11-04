#!/usr/bin/env bash
# D11 fallback extension (5% / 45% S1 offer cells + their checks) for one local model. Resumable.
#   sbatch --export=ALL,MODEL_KEY=qwen25_7b ada/run_extension.sbatch
#
#SBATCH --job-name=neuroeco-ext
#SBATCH --partition=u22
#SBATCH --account=research
#SBATCH --qos=medium
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=0-04:00:00
#SBATCH --output=slurm-%x-%j.out

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
: "${MODEL_KEY:?set MODEL_KEY}"
export OLLAMA_MODELS="$HOME/ollama_models" OLLAMA_HOST=127.0.0.1:11434 OLLAMA_KEEP_ALIVE=60m
"$HOME/ollama/bin/ollama" serve > "slurm-ollama-$SLURM_JOB_ID.log" 2>&1 &
OPID=$!
trap 'kill $OPID 2>/dev/null' EXIT
for i in $(seq 90); do curl -sf localhost:11434/api/version >/dev/null && break; sleep 2; done
R=".venv/bin/python -m run.runner --model $MODEL_KEY"
$R --tag main --extension-only --logprobs
$R --bank checks --tag checks --extension-only
echo "EXTENSION COMPLETE FOR $MODEL_KEY"
