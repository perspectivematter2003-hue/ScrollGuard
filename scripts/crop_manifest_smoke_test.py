#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scrollguard.crop_manifest import get_manifest_item, load_crop_manifest


def main() -> None:
    items = load_crop_manifest()

    if len(items) != 1:
        raise SystemExit(f"ERROR expected 1 manifest item, found {len(items)}")

    item = get_manifest_item("gate_a_tiny_crop")

    if item.name != "gate_a_tiny_crop":
        raise SystemExit(f"ERROR unexpected item name: {item.name}")

    if item.request.scan_id != "Scroll1":
        raise SystemExit(f"ERROR unexpected scan_id: {item.request.scan_id}")

    if item.crop_cache_path != Path("data_cache/crops/Scroll1_z1000_y3520_3584_x4256_4320.npy"):
        raise SystemExit(f"ERROR unexpected crop cache path: {item.crop_cache_path}")

    if item.feature_cache_dir != Path("data_cache/features/gate_a_tiny_crop"):
        raise SystemExit(f"ERROR unexpected feature cache dir: {item.feature_cache_dir}")

    if item.quality_cache_dir != Path("data_cache/quality/gate_a_tiny_crop"):
        raise SystemExit(f"ERROR unexpected quality cache dir: {item.quality_cache_dir}")

    if item.review_output_dir != Path("outputs/review/gate_a_tiny_crop"):
        raise SystemExit(f"ERROR unexpected review output dir: {item.review_output_dir}")

    print("OK crop manifest smoke test passed")
    print("manifest_item_count=1")
    print(f"crop_name={item.name}")
    print(f"crop_cache_path={item.crop_cache_path}")
    print("No Vesuvius server access used.")


if __name__ == "__main__":
    main()
