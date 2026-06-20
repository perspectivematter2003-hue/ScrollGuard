#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."
source ~/miniconda3/etc/profile.d/conda.sh
conda activate scrollguard

streamlit run apps/scrollguard_dashboard.py --server.address 0.0.0.0 --server.port 8501
