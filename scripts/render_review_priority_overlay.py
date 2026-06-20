from pathlib import Path
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

crop = np.load("data_cache/crops/Scroll1_z1000_y3520_3584_x4256_4320.npy")
risk_map = np.load("data_cache/quality/gate_a_tiny_crop/risk_map.npy")

csv_path = Path("outputs/review/gate_a_tiny_crop/review_priority.csv")
out_path = Path("outputs/review/gate_a_tiny_crop/review_priority_overlay.png")

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
print(f"output={out_path}")
print("Top records:")
for record in top_records:
    print(record)
