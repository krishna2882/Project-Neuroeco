#!/usr/bin/env bash
# LAPTOP (Git Bash): pack the code + frozen extension-4 bank and copy it to your Ada home. No rsync needed.
#   ADA_USER=your.username bash ada/push_ext4.sh
# Never sends data/raw, results, .env or .venv.
set -euo pipefail
: "${ADA_USER:?set ADA_USER, e.g. ADA_USER=firstname.lastname bash ada/push_ext4.sh}"
GW="$ADA_USER@ada-gw1.iiit.ac.in"
cd "$(dirname "$0")/.."
TAR=/tmp/neuroeco_ext4.tar.gz
tar -czf "$TAR" --exclude=__pycache__ --exclude='*.pyc' \
    config.py requirements.txt build_scenarios.py build_ext4.py run analysis ada stimuli \
    data/scenarios/trials.jsonl data/scenarios/followup_trials.jsonl \
    data/scenarios/ext4_trials.jsonl data/scenarios/probe_ext4_mood.jsonl \
    docs/preregistration_extension4.md
ls -lh "$TAR"
ssh "$GW" "mkdir -p ~/projects/neuroeco"
scp "$TAR" "$GW:projects/neuroeco/"
ssh "$GW" "cd ~/projects/neuroeco && tar -xzf neuroeco_ext4.tar.gz && rm neuroeco_ext4.tar.gz && find ada -name '*.sh' -o -name '*.sbatch' | xargs sed -i 's/\r$//' && ls"
# (sed: Windows checkouts with core.autocrlf=true have CRLF line endings, which break bash on Linux)
echo "PUSHED. Next, on Ada:  ssh $GW   then   cd ~/projects/neuroeco && bash ada/setup_ext4_gw.sh"
