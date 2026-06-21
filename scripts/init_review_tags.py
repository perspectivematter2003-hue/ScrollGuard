from pathlib import Path
import csv

review_csv = Path("outputs/review/gate_a_tiny_crop/review_priority.csv")
out_csv = Path("outputs/review/gate_a_tiny_crop/review_tags.csv")

with review_csv.open("r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

fields = [
    "review_id",
    "rank",
    "scan_id",
    "z",
    "voxel_y0",
    "voxel_y1",
    "voxel_x0",
    "voxel_x1",
    "risk_mean",
    "quality_mean",
    "human_label",
    "human_notes",
]

out_csv.parent.mkdir(parents=True, exist_ok=True)

with out_csv.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for row in rows:
        writer.writerow({
            "review_id": row["review_id"],
            "rank": row["rank"],
            "scan_id": row["scan_id"],
            "z": row["z"],
            "voxel_y0": row["voxel_y0"],
            "voxel_y1": row["voxel_y1"],
            "voxel_x0": row["voxel_x0"],
            "voxel_x1": row["voxel_x1"],
            "risk_mean": row["risk_mean"],
            "quality_mean": row["quality_mean"],
            "human_label": "unreviewed",
            "human_notes": "",
        })

print(f"OK initialized review tags: {out_csv}")
print(f"rows={len(rows)}")
