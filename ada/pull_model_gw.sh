#!/usr/bin/env bash
# Gateway-only: pull an Ollama model into ~/ollama_models, then submit its collection job.
#   nohup bash ada/pull_model_gw.sh qwen2.5:7b-instruct-q4_K_M qwen25_7b > pull_qwen.log 2>&1 &
set -euo pipefail
TAG=$1; KEY=$2
cd ~/projects/neuroeco
export OLLAMA_MODELS=~/ollama_models OLLAMA_HOST=127.0.0.1:11556
~/ollama/bin/ollama serve > ~/ollama_gw_pull.log 2>&1 &
SP=$!; sleep 8
~/ollama/bin/ollama pull "$TAG"
~/ollama/bin/ollama list
kill $SP
sbatch --export=ALL,MODEL_KEY="$KEY" ada/run_model.sbatch
echo PULL_AND_SUBMIT_DONE
