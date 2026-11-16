#!/usr/bin/env bash
# Extension 6: probing and steering (docs/preregistration_extension6.md). Everything heavy lives on the node's /scratch.
#   sbatch --export=ALL,HF_MODEL=Qwen/Qwen2.5-3B-Instruct,KEY=qwen25_3b_hf ada/run_ext6.sbatch
#   sbatch --gres=gpu:2 --export=ALL,HF_MODEL=Qwen/Qwen2.5-7B-Instruct,KEY=qwen25_7b_hf ada/run_ext6.sbatch
# Development (not analysed): add EXTRA="--limit 6 --n-random 3 --sweep-random 1" and a dev model.
#
#SBATCH --job-name=neuroeco-ext6
#SBATCH --partition=u22
#SBATCH --account=research
#SBATCH --qos=medium
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=6
#SBATCH --mem=32G
#SBATCH --time=0-10:00:00
#SBATCH --output=slurm-%x-%j.out

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
: "${HF_MODEL:?set HF_MODEL}" "${KEY:?set KEY}"
source ada/mech_env.sh
hostname; nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
"$MECH_PY" -m mech.run_mech --model "$HF_MODEL" --key "$KEY" ${EXTRA:-}
echo "EXT6 COMPLETE $KEY"
