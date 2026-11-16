#!/usr/bin/env bash
# ADA COMPUTE NODE (sourced by the mech jobs): build, if missing, a PyTorch environment and a Hugging Face cache on the
# node-local /scratch (the home quota is too small; compute nodes have internet). Idempotent; /scratch is per node.
set -euo pipefail
export MECH_ROOT=/scratch/$USER/neuroeco_mech
export HF_HOME=$MECH_ROOT/hf PIP_CACHE_DIR=$MECH_ROOT/pip TMPDIR=$MECH_ROOT/tmp
mkdir -p "$MECH_ROOT" "$HF_HOME" "$TMPDIR"
if [ ! -f "$MECH_ROOT/venv/ok" ]; then
  python3 -m venv "$MECH_ROOT/venv"
  "$MECH_ROOT/venv/bin/pip" install -q --upgrade pip
  # cu121 wheels still support the GTX 1080 Ti (Pascal)
  "$MECH_ROOT/venv/bin/pip" install -q torch==2.5.1 --index-url https://download.pytorch.org/whl/cu121
  "$MECH_ROOT/venv/bin/pip" install -q "transformers==4.46.3" "accelerate==1.1.1" "scikit-learn==1.5.2" "pandas==2.2.3" \
      "numpy==1.26.4" "scipy==1.14.1" "statsmodels==0.14.4" "safetensors"
  touch "$MECH_ROOT/venv/ok"
fi
export MECH_PY=$MECH_ROOT/venv/bin/python
"$MECH_PY" -c "
import torch, transformers
print('torch', torch.__version__, 'cuda', torch.cuda.is_available(), torch.cuda.device_count(), 'transformers', transformers.__version__)
assert torch.cuda.is_available(), 'no usable GPU on this node: resubmit with --exclude=' + __import__('socket').gethostname()
"
