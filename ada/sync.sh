#!/usr/bin/env bash
# push code (never while a job is running from this folder) | pull raw data + logs back to the laptop
#   bash ada/sync.sh push|pull
set -euo pipefail
GW=krishna.goel@ada-gw1.iiit.ac.in; DIR=projects/neuroeco
cd "$(dirname "$0")/.."
case "${1:-pull}" in
  push) rsync -az --exclude .venv --exclude data/sim --exclude data/raw --exclude results --exclude __pycache__ \
              --exclude .env --exclude 'logs_*' --exclude '*.pdf' --exclude wheels ./ $GW:$DIR/ ;;
  pull) rsync -az $GW:$DIR/data/raw/ data/raw/ && rsync -az $GW:$DIR/data/FALLBACK_DECISION.txt data/ 2>/dev/null || true
        mkdir -p logs_ada && rsync -az "$GW:$DIR/slurm-*" logs_ada/ 2>/dev/null || true ;;
esac
