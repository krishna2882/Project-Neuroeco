#!/usr/bin/env bash
# Extension 7 feasibility (NOT data): pull candidate models to node-local /scratch and run ~25 smoke trials each, to check
# that the tags exist, fit on the GPU and answer in the required JSON formats. Outputs: tag "zoo_smoke" (never analysed).
#   sbatch ada/zoo_check.sbatch
#SBATCH --job-name=neuroeco-zoo-check
#SBATCH --partition=u22
#SBATCH --account=research
#SBATCH --qos=medium
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=0-03:00:00
#SBATCH --output=slurm-%x-%j.out

set -uo pipefail
cd "$SLURM_SUBMIT_DIR"
PORT=$((11500 + SLURM_JOB_ID % 400))
export OLLAMA_MODELS=/scratch/$USER/ollama_models OLLAMA_HOST=127.0.0.1:$PORT OLLAMA_KEEP_ALIVE=10m
export NEUROECO_OLLAMA_URL=http://127.0.0.1:$PORT
mkdir -p "$OLLAMA_MODELS"
"$HOME/ollama/bin/ollama" serve > "slurm-ollama-$SLURM_JOB_ID.log" 2>&1 &
OPID=$!
trap 'kill $OPID 2>/dev/null || true' EXIT
for i in $(seq 90); do curl -sf localhost:$PORT/api/version >/dev/null && break; sleep 2; done
hostname; nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
for K in ${MODEL_KEYS:-gemma3_12b gemma3_4b mistral_nemo_12b phi4_14b granite33_8b llama32_3b}; do
  TAG=$(.venv/bin/python -c "from config import MODELS; print(MODELS['$K']['model'])")
  echo "=== $K $TAG"
  if ! "$HOME/ollama/bin/ollama" pull "$TAG" > /dev/null 2>&1; then echo "PULL FAILED $K $TAG"; continue; fi
  "$HOME/ollama/bin/ollama" list | grep -F "${TAG%%:*}"
  rm -f "data/raw/$K/zoo_smoke.jsonl" "data/raw/$K/zoo_smoke_probe.jsonl"
  .venv/bin/python -m run.runner --model "$K" --bank zoo_smoke_trials --tag zoo_smoke --logprobs 2>&1 | tail -2
  .venv/bin/python -m run.runner --model "$K" --bank zoo_smoke_probe --tag zoo_smoke_probe 2>&1 | tail -1
  .venv/bin/python - "$K" <<'PY'
import collections, json, sys
k = sys.argv[1]
for tag in ("zoo_smoke", "zoo_smoke_probe"):
    recs = [json.loads(l) for l in open(f"data/raw/{k}/{tag}.jsonl")]
    print(k, tag, len(recs), dict(collections.Counter(r["status"] for r in recs)),
          "first-attempt ok:", sum(r["status"] == "ok" and r["attempt"] == 1 for r in recs),
          "lp:", sum(r.get("p_accept_lp") is not None for r in recs),
          "mean latency %.1fs" % (sum(r.get("latency_s", 0) for r in recs) / max(len(recs), 1)))
    for r in recs:
        if r["status"] != "ok":
            print("   ERR", r["trial_id"], str(r.get("error"))[:160], "| raw:", str(r.get("raw"))[:120])
PY
  nvidia-smi --query-gpu=memory.used --format=csv,noheader
done
du -sh "$OLLAMA_MODELS"
echo "ZOO CHECK COMPLETE"
