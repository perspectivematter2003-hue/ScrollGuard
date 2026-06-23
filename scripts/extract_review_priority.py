#!/usr/bin/env python3
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scrollguard.crop_manifest import get_manifest_item
from scrollguard.review_priority import extract_review_tiles, write_csv, write_jsonl


item = get_manifest_item("gate_a_tiny_crop")

risk_map = np.load(item.quality_cache_dir / "risk_map.npy")
quality_map = np.load(item.quality_cache_dir / "quality_map.npy")
metadata_path = Path("outputs") / f"{item.name}_metadata.json"
metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

records = extract_review_tiles(
    risk_map=risk_map,
    quality_map=quality_map,
    metadata=metadata,
    tile_size=16,
)

out_dir = item.review_output_dir
write_csv(records, out_dir / "review_priority.csv")
write_jsonl(records, out_dir / "review_priority.jsonl")

print(f"OK extracted {len(records)} review-priority tile(s)")
print(f"crop_name={item.name}")
print("Top 3:")
for record in records[:3]:
    print(record)
print("No Vesuvius server access used.")
