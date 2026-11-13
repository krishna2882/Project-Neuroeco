#!/usr/bin/env bash
# Local-model (Llama-3.1-8B via Ollama) data collection on one Ada GPU:
#   pilot -> D11 ceiling/floor decision -> main S1 (+fallback cells) -> S2 -> S3 -> manipulation checks.
# Every step is resumable: if the job times out or is pre-empted, sbatch it again.
#
#   cd ~/projects/neuroeco && sbatch ada/run_local.sbatch
#
#SBATCH --job-name=neuroeco-llama
#SBATCH --partition=u22
#SBATCH --account=research
#SBATCH --qos=medium
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=2-00:00:00
#SBATCH --output=slurm-%x-%j.out

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
export OLLAMA_MODELS="$HOME/ollama_models" OLLAMA_HOST=127.0.0.1:11434 OLLAMA_KEEP_ALIVE=60m
PY=.venv/bin/python
R="$PY -m run.runner --model llama31_8b"

nvidia-smi --query-gpu=name,memory.total --format=csv
"$HOME/ollama/bin/ollama" serve > "slurm-ollama-$SLURM_JOB_ID.log" 2>&1 &
OPID=$!
trap 'kill $OPID 2>/dev/null || true' EXIT
for i in $(seq 90); do curl -sf localhost:11434/api/version >/dev/null && break; sleep 2; done
curl -s localhost:11434/api/version; echo

# Pilot on this runtime (with logprobs), then the D11 decision
$R --tag pilot_ada --pilot --logprobs
$PY -m run.d11 pilot_ada
FALLBACK=$(grep -c "fallback=True" data/FALLBACK_DECISION.txt || true)

# Main run in the approach paper's priority order (S1, then S2, then S3)
$R --tag main --sub-exp S1 --logprobs
[ "$FALLBACK" -ge 1 ] && $R --tag main --extension-only --logprobs
$R --tag main --sub-exp S2
$R --tag main --sub-exp S3a S3b
$R --bank checks --tag checks
[ "$FALLBACK" -ge 1 ] && $R --bank checks --tag checks --extension-only
echo "ALL LOCAL-MODEL COLLECTION COMPLETE"
