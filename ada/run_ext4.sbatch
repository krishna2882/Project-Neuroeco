#!/usr/bin/env bash
# Extension 4: stress tests (docs/preregistration_extension4.md). Resumable; completed trials are skipped.
# Only submit AFTER the pre-registration is approved, frozen and pushed, and the banks are built:
#   python build_ext4.py
#   sbatch --export=ALL,MODEL_KEYS="qwen25_7b llama31_8b qwen25_14b" ada/run_ext4.sbatch
# About 5,300 decisions + 128 mood-probe items per model (Qwen-7B / Llama: well under 1 h; Qwen-14B: about 1-2 h).
#
#SBATCH --job-name=neuroeco-ext4
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
: "${MODEL_KEYS:?set MODEL_KEYS}"
export OLLAMA_MODELS="$HOME/ollama_models" OLLAMA_HOST=127.0.0.1:11434 OLLAMA_KEEP_ALIVE=60m
"$HOME/ollama/bin/ollama" serve > "slurm-ollama-$SLURM_JOB_ID.log" 2>&1 &
OPID=$!
trap 'kill $OPID 2>/dev/null || true' EXIT
for i in $(seq 90); do curl -sf localhost:11434/api/version >/dev/null && break; sleep 2; done
for K in $MODEL_KEYS; do
  R=".venv/bin/python -m run.runner --model $K --bank ext4_trials --tag ext4"
  $R --module O D --logprobs        # ultimatum formats + dominance checks (graded P(accept) from log-probs)
  $R --module I X                   # injection / pressure messages, incidental mood
  .venv/bin/python -m run.runner --model $K --bank probe_ext4_mood --tag probe_ext4_mood   # mood manipulation check
done
echo "EXT4 COMPLETE $MODEL_KEYS"
