from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

CACHE_PATH = Path("data_cache/crops/Scroll1_z1000_y3520_3584_x4256_4320.npy")
OUT_PATH = Path("outputs/cached_tiny_crop_preview.png")

if not CACHE_PATH.exists():
    raise FileNotFoundError(
        f"Missing cache file: {CACHE_PATH}. Run scripts/cache_tiny_crop.py first."
    )

crop = np.load(CACHE_PATH)

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
plt.imshow(crop, cmap="gray")
plt.axis("off")
plt.savefig(OUT_PATH, dpi=200, bbox_inches="tight", pad_inches=0)

print("OK rendered cached crop preview")
print(f"input={CACHE_PATH}")
print(f"output={OUT_PATH}")
print(f"shape={crop.shape}, dtype={crop.dtype}, min={crop.min()}, max={crop.max()}, mean={crop.mean():.4f}")
