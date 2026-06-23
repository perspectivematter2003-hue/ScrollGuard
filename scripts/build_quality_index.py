#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scrollguard.crop_manifest import get_manifest_item
from scrollguard.quality_index import build_quality_record, write_csv, write_jsonl


item = get_manifest_item("gate_a_tiny_crop")

record = build_quality_record(
    quality_set=f"{item.name}_quality_v0",
    quality_cache_dir=str(item.quality_cache_dir),
    quality_output_dir=str(item.quality_output_dir),
)

records = [record]

write_jsonl(records, "outputs/quality/quality_index.jsonl")
write_csv(records, "outputs/quality/quality_index.csv")

print("OK built quality index")
print("outputs/quality/quality_index.jsonl")
print("outputs/quality/quality_index.csv")
print(record)
