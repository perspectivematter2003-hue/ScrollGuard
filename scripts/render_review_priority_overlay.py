#!/usr/bin/env python3
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scrollguard.crop_manifest import get_manifest_item


item = get_manifest_item("gate_a_tiny_crop")

crop = np.load(item.crop_cache_path)
risk_map = np.load(item.quality_cache_dir / "risk_map.npy")

csv_path = item.review_output_dir / "review_priority.csv"
out_path = item.review_output_dir / "review_priority_overlay.png"

with csv_path.open("r", encoding="utf-8") as f:
    records = list(csv.DictReader(f))

top_records = records[:5]

fig, axes = plt.subplots(1, 2, figsize=(8, 4))

axes[0].imshow(crop, cmap="gray")
axes[0].set_title("original + top risk tiles")
axes[0].axis("off")

axes[1].imshow(risk_map, cmap="gray")
axes[1].set_title("risk map + top risk tiles")
axes[1].axis("off")

for record in top_records:
    rank = int(record["rank"])
    y0 = int(record["tile_y0"])
    y1 = int(record["tile_y1"])
    x0 = int(record["tile_x0"])
    x1 = int(record["tile_x1"])

    for ax in axes:
        rect = patches.Rectangle(
            (x0, y0),
            x1 - x0,
            y1 - y0,
            fill=False,
            linewidth=1.5,
        )
        ax.add_patch(rect)
        ax.text(x0 + 1, y0 + 8, str(rank), fontsize=8)

out_path.parent.mkdir(parents=True, exist_ok=True)
plt.tight_layout()
plt.savefig(out_path, dpi=200, bbox_inches="tight")
plt.close()

print("OK rendered review-priority overlay")
print(f"crop_name={item.name}")
print(f"output={out_path}")
print("Top records:")
for record in top_records:
    print(record)
print("No Vesuvius server access used.")
