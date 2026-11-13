# Rater-flag sensitivity analyses (pre-specified in docs/preregistration_followup.md, section 2).
# PART=main|followup|both (default both)
set -x
PY=.venv/bin/python
PART=${PART:-both}
if [ "$PART" != followup ]; then
$PY -m analysis.run_all --tag main --checks-tag checks --out main_excl --models llama31_8b qwen25_7b mistral --exclude-msgs A3 A4 && $PY -m analysis.forest --out main_excl && $PY -m analysis.message_re --out main_excl; echo MAIN_DONE $?
fi
if [ "$PART" != main ]; then
$PY -m analysis.run_all --bank-prefix followup --tag followup --checks-tag followup_checks --out followup_excl --models llama31_8b qwen25_7b --exclude-msgs FA2 FA3 FA4 FA6 FA7 && $PY -m analysis.forest --out followup_excl && $PY -m analysis.message_re --out followup_excl; echo FU_DONE $?
fi
