from pathlib import Path
import json

import numpy as np
import tifffile

from vc_segcheck.surface import load_tifxyz_surface, sample_surface_with_normals

OUT = Path("surfaces/lcc_synthetic_tifxyz")


def write_synthetic_tifxyz(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)

    h, w = 64, 64
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)

    x = xx.copy()
    y = yy.copy()
    z = (1000.0 + 0.05 * xx + 0.10 * yy + 2.0 * np.sin(xx / 8.0)).astype(np.float32)
    mask = np.ones((h, w), dtype=np.uint8)

    tifffile.imwrite(out / "x.tif", x)
    tifffile.imwrite(out / "y.tif", y)
    tifffile.imwrite(out / "z.tif", z)
    tifffile.imwrite(out / "mask.tif", mask)

    meta = {
        "uuid": "lcc_synthetic_tifxyz",
        "scale": [1.0, 1.0],
        "bbox": [
            [float(x.min()), float(y.min()), float(z.min())],
            [float(x.max()), float(y.max()), float(z.max())],
        ],
        "area": float(h * w),
        "source": "vc_segcheck synthetic smoke test",
    }
    (out / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")


def main() -> None:
    write_synthetic_tifxyz(OUT)

    surface = load_tifxyz_surface(OUT)
    samples = sample_surface_with_normals(OUT, n=40)

    if surface.shape != (64, 64):
        raise RuntimeError(f"Unexpected surface shape: {surface.shape}")

    if len(samples) < 20:
        raise RuntimeError(f"Too few finite normal samples: {len(samples)}")

    print("OK LCC tifxyz surface smoke test passed")
    print(f"surface={OUT}")
    print(f"shape={surface.shape}")
    print(f"finite_normal_samples={len(samples)}")
    print(f"first_sample={samples[0]}")


if __name__ == "__main__":
    main()
