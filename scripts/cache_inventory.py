#!/usr/bin/env python3
from pathlib import Path
import numpy as np


def main() -> None:
    print("ScrollGuard local cache inventory")
    print(f"cwd={Path.cwd()}")

    crop_dir = Path("data_cache/crops")
    if not crop_dir.exists():
        raise SystemExit("ERROR missing data_cache/crops")

    npy_files = sorted(crop_dir.glob("*.npy"))
    print(f"npy_crop_count={len(npy_files)}")

    if not npy_files:
        raise SystemExit("ERROR no local cached .npy crops found")

    for p in npy_files:
        arr = np.load(p)
        print(
            "CROP "
            f"{p} "
            f"shape={arr.shape} "
            f"dtype={arr.dtype} "
            f"min={arr.min()} "
            f"max={arr.max()} "
            f"bytes={p.stat().st_size}"
        )

    print("OK local cache inventory complete")
    print("No Vesuvius server access used.")


if __name__ == "__main__":
    main()
