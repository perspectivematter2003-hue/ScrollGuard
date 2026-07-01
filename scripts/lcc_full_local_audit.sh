#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH=src

echo "== LCC full local audit =="
echo "repo: $(pwd)"
echo "python: $(python --version)"
echo

echo "[1/10] normal profile smoke"
python scripts/lcc_normal_profile_smoke_test.py

echo
echo "[2/10] surface reader smoke"
python scripts/lcc_surface_smoke_test.py

echo
echo "[3/10] lamina spacing smoke"
python scripts/lcc_spacing_smoke_test.py

echo
echo "[4/10] lamina index smoke"
python scripts/lcc_lamina_smoke_test.py

echo
echo "[5/10] discontinuity detector smoke"
python scripts/lcc_discontinuity_smoke_test.py

echo
echo "[6/10] confidence gate smoke"
python scripts/lcc_gate_smoke_test.py

echo
echo "[7/10] region grouper smoke"
python scripts/lcc_grouper_smoke_test.py

echo
echo "[8/10] reporting / evidence smoke"
python scripts/lcc_reporting_smoke_test.py

echo
echo "[9/10] end-to-end pipeline smoke"
python scripts/lcc_pipeline_smoke_test.py

echo
echo "[10/10] CLI smoke"
python scripts/lcc_cli_smoke_test.py

echo
echo "OK LCC full local audit passed"
