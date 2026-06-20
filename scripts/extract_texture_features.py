from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from scrollguard.texture_features import (
    structure_tensor_texture_features,
    summarize_texture_features,
    save_texture_summary,
)

CACHE_PATH = Path("data_cache/crops/Scroll1_z1000_y3520_3584_x4256_4320.npy")
FEATURE_DIR = Path("data_cache/features/gate_a_tiny_crop")
PREVIEW_DIR = Path("outputs/features/gate_a_tiny_crop")

crop = np.load(CACHE_PATH)
features = structure_tensor_texture_features(crop)
summary = summarize_texture_features(features)

FEATURE_DIR.mkdir(parents=True, exist_ok=True)
PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

for name, arr in features.items():
    np.save(FEATURE_DIR / f"{name}.npy", arr)

for name in ["texture_coherence", "texture_orientation"]:
    plt.figure()
    plt.imshow(features[name], cmap="gray")
    plt.axis("off")
    out = PREVIEW_DIR / f"{name}.png"
    plt.savefig(out, dpi=200, bbox_inches="tight", pad_inches=0)
    plt.close()

save_texture_summary(summary, PREVIEW_DIR / "texture_feature_summary.json")

print("OK extracted texture-continuity features")
print(summary)
