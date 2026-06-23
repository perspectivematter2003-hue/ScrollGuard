#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scrollguard.data_access import CropRequest
from scrollguard.cache import crop_cache_name


def main() -> None:
    manifest_path = Path("configs/crops_manifest.json")
    items = json.loads(manifest_path.read_text(encoding="utf-8"))

    crop_dir = Path("data_cache/crops")
    missing = []

    print("ScrollGuard manifest cache check")
    print(f"manifest={manifest_path}")
    print(f"manifest_crop_count={len(items)}")

    for item in items:
        request = CropRequest(
            scan_id=item["scan_id"],
            z=item["z"],
            y0=item["y0"],
            y1=item["y1"],
            x0=item["x0"],
            x1=item["x1"],
        )
        cache_path = crop_dir / crop_cache_name(request)
        name = item.get("name", cache_path.stem)

        if cache_path.exists():
            print(f"OK cached {name}: {cache_path}")
        else:
            print(f"MISSING cached {name}: {cache_path}")
            missing.append(str(cache_path))

    if missing:
        raise SystemExit("ERROR manifest contains crop(s) missing from local cache. Cache-only mode refuses server access.")

    print("OK manifest cache check passed")
    print("No Vesuvius server access used.")


if __name__ == "__main__":
    main()
