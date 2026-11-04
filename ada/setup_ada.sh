#!/usr/bin/env bash
# One-time Ada setup, run FROM THE LAPTOP (passwordless SSH to the gateway).
# Gateway has internet; compute nodes (partition u22) do not, so everything is fetched on the gateway.
#   bash ada/setup_ada.sh
set -euo pipefail
GW=krishna.goel@ada-gw1.iiit.ac.in
DIR=projects/neuroeco
cd "$(dirname "$0")/.."

# 1. code + frozen scenario bank (never raw data, results or .env)
ssh $GW "mkdir -p ~/$DIR"
rsync -az --exclude .venv --exclude data/sim --exclude data/raw --exclude results --exclude __pycache__ \
      --exclude .env --exclude 'logs_*' --exclude '*.pdf' --exclude wheels ./ $GW:$DIR/

# 2. wheels on the gateway, venv built offline on a compute node
ssh $GW "cd ~/$DIR && ([ -x ~/.gwpip/bin/pip ] || python3 -m venv ~/.gwpip) && \
  ~/.gwpip/bin/pip download -q --dest wheels --only-binary=:all: --python-version 3.10 --implementation cp \
  --abi cp310 --platform manylinux2014_x86_64 --platform manylinux_2_17_x86_64 --platform manylinux_2_28_x86_64 \
  --platform linux_x86_64 -r requirements.txt"
ssh $GW "srun -p u22 -A research --qos=medium -c 2 --mem=4G -t 00:20:00 bash -c \
  'cd ~/$DIR && python3 -m venv .venv && .venv/bin/pip install -q --no-index --find-links wheels -r requirements.txt'"

# 3. Ollama (user space) + model, fetched on the gateway (~1.5 GB + ~4.9 GB, into ~/ollama, ~/ollama_models)
ssh $GW "cd ~/$DIR && bash ada/fetch_ollama_gw.sh"
echo "Setup done. Submit:  ssh $GW 'cd ~/$DIR && sbatch ada/run_local.sbatch'"
