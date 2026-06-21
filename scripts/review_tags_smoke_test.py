from pathlib import Path
import csv

tags_path = Path("outputs/review/gate_a_tiny_crop/review_tags.csv")
priority_path = Path("outputs/review/gate_a_tiny_crop/review_priority.csv")

required = [tags_path, priority_path]
missing = [str(p) for p in required if not p.exists()]
if missing:
    raise FileNotFoundError("Missing review tag files:\n" + "\n".join(missing))

with tags_path.open("r", encoding="utf-8") as f:
    tag_rows = list(csv.DictReader(f))

with priority_path.open("r", encoding="utf-8") as f:
    priority_rows = list(csv.DictReader(f))

assert len(tag_rows) == len(priority_rows), "Review tag row count must match priority row count"

allowed_labels = {"unreviewed", "accept", "reject", "unsure"}

for row in tag_rows:
    assert row["human_label"] in allowed_labels, f"Invalid human_label: {row['human_label']}"
    assert row["review_id"], "Missing review_id"
    assert row["scan_id"] == "Scroll1", "Unexpected scan_id"

print("OK review tags smoke test passed")
print(f"review_tag_rows={len(tag_rows)}")
print("No Vesuvius server access used in this test.")
