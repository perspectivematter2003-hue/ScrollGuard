#!/usr/bin/env python3
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scrollguard.crop_manifest import get_manifest_item


item = get_manifest_item("gate_a_tiny_crop")

crop_path = item.crop_cache_path
quality_dir = item.quality_cache_dir
out_path = item.quality_output_dir / "quality_contact_sheet.png"

items = [
    ("original_crop", np.load(crop_path)),
    ("quality_map", np.load(quality_dir / "quality_map.npy")),
    ("risk_map", np.load(quality_dir / "risk_map.npy")),
    ("smoothness_score", np.load(quality_dir / "smoothness_score.npy")),
    ("stability_score", np.load(quality_dir / "stability_score.npy")),
    ("texture_score", np.load(quality_dir / "texture_score.npy")),
]

fig, axes = plt.subplots(2, 3, figsize=(9, 6))
for ax, (title, img) in zip(axes.ravel(), items):
    ax.imshow(img, cmap="gray")
    ax.set_title(title)
    ax.axis("off")

out_path.parent.mkdir(parents=True, exist_ok=True)
plt.tight_layout()
plt.savefig(out_path, dpi=200, bbox_inches="tight")
plt.close()

print("OK rendered quality contact sheet")
print(f"crop_name={item.name}")
print(f"output={out_path}")
print("No Vesuvius server access used.")
