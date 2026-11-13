#!/usr/bin/env bash
# Rater-flag sensitivity analyses (main without A3/A4; follow-up without flagged anger messages). CPU only.
#   sbatch ada/run_sensitivity.sbatch
#SBATCH --job-name=neuroeco-sens
#SBATCH --partition=u22
#SBATCH --account=research
#SBATCH --qos=medium
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --output=slurm-%x-%j.out
set -uo pipefail
cd "$SLURM_SUBMIT_DIR"
export MPLBACKEND=Agg OMP_NUM_THREADS=4
bash ada/run_sensitivity.sh
echo SENS_COMPLETE
