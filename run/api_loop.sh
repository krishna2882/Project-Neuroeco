#!/usr/bin/env bash
# LAPTOP: run a rate-limited free-tier API model on a bank until nothing is left to run, retrying every 30 minutes
# (daily quota or no internet stops a pass without using up attempts; see P24).
#   bash run/api_loop.sh <model_key> <trial bank> <trial tag> <probe bank> <probe tag>
#   bash run/api_loop.sh gptoss_120b ext5core_trials ext5 probe_ext5core_mood probe_ext5_mood
set -uo pipefail
cd "$(dirname "$0")/.."
export PYTHONIOENCODING=utf-8
M=$1; BANK=$2; TAG=$3; PBANK=$4; PTAG=$5
LOG=logs_ada/api_${M}_${TAG}.log
mkdir -p logs_ada
left() {  # trials of a bank that still have attempts left (offline failures do not count as attempts)
  python -c "
import sys, pandas as pd
from run.runner import SCEN, load_done
from config import RAW_DIR
ids = set(pd.read_json(SCEN / (sys.argv[2] + '.jsonl'), lines=True, dtype=False).trial_id)
done, _ = load_done(RAW_DIR / sys.argv[1] / (sys.argv[3] + '.jsonl'))
print(len(ids - done))" "$M" "$1" "$2"
}
for i in $(seq 200); do
  python -m run.runner --model "$M" --bank "$BANK" --tag "$TAG" >> "$LOG" 2>&1
  python -m run.runner --model "$M" --bank "$PBANK" --tag "$PTAG" >> "$LOG" 2>&1
  A=$(left "$BANK" "$TAG"); B=$(left "$PBANK" "$PTAG")
  echo "$(date '+%d %H:%M') $M $TAG: $A to run; probes: $B to run" >> "logs_ada/api_${M}_${TAG}_resume.log"
  if [ "$A" = "0" ] && [ "$B" = "0" ]; then echo "${M}_${TAG}_ALL_DONE"; break; fi
  sleep 1800
done
tail -2 "logs_ada/api_${M}_${TAG}_resume.log"
