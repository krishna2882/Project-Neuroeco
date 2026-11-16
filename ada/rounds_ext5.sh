#!/usr/bin/env bash
# ADA GATEWAY: run extension 5 in two rounds because of the home-directory quota (compute nodes only see the home).
#   Round 1: Qwen2.5-14B (already pulled). Meanwhile pull Qwen2.5-7B.
#   Round 2: after round 1 completes cleanly, remove Qwen-14B, pull Llama-3.1-8B, run Qwen-7B and Llama.
#   cd ~/projects/neuroeco && nohup bash ada/rounds_ext5.sh > rounds_ext5.log 2>&1 &
# Only run AFTER the pre-registration is frozen and pushed.
set -euo pipefail
cd ~/projects/neuroeco
OL=~/ollama/bin/ollama
export OLLAMA_MODELS=~/ollama_models OLLAMA_HOST=127.0.0.1:11559

gw_ollama() {  # run ollama client commands against a temporary server on the gateway (internet is only here)
  "$OL" serve > ~/ollama_gw_ext5.log 2>&1 &
  local sp=$!
  for i in $(seq 30); do curl -sf localhost:11559/api/version >/dev/null && break; sleep 2; done
  "$@"
  kill $sp 2>/dev/null || true
  wait $sp 2>/dev/null || true
}
submit() { sbatch --parsable -A research --qos=medium --export=ALL,MODEL_KEYS="$1" ada/run_ext5.sbatch; }
wait_job() { while squeue -h -j "$1" 2>/dev/null | grep -q .; do sleep 60; done; }

J1=$(submit "qwen25_14b")
echo "ROUND1 SUBMITTED job $J1 $(date)"
gw_ollama "$OL" pull qwen2.5:7b-instruct-q4_K_M
wait_job "$J1"
if ! grep -q "EXT5 COMPLETE" "slurm-neuroeco-ext5-$J1.out"; then
  echo "ROUND1 DID NOT COMPLETE - not deleting models, not starting round 2 $(date)"; exit 1
fi
echo "ROUND1 COMPLETE $(date)"
gw_ollama bash -c "$OL rm qwen2.5:14b-instruct-q4_K_M && $OL pull llama3.1:8b-instruct-q4_K_M && $OL list"
J2=$(submit "qwen25_7b llama31_8b")
echo "ROUND2 SUBMITTED job $J2 $(date)"
wait_job "$J2"
grep -q "EXT5 COMPLETE" "slurm-neuroeco-ext5-$J2.out" && echo "ROUND2 COMPLETE $(date)" || echo "ROUND2 DID NOT COMPLETE $(date)"
