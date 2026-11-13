#!/usr/bin/env bash
# Extension 3: non-threatening anger (docs/preregistration_extension3.md). Resumable; completed trials are skipped.
# Only submit AFTER (1) the pre-registration is approved, frozen and pushed, (2) the ratings are in and
# stimuli/threat/select_nt.py has frozen the messages, (3) the banks are built:
#   python build_scenarios.py --fallback --messages stimuli/threat/messages_frozen.csv --name threat --sub-exp S1 S2 S3b --no-baseline
#   python stimuli/threat/build_probe.py
#   sbatch --export=ALL,MODEL_KEYS="qwen25_7b qwen25_14b llama31_8b" ada/run_ext3.sbatch
#
#SBATCH --job-name=neuroeco-ext3
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
  R=".venv/bin/python -m run.runner --model $K"
  $R --bank threat_trials --tag threat --sub-exp S3b          # confirmatory decisions
  $R --bank threat_checks --tag threat_checks --sub-exp S3b   # emotion recognition (manipulation check)
  $R --bank probe_threat --tag probe_threat                   # exploratory: does the model read it as a threat?
done
echo "EXT3 COMPLETE $MODEL_KEYS"
