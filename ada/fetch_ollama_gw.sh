#!/usr/bin/env bash
# Gateway-only (has internet): fetch Ollama + pull the model into ~/ollama_models. Idempotent.
set -euo pipefail
VER=v0.40.11
mkdir -p ~/ollama ~/ollama_models
if [ ! -x ~/ollama/bin/ollama ]; then
  cd ~/ollama
  curl -fL --retry 5 -o ollama.tar.zst https://github.com/ollama/ollama/releases/download/$VER/ollama-linux-amd64.tar.zst
  ~/.gwpip/bin/pip install -q zstandard
  ~/.gwpip/bin/python -c "import zstandard,tarfile;f=open(\"ollama.tar.zst\",\"rb\");r=zstandard.ZstdDecompressor().stream_reader(f);tarfile.open(fileobj=r,mode=\"r|\").extractall(\".\")"
  rm ollama.tar.zst
fi
~/ollama/bin/ollama --version || true
export OLLAMA_MODELS=~/ollama_models OLLAMA_HOST=127.0.0.1:11555
~/ollama/bin/ollama serve > ~/ollama_gw_serve.log 2>&1 &
SP=$!; sleep 8
~/ollama/bin/ollama pull llama3.1:8b-instruct-q4_K_M
~/ollama/bin/ollama list
kill $SP
echo FETCH_DONE
