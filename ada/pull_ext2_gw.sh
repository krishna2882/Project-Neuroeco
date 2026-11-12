#!/usr/bin/env bash
# Gateway-only: pull the three extension-2 models, then submit the four extension-2 jobs.
#   setsid nohup bash ada/pull_ext2_gw.sh > pull_ext2.log 2>&1 < /dev/null & disown
set -euo pipefail
cd ~/projects/neuroeco
export OLLAMA_MODELS=~/ollama_models OLLAMA_HOST=127.0.0.1:11556
~/ollama/bin/ollama serve > ~/ollama_gw_pull.log 2>&1 &
SP=$!; sleep 8
for TAG in qwen2.5:3b-instruct-q4_K_M qwen2.5:14b-instruct-q4_K_M qwen2.5:7b-instruct-q8_0; do
  ~/ollama/bin/ollama pull "$TAG"
done
~/ollama/bin/ollama list
kill $SP
# comprehension for the existing models first (shortest), then the model runs
sbatch --export=ALL,MODE=comp,MODEL_KEYS="llama31_8b qwen25_7b" ada/run_ext2.sbatch
sbatch --export=ALL,MODE=scale,MODEL_KEY=qwen25_3b ada/run_ext2.sbatch
sbatch --export=ALL,MODE=q8,MODEL_KEY=qwen25_7b_q8 ada/run_ext2.sbatch
sbatch --export=ALL,MODE=scale,MODEL_KEY=qwen25_14b ada/run_ext2.sbatch
echo PULL_AND_SUBMIT_DONE
