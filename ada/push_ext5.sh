#!/usr/bin/env bash
# LAPTOP (Git Bash): pack the code + frozen extension-5 bank and copy it to your Ada home (md5-checked).
#   ADA_USER=your.username bash ada/push_ext5.sh
# Never sends data/raw, results, .env or .venv.
set -euo pipefail
: "${ADA_USER:?set ADA_USER, e.g. ADA_USER=firstname.lastname bash ada/push_ext5.sh}"
GW="$ADA_USER@ada-gw1.iiit.ac.in"
cd "$(dirname "$0")/.."
TAR=/tmp/neuroeco_ext5.tar.gz
tar -czf "$TAR" --exclude=__pycache__ --exclude='*.pyc' \
    config.py requirements.txt build_scenarios.py build_ext4.py build_ext5.py run analysis ada stimuli \
    data/scenarios/ext5_trials.jsonl data/scenarios/probe_ext5_mood.jsonl \
    docs/preregistration_extension5.md
ls -lh "$TAR"
SUM=$(md5sum "$TAR" | cut -d' ' -f1)
ssh "$GW" "mkdir -p ~/projects/neuroeco"
scp "$TAR" "$GW:projects/neuroeco/"
ssh "$GW" "cd ~/projects/neuroeco && [ \"\$(md5sum neuroeco_ext5.tar.gz | cut -d' ' -f1)\" = \"$SUM\" ] && tar -xzf neuroeco_ext5.tar.gz && rm neuroeco_ext5.tar.gz && find ada -name '*.sh' -o -name '*.sbatch' | xargs sed -i 's/\r\$//' && echo MD5_OK_UNPACKED"
# (sed: Windows checkouts with core.autocrlf=true have CRLF line endings, which break bash on Linux)
echo "PUSHED. Next, on Ada:  cd ~/projects/neuroeco && nohup bash ada/rounds_ext5.sh > rounds_ext5.log 2>&1 &"
