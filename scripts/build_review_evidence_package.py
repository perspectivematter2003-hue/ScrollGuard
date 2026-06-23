#!/usr/bin/env python3
import csv
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scrollguard.crop_manifest import get_manifest_item


item = get_manifest_item("gate_a_tiny_crop")

review_csv = item.review_output_dir / "review_priority.csv"
metadata_path = Path("outputs") / f"{item.name}_metadata.json"
feature_dir = item.feature_cache_dir
quality_dir = item.quality_cache_dir
out_path = item.review_output_dir / "evidence_package_top5.json"

metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

arrays = {
    "gradient_magnitude": np.load(feature_dir / "gradient_magnitude.npy"),
    "local_std": np.load(feature_dir / "local_std.npy"),
    "texture_coherence": np.load(feature_dir / "texture_coherence.npy"),
    "quality_map": np.load(quality_dir / "quality_map.npy"),
    "risk_map": np.load(quality_dir / "risk_map.npy"),
}

with review_csv.open("r", encoding="utf-8") as f:
    records = list(csv.DictReader(f))

evidence_items = []

for record in records[:5]:
    y0 = int(record["tile_y0"])
    y1 = int(record["tile_y1"])
    x0 = int(record["tile_x0"])
    x1 = int(record["tile_x1"])

    feature_stats = {}
    for name, arr in arrays.items():
        tile = arr[y0:y1, x0:x1]
        feature_stats[name] = {
            "mean": float(np.mean(tile)),
            "min": float(np.min(tile)),
            "max": float(np.max(tile)),
        }

    evidence_items.append({
        "review_id": record["review_id"],
        "rank": int(record["rank"]),
        "scan_id": record["scan_id"],
        "z": int(record["z"]),
        "tile_coordinate": {
            "tile_y0": y0,
            "tile_y1": y1,
            "tile_x0": x0,
            "tile_x1": x1,
        },
        "voxel_coordinate": {
            "voxel_y0": int(record["voxel_y0"]),
            "voxel_y1": int(record["voxel_y1"]),
            "voxel_x0": int(record["voxel_x0"]),
            "voxel_x1": int(record["voxel_x1"]),
        },
        "ranking_values": {
            "risk_mean": float(record["risk_mean"]),
            "risk_max": float(record["risk_max"]),
            "quality_mean": float(record["quality_mean"]),
            "quality_min": float(record["quality_min"]),
        },
        "feature_stats": feature_stats,
        "source_files": {
            "crop_metadata": str(metadata_path),
            "review_priority_csv": str(review_csv),
            "feature_dir": str(feature_dir),
            "quality_dir": str(quality_dir),
            "overlay": str(item.review_output_dir / "review_priority_overlay.png"),
        },
        "method": "scrollguard.review_evidence_package.top_risk_tiles.v0",
    })

package = {
    "package_name": f"{item.name}_top5_review_evidence",
    "doctrine": "AI proposes, verifier decides. Never hallucinate letters. Every output must have evidence trail back to CT data.",
    "crop_metadata": metadata,
    "evidence_count": len(evidence_items),
    "evidence_items": evidence_items,
}

out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(package, indent=2), encoding="utf-8")

print("OK built review evidence package")
print(f"crop_name={item.name}")
print(f"output={out_path}")
print(f"items={len(evidence_items)}")
print("top_review_id=", evidence_items[0]["review_id"])
print("No Vesuvius server access used.")
