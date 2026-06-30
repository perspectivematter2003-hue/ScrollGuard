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
feature_dir = item.feature_cache_dir
out_path = item.feature_output_dir / "contact_sheet.png"

items = [
    ("original_crop", np.load(crop_path)),
    ("normalized", np.load(feature_dir / "normalized.npy")),
    ("gradient_magnitude", np.load(feature_dir / "gradient_magnitude.npy")),
    ("local_std", np.load(feature_dir / "local_std.npy")),
    ("texture_coherence", np.load(feature_dir / "texture_coherence.npy")),
    ("texture_orientation", np.load(feature_dir / "texture_orientation.npy")),
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

print("OK rendered feature contact sheet")
print(f"crop_name={item.name}")
print(f"output={out_path}")
print("No Vesuvius server access used.")
