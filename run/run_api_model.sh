#!/usr/bin/env bash
# Full collection for a hosted API model from the laptop: pilot -> D11 -> S1 -> S2 -> S3 -> checks.
# Resumable. Wrapped in systemd-inhibit so idle sleep can't interrupt it (a closed lid still sleeps).
#   systemd-inhibit --what=sleep:idle --why="Neuroeco API run" bash run/run_api_model.sh mistral 10
set -euo pipefail
cd "$(dirname "$0")/.."
KEY=$1; W=${2:-8}
PY=.venv/bin/python
R="$PY -m run.runner --model $KEY --workers $W"
$R --tag pilot_api --pilot
$PY -m run.d11 pilot_api "$KEY"
FALLBACK=$(grep -c "fallback=True" "data/FALLBACK_DECISION_$KEY.txt" || true)
$R --tag main --sub-exp S1
[ "$FALLBACK" -ge 1 ] && $R --tag main --extension-only
$R --tag main --sub-exp S2
$R --tag main --sub-exp S3a S3b
$R --bank checks --tag checks
[ "$FALLBACK" -ge 1 ] && $R --bank checks --tag checks --extension-only
echo "ALL COLLECTION COMPLETE FOR $KEY"
