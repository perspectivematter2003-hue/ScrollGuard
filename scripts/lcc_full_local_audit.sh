#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH=src
export VC_SEGCHECK_FIXED_CREATED_AT_UTC="2000-01-01T00:00:00+00:00"

echo "== LCC full local audit =="
echo "repo: $(pwd)"
echo "python: $(python --version)"
echo

echo "[1/11] normal profile smoke"
python scripts/lcc_normal_profile_smoke_test.py

echo
echo "[2/11] surface reader smoke"
python scripts/lcc_surface_smoke_test.py

echo
echo "[3/11] lamina spacing smoke"
python scripts/lcc_spacing_smoke_test.py

echo
echo "[4/11] lamina index smoke"
python scripts/lcc_lamina_smoke_test.py

echo
echo "[5/11] discontinuity detector smoke"
python scripts/lcc_discontinuity_smoke_test.py

echo
echo "[6/11] confidence gate smoke"
python scripts/lcc_gate_smoke_test.py

echo
echo "[7/11] region grouper smoke"
python scripts/lcc_grouper_smoke_test.py

echo
echo "[8/11] reporting / evidence smoke"
python scripts/lcc_reporting_smoke_test.py

echo
echo "[9/11] end-to-end pipeline smoke"
python scripts/lcc_pipeline_smoke_test.py

echo
echo "[10/11] CLI smoke"
python scripts/lcc_cli_smoke_test.py

echo
echo "[11/11] CLI validation smoke"
python scripts/lcc_cli_validation_smoke_test.py

echo
echo "OK LCC full local audit passed"
