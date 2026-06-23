#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scrollguard.cache import load_crop_cache_only
from scrollguard.crop_manifest import load_crop_manifest
from scrollguard.data_access import build_metadata, save_metadata
from scrollguard.metadata_index import load_metadata_files, write_csv, write_jsonl


manifest_path = Path("configs/crops_manifest.json")
items = load_crop_manifest(manifest_path)

for item in items:
    crop = load_crop_cache_only(item.request)
    metadata = build_metadata(item.request, crop)
    out_path = Path("outputs") / f"{item.name}_metadata.json"
    save_metadata(metadata, out_path)
    print(f"OK wrote {out_path}")

metadata_files = sorted(Path("outputs").glob("*metadata.json"))
records = load_metadata_files(metadata_files)
write_jsonl(records, "outputs/metadata_index.jsonl")
write_csv(records, "outputs/metadata_index.csv")

print(f"OK rebuilt metadata index with {len(records)} record(s)")
