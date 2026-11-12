#!/usr/bin/env bash
# Full collection for one local (Ollama) model on one Ada GPU:
#   pilot -> D11 ceiling/floor decision -> main S1 (with logprobs, +fallback cells) -> S2 -> S3 -> checks
#   -> S1 temperature-0.7 robustness subset.
# Resumable: if the job times out or is pre-empted, sbatch it again with the same MODEL_KEY.
#
#   sbatch --export=ALL,MODEL_KEY=qwen25_7b ada/run_model.sbatch
#
#SBATCH --job-name=neuroeco-model
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
: "${MODEL_KEY:?set MODEL_KEY, e.g. sbatch --export=ALL,MODEL_KEY=qwen25_7b ada/run_model.sbatch}"
export OLLAMA_MODELS="$HOME/ollama_models" OLLAMA_HOST=127.0.0.1:11434 OLLAMA_KEEP_ALIVE=60m
PY=.venv/bin/python
R="$PY -m run.runner --model $MODEL_KEY"
echo "MODEL_KEY=$MODEL_KEY"
nvidia-smi --query-gpu=name,memory.total --format=csv
"$HOME/ollama/bin/ollama" serve > "slurm-ollama-$SLURM_JOB_ID.log" 2>&1 &
OPID=$!
trap 'kill $OPID 2>/dev/null || true' EXIT
for i in $(seq 90); do curl -sf localhost:11434/api/version >/dev/null && break; sleep 2; done
curl -s localhost:11434/api/version; echo

$R --tag pilot_ada --pilot --logprobs
$PY -m run.d11 pilot_ada "$MODEL_KEY"
FALLBACK=$(grep -c "fallback=True" "data/FALLBACK_DECISION_$MODEL_KEY.txt" || true)

$R --tag main --sub-exp S1 --logprobs
[ "$FALLBACK" -ge 1 ] && $R --tag main --extension-only --logprobs
$R --tag main --sub-exp S2
$R --tag main --sub-exp S3a S3b
$R --bank checks --tag checks
[ "$FALLBACK" -ge 1 ] && $R --bank checks --tag checks --extension-only
$R --tag temp07 --sub-exp S1 --temperature 0.7 --logprobs
echo "ALL COLLECTION COMPLETE FOR $MODEL_KEY"
