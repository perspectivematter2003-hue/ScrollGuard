from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from vc_segcheck.normal_profile import run_normal_profile_sampler
from vc_segcheck.surface import sample_surface_with_normals
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.lcc_surface_smoke_test import OUT, write_synthetic_tifxyz


PROFILE_OUT = Path("profiles/lcc_normal_profile_smoke")


def make_synthetic_lamina_volume() -> np.ndarray:
    depth, height, width = 1032, 64, 64
    zz, yy, xx = np.mgrid[0:depth, 0:height, 0:width].astype(np.float32)

    lamina_period = 6.0
    bands = 0.5 + 0.5 * np.cos(2.0 * np.pi * (zz - 1000.0) / lamina_period)
    slow_gradient = 0.01 * xx + 0.02 * yy

    volume = 60.0 + 150.0 * bands + slow_gradient
    return volume.astype(np.float32)


def build_contact_sheet(out_dir: Path) -> Path:
    imgs = sorted(out_dir.glob("normal_profile_*.png"))
    if not imgs:
        raise RuntimeError("No normal profile PNGs found")

    thumbs = []
    for p in imgs:
        im = Image.open(p).convert("RGB")
        im.thumbnail((360, 150))
        canvas = Image.new("RGB", (380, 180), "white")
        canvas.paste(im, (10, 10))
        d = ImageDraw.Draw(canvas)
        d.text((10, 158), p.name, fill=(0, 0, 0))
        thumbs.append(canvas)

    cols = 2
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 380, rows * 180), "white")

    for i, im in enumerate(thumbs):
        x = (i % cols) * 380
        y = (i // cols) * 180
        sheet.paste(im, (x, y))

    out = out_dir / "contact_sheet.png"
    sheet.save(out)
    return out


def main() -> None:
    write_synthetic_tifxyz(OUT)

    samples = sample_surface_with_normals(OUT, n=40)
    volume = make_synthetic_lamina_volume()

    records = run_normal_profile_sampler(
        volume=volume,
        samples=samples,
        out_dir=PROFILE_OUT,
        half_width=15,
        step=1.0,
    )

    if len(records) < 20:
        raise RuntimeError(f"Expected at least 20 profiles, got {len(records)}")

    png_count = len(list(PROFILE_OUT.glob("normal_profile_*.png")))
    if png_count != len(records):
        raise RuntimeError(f"PNG/profile mismatch: png_count={png_count}, records={len(records)}")

    contact_sheet = build_contact_sheet(PROFILE_OUT)

    print("OK LCC normal-profile smoke test passed")
    print(f"surface={OUT}")
    print(f"volume_shape={volume.shape}")
    print(f"profiles={len(records)}")
    print(f"out_dir={PROFILE_OUT}")
    print(f"contact_sheet={contact_sheet}")


if __name__ == "__main__":
    main()
