#!/usr/bin/env bash
# LAPTOP (Git Bash): copy the extension-4 raw data and Slurm logs back from Ada, then analyse.
#   ADA_USER=your.username bash ada/pull_ext4.sh && python -m analysis.ext4
set -euo pipefail
: "${ADA_USER:?set ADA_USER}"
GW="$ADA_USER@ada-gw1.iiit.ac.in"
cd "$(dirname "$0")/.."
for K in qwen25_7b llama31_8b qwen25_14b; do
  mkdir -p "data/raw/$K"
  for T in ext4 probe_ext4_mood; do
    scp "$GW:projects/neuroeco/data/raw/$K/$T.jsonl" "data/raw/$K/" 2>/dev/null && echo "got $K/$T" || echo "missing $K/$T"
  done
done
mkdir -p logs_ada && scp "$GW:projects/neuroeco/slurm-*ext4*" logs_ada/ 2>/dev/null || true
