#!/usr/bin/env bash
# S1 temperature-0.7 robustness subset for one model (tag temp07). Resumable.
#   sbatch --export=ALL,MODEL_KEY=llama31_8b ada/run_temp07.sbatch
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
.venv/bin/python -m run.runner --model "$MODEL_KEY" --tag temp07 --sub-exp S1 --temperature 0.7 --logprobs
echo "TEMP07 COMPLETE FOR $MODEL_KEY"
