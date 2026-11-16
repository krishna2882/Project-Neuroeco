#!/usr/bin/env bash
# Extension 7 (docs/preregistration_extension7.md). One job per model; the model is pulled to node-local /scratch (compute
# nodes have internet), so the home quota does not matter. Resumable: completed trials are skipped.
# Only submit AFTER the pre-registration is approved, frozen and pushed.
#   New model (families G and N):   sbatch --export=ALL,MODEL_KEY=gemma3_12b,PARTS="ext4 ext5 ext7" ada/run_ext7.sbatch
#   Original model (family N only): sbatch --export=ALL,MODEL_KEY=qwen25_7b,PARTS="ext7" ada/run_ext7.sbatch
#
#SBATCH --job-name=neuroeco-ext7
#SBATCH --partition=u22
#SBATCH --account=research
#SBATCH --qos=medium
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=0-10:00:00
#SBATCH --output=slurm-%x-%j.out

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
: "${MODEL_KEY:?set MODEL_KEY}" "${PARTS:?set PARTS, e.g. \"ext4 ext5 ext7\"}"
PORT=$((11500 + SLURM_JOB_ID % 400))
export OLLAMA_MODELS=/scratch/$USER/ollama_models OLLAMA_HOST=127.0.0.1:$PORT OLLAMA_KEEP_ALIVE=60m
export NEUROECO_OLLAMA_URL=http://127.0.0.1:$PORT
mkdir -p "$OLLAMA_MODELS"
"$HOME/ollama/bin/ollama" serve > "slurm-ollama-$SLURM_JOB_ID.log" 2>&1 &
OPID=$!
trap 'kill $OPID 2>/dev/null || true' EXIT
for i in $(seq 90); do curl -sf localhost:$PORT/api/version >/dev/null && break; sleep 2; done
hostname; nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
TAG=$(.venv/bin/python -c "from config import MODELS; print(MODELS['$MODEL_KEY']['model'])")
"$HOME/ollama/bin/ollama" pull "$TAG" > /dev/null 2>&1
"$HOME/ollama/bin/ollama" list
RUN=".venv/bin/python -m run.runner --model $MODEL_KEY"
for P in $PARTS; do
  case $P in
    ext4)
      $RUN --bank ext4_trials --tag ext4 --module O D --logprobs
      $RUN --bank ext4_trials --tag ext4 --module I X
      $RUN --bank probe_ext4_mood --tag probe_ext4_mood ;;
    ext5)
      $RUN --bank ext5_trials --tag ext5 --module R F --logprobs
      $RUN --bank ext5_trials --tag ext5 --module P
      $RUN --bank probe_ext5_mood --tag probe_ext5_mood ;;
    ext7)
      $RUN --bank ext7_trials --tag ext7 --logprobs
      $RUN --bank probe_ext7_mood --tag probe_ext7_mood ;;
  esac
done
echo "EXT7 COMPLETE $MODEL_KEY $PARTS"
