import json
from pathlib import Path

from scrollguard.data_access import CropRequest, build_metadata, save_metadata
from scrollguard.cache import load_or_create_crop_cache
from scrollguard.metadata_index import load_metadata_files, write_csv, write_jsonl

manifest_path = Path("configs/crops_manifest.json")
items = json.loads(manifest_path.read_text(encoding="utf-8"))

for item in items:
    name = item["name"]
    request = CropRequest(
        scan_id=item["scan_id"],
        z=item["z"],
        y0=item["y0"],
        y1=item["y1"],
        x0=item["x0"],
        x1=item["x1"],
    )

    crop = load_or_create_crop_cache(request)
    metadata = build_metadata(request, crop)
    out_path = Path("outputs") / f"{name}_metadata.json"
    save_metadata(metadata, out_path)
    print(f"OK wrote {out_path}")

metadata_files = sorted(Path("outputs").glob("*metadata.json"))
records = load_metadata_files(metadata_files)
write_jsonl(records, "outputs/metadata_index.jsonl")
write_csv(records, "outputs/metadata_index.csv")

print(f"OK rebuilt metadata index with {len(records)} record(s)")
