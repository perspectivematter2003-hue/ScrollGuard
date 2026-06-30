#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scrollguard.crop_manifest import get_manifest_item
from scrollguard.feature_index import build_feature_record, write_csv, write_jsonl


item = get_manifest_item("gate_a_tiny_crop")

record = build_feature_record(
    feature_set=f"{item.name}_basic_features",
    source_crop_cache=str(item.crop_cache_path),
    source_metadata=f"outputs/{item.name}_metadata.json",
    feature_dir=str(item.feature_cache_dir),
    preview_dir=str(item.feature_output_dir),
)

records = [record]

write_jsonl(records, "outputs/features/feature_index.jsonl")
write_csv(records, "outputs/features/feature_index.csv")

print("OK built feature index")
print("outputs/features/feature_index.jsonl")
print("outputs/features/feature_index.csv")
print(record)
print("No Vesuvius server access used.")
