from pathlib import Path
import json
import csv

package_path = Path("outputs/review/gate_a_tiny_crop/evidence_package_top5.json")
csv_path = Path("outputs/review/gate_a_tiny_crop/review_priority.csv")
overlay_path = Path("outputs/review/gate_a_tiny_crop/review_priority_overlay.png")

required = [package_path, csv_path, overlay_path]
missing = [str(p) for p in required if not p.exists()]
if missing:
    raise FileNotFoundError("Missing review/evidence files:\n" + "\n".join(missing))

package = json.loads(package_path.read_text(encoding="utf-8"))

assert package["evidence_count"] == 5, "Expected top-5 evidence items"
assert len(package["evidence_items"]) == 5, "Evidence item count mismatch"

with csv_path.open("r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

assert len(rows) == 16, "Expected 16 review-priority tiles"

for item in package["evidence_items"]:
    assert "review_id" in item
    assert "voxel_coordinate" in item
    assert "feature_stats" in item
    assert "quality_map" in item["feature_stats"]
    assert "risk_map" in item["feature_stats"]
    assert item["scan_id"] == "Scroll1"
    assert item["z"] == 1000

print("OK review evidence smoke test passed")
print(f"evidence_count={package['evidence_count']}")
print(f"review_tiles={len(rows)}")
print("No Vesuvius server access used in this test.")
