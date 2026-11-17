#!/usr/bin/env bash
# ADA LOGIN NODE: submit every extension-6 and extension-7 job. Run only after both pre-registrations are frozen and
# pushed (commit 4f13710). Jobs are resumable, so running this twice only re-submits (completed trials are skipped).
#   cd ~/projects/neuroeco && bash ada/submit_ext67.sh
set -euo pipefail
cd "$(dirname "$0")/.."
X="--exclude=gnode042"   # gnode042: broken CUDA setup

# Extension 7, new models: frozen extension-4 and extension-5 banks (family G) + mood controls (family N)
for M in gemma3_12b gemma3_4b mistral_nemo_12b phi4_14b granite33_8b llama32_3b; do
  echo "ext7 $M $(sbatch --parsable $X --job-name=e7-$M --export=ALL,MODEL_KEY=$M,PARTS="ext4 ext5 ext7" ada/run_ext7.sbatch)"
done
# Extension 7, original Ada models: mood controls only (family N)
for M in qwen25_7b llama31_8b qwen25_14b; do
  echo "ext7 $M $(sbatch --parsable $X --job-name=e7-$M --export=ALL,MODEL_KEY=$M,PARTS="ext7" ada/run_ext7.sbatch)"
done
# Extension 6: probing and steering (Hugging Face fp16; the 7B model needs two 11 GB GPUs)
echo "ext6 3b $(sbatch --parsable $X --job-name=e6-3b --export=ALL,HF_MODEL=Qwen/Qwen2.5-3B-Instruct,KEY=qwen25_3b_hf ada/run_ext6.sbatch)"
echo "ext6 7b $(sbatch --parsable $X --job-name=e6-7b --gres=gpu:2 --export=ALL,HF_MODEL=Qwen/Qwen2.5-7B-Instruct,KEY=qwen25_7b_hf ada/run_ext6.sbatch)"
squeue -u "$USER"
