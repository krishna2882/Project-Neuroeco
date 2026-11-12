#!/usr/bin/env bash
# Extension 2 (docs/preregistration_extension2.md, frozen 12 Nov 2026). Resumable: re-submit with the same variables.
#   MODE=scale MODEL_KEY=qwen25_3b|qwen25_14b   E1: full frozen main bank (+5%/45% cells, S1 logprobs) + checks + E2 items
#   MODE=q8    MODEL_KEY=qwen25_7b_q8           E3: main-bank S1 (+5%/45% cells, logprobs) and S3b
#   MODE=comp  MODEL_KEYS="llama31_8b qwen25_7b" E2: comprehension items only
#   sbatch --export=ALL,MODE=scale,MODEL_KEY=qwen25_14b ada/run_ext2.sbatch
#
#SBATCH --job-name=neuroeco-ext2
#SBATCH --partition=u22
#SBATCH --account=research
#SBATCH --qos=medium
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=1-00:00:00
#SBATCH --output=slurm-%x-%j.out

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
: "${MODE:?set MODE=scale|q8|comp}"
export OLLAMA_MODELS="$HOME/ollama_models" OLLAMA_HOST=127.0.0.1:11434 OLLAMA_KEEP_ALIVE=60m
PY=.venv/bin/python
nvidia-smi --query-gpu=name,memory.total --format=csv
"$HOME/ollama/bin/ollama" serve > "slurm-ollama-$SLURM_JOB_ID.log" 2>&1 &
OPID=$!
trap 'kill $OPID 2>/dev/null || true' EXIT
for i in $(seq 90); do curl -sf localhost:11434/api/version >/dev/null && break; sleep 2; done
curl -s localhost:11434/api/version; echo

case "$MODE" in
  scale)
    R="$PY -m run.runner --model $MODEL_KEY"
    $R --tag main --sub-exp S1 --logprobs
    $R --tag main --extension-only --logprobs
    $R --tag main --sub-exp S2
    $R --tag main --sub-exp S3a S3b
    $R --bank checks --tag checks
    $R --bank checks --tag checks --extension-only
    $R --bank comprehension --tag comprehension
    ;;
  q8)
    R="$PY -m run.runner --model $MODEL_KEY"
    $R --tag main --sub-exp S1 --logprobs
    $R --tag main --extension-only --logprobs
    $R --tag main --sub-exp S3b
    ;;
  comp)
    for K in $MODEL_KEYS; do $PY -m run.runner --model "$K" --bank comprehension --tag comprehension; done
    ;;
  *) echo "unknown MODE=$MODE"; exit 1 ;;
esac
echo "EXT2 $MODE COMPLETE ${MODEL_KEY:-$MODEL_KEYS}"
