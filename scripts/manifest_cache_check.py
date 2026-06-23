#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scrollguard.crop_manifest import load_crop_manifest


def main() -> None:
    manifest_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("configs/crops_manifest.json")
    items = load_crop_manifest(manifest_path)
    missing = []

    print("ScrollGuard manifest cache check")
    print(f"manifest={manifest_path}")
    print(f"manifest_crop_count={len(items)}")

    for item in items:
        cache_path = item.crop_cache_path

        if cache_path.exists():
            print(f"OK cached {item.name}: {cache_path}")
        else:
            print(f"MISSING cached {item.name}: {cache_path}")
            missing.append(str(cache_path))

    if missing:
        raise SystemExit("ERROR manifest contains crop(s) missing from local cache. Cache-only mode refuses server access.")

    print("OK manifest cache check passed")
    print("No Vesuvius server access used.")


if __name__ == "__main__":
    main()
