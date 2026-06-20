from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

crop_path = Path("data_cache/crops/Scroll1_z1000_y3520_3584_x4256_4320.npy")
feature_dir = Path("data_cache/features/gate_a_tiny_crop")
out_path = Path("outputs/features/gate_a_tiny_crop/contact_sheet.png")

crop = np.load(crop_path)

items = [
    ("original_crop", crop),
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

print("OK rendered expanded feature contact sheet")
print(f"output={out_path}")
