from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

crop_path = Path("data_cache/crops/Scroll1_z1000_y3520_3584_x4256_4320.npy")
quality_dir = Path("data_cache/quality/gate_a_tiny_crop")
out_path = Path("outputs/quality/gate_a_tiny_crop/quality_contact_sheet.png")

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
print(f"output={out_path}")
