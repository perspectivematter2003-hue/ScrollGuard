#!/usr/bin/env bash
set -e

python scripts/start_day_check.py
python scripts/cache_inventory.py
python scripts/manifest_cache_check.py
python scripts/month2_smoke_test.py
python scripts/month3_smoke_test.py
python scripts/month4_smoke_test.py
python scripts/review_evidence_smoke_test.py
python scripts/review_tags_smoke_test.py
python scripts/dashboard_smoke_test.py
python scripts/demo_package_smoke_test.py
python scripts/build_demo_zip.py
python scripts/demo_zip_smoke_test.py

echo "OK full ScrollGuard local audit passed"
echo "No Vesuvius server access used."
