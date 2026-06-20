from pathlib import Path
import json

import numpy as np

from scrollguard.review_priority import extract_review_tiles, write_csv, write_jsonl

risk_map = np.load("data_cache/quality/gate_a_tiny_crop/risk_map.npy")
quality_map = np.load("data_cache/quality/gate_a_tiny_crop/quality_map.npy")
metadata = json.loads(Path("outputs/cached_tiny_crop_metadata.json").read_text())

records = extract_review_tiles(
    risk_map=risk_map,
    quality_map=quality_map,
    metadata=metadata,
    tile_size=16,
)

out_dir = Path("outputs/review/gate_a_tiny_crop")
write_csv(records, out_dir / "review_priority.csv")
write_jsonl(records, out_dir / "review_priority.jsonl")

print(f"OK extracted {len(records)} review-priority tile(s)")
print("Top 3:")
for record in records[:3]:
    print(record)
