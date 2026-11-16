#!/usr/bin/env bash
# ADA GATEWAY (ada-gw1, has internet; compute nodes do not). One-time setup for a fresh account, idempotent:
#   cd ~/projects/neuroeco && bash ada/setup_ext4_gw.sh
# 1. Python wheels (downloaded here) -> .venv built offline on a compute node
# 2. Ollama v0.40.11 in ~/ollama (user space, no root)
# 3. the three extension-4 models in ~/ollama_models (~4.7 + 4.9 + 9.0 GB)
# Override the Slurm account / QoS if yours differ:  ACCOUNT=xyz QOS=abc bash ada/setup_ext4_gw.sh
set -euo pipefail
cd ~/projects/neuroeco
ACCOUNT=${ACCOUNT:-research}; QOS=${QOS:-medium}
# Small home quota? Pull in rounds, e.g. MODELS="qwen2.5:7b-instruct-q4_K_M llama3.1:8b-instruct-q4_K_M", run, delete, then
# MODELS="qwen2.5:14b-instruct-q4_K_M" (compute nodes only see your home, not /share1).
MODELS_TO_PULL=${MODELS:-"qwen2.5:7b-instruct-q4_K_M llama3.1:8b-instruct-q4_K_M qwen2.5:14b-instruct-q4_K_M"}

echo "== 0. disk: models need ~19 GB in your home"
df -h ~ | tail -1

echo "== 1. Python environment"
if [ ! -x .venv/bin/python ]; then
  ([ -x ~/.gwpip/bin/pip ] || python3 -m venv ~/.gwpip)
  ~/.gwpip/bin/pip download -q --dest wheels --only-binary=:all: --python-version 3.10 --implementation cp \
    --abi cp310 --platform manylinux2014_x86_64 --platform manylinux_2_17_x86_64 --platform manylinux_2_28_x86_64 \
    --platform linux_x86_64 -r requirements.txt
  srun -p u22 -A "$ACCOUNT" --qos="$QOS" -c 2 --mem=4G -t 00:20:00 bash -c \
    'cd ~/projects/neuroeco && python3 -m venv .venv && .venv/bin/pip install -q --no-index --find-links wheels -r requirements.txt'
fi
# the venv is built for the compute nodes' Python 3.10 (the gateway has 3.9), so it is checked there
srun -p u22 -A "$ACCOUNT" --qos="$QOS" -c 1 --mem=2G -t 00:05:00 bash -c   'cd ~/projects/neuroeco && .venv/bin/python -c "import pandas, statsmodels; print(\"venv OK, pandas\", pandas.__version__)"' 

echo "== 2. Ollama"
VER=v0.40.11
mkdir -p ~/ollama ~/ollama_models
if [ ! -x ~/ollama/bin/ollama ]; then
  cd ~/ollama
  curl -fL --retry 5 -o ollama.tar.zst https://github.com/ollama/ollama/releases/download/$VER/ollama-linux-amd64.tar.zst
  ~/.gwpip/bin/pip install -q zstandard
  ~/.gwpip/bin/python -c "import zstandard,tarfile;f=open('ollama.tar.zst','rb');r=zstandard.ZstdDecompressor().stream_reader(f);tarfile.open(fileobj=r,mode='r|').extractall('.')"
  rm ollama.tar.zst
  cd ~/projects/neuroeco
fi
~/ollama/bin/ollama --version || true

echo "== 3. Models"
export OLLAMA_MODELS=~/ollama_models OLLAMA_HOST=127.0.0.1:11557
~/ollama/bin/ollama serve > ~/ollama_gw_pull.log 2>&1 &
SP=$!; trap 'kill $SP 2>/dev/null || true' EXIT
for i in $(seq 30); do curl -sf localhost:11557/api/version >/dev/null && break; sleep 2; done
for TAG in $MODELS_TO_PULL; do ~/ollama/bin/ollama pull "$TAG"; done
~/ollama/bin/ollama list

echo "== 4. Bank check"
python3 - <<'PY'
import json
t = [json.loads(l) for l in open("data/scenarios/ext4_trials.jsonl")]
p = [json.loads(l) for l in open("data/scenarios/probe_ext4_mood.jsonl")]
assert len(t) == 5328 and len(p) == 128, (len(t), len(p))
mods = {}
for r in t:
    mods[r["module"]] = mods.get(r["module"], 0) + 1
print("ext4 bank OK:", dict(sorted(mods.items())), "| mood probes:", len(p))
PY
echo "SETUP DONE. After the pre-registration is frozen and pushed, submit:"
echo "  sbatch -A $ACCOUNT --qos=$QOS --export=ALL,MODEL_KEYS=\"qwen25_7b llama31_8b qwen25_14b\" ada/run_ext4.sbatch"
