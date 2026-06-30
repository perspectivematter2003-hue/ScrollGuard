from pathlib import Path
from PIL import Image, ImageDraw

from vc_segcheck.sampler import run_cached_crop_profile_smoke

CACHED_CROP = "data_cache/crops/Scroll1_z1000_y3520_3584_x4256_4320.npy"
OUT_DIR = Path("profiles/lcc_day1_smoke")


def build_contact_sheet(out_dir: Path) -> Path:
    imgs = sorted(out_dir.glob("vertex_*.png"))
    if len(imgs) != 40:
        raise RuntimeError(f"Expected 40 profile PNGs, found {len(imgs)}")

    thumbs = []
    for p in imgs:
        im = Image.open(p).convert("RGB")
        im.thumbnail((360, 140))
        canvas = Image.new("RGB", (380, 170), "white")
        canvas.paste(im, (10, 10))
        d = ImageDraw.Draw(canvas)
        d.text((10, 148), p.name, fill=(0, 0, 0))
        thumbs.append(canvas)

    cols = 2
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 380, rows * 170), "white")

    for i, im in enumerate(thumbs):
        x = (i % cols) * 380
        y = (i // cols) * 170
        sheet.paste(im, (x, y))

    out = out_dir / "contact_sheet.png"
    sheet.save(out)
    return out


def main() -> None:
    records = run_cached_crop_profile_smoke(
        cached_crop=CACHED_CROP,
        vertices=40,
        out_dir=OUT_DIR,
        axis="y",
        half_width=15,
    )

    if len(records) != 40:
        raise RuntimeError(f"Expected 40 records, found {len(records)}")

    contact_sheet = build_contact_sheet(OUT_DIR)

    print("OK LCC Day-1 cached-crop smoke test passed")
    print(f"profiles={len(records)}")
    print(f"out_dir={OUT_DIR}")
    print(f"contact_sheet={contact_sheet}")
    print("No Vesuvius server access used.")


if __name__ == "__main__":
    main()
