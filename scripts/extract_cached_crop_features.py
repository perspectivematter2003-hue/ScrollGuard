from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from scrollguard.features import basic_image_features, summarize_features, save_feature_summary

CACHE_PATH = Path("data_cache/crops/Scroll1_z1000_y3520_3584_x4256_4320.npy")
FEATURE_DIR = Path("data_cache/features/gate_a_tiny_crop")
PREVIEW_DIR = Path("outputs/features/gate_a_tiny_crop")

crop = np.load(CACHE_PATH)
features = basic_image_features(crop)
summary = summarize_features(crop, features)

FEATURE_DIR.mkdir(parents=True, exist_ok=True)
PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

for name, arr in features.items():
    np.save(FEATURE_DIR / f"{name}.npy", arr)

for name in ["normalized", "gradient_magnitude", "local_std"]:
    plt.figure()
    plt.imshow(features[name], cmap="gray")
    plt.axis("off")
    out = PREVIEW_DIR / f"{name}.png"
    plt.savefig(out, dpi=200, bbox_inches="tight", pad_inches=0)
    plt.close()

save_feature_summary(summary, PREVIEW_DIR / "feature_summary.json")

print("OK extracted Month 3 v0 features")
print(summary)
print(f"saved_arrays={FEATURE_DIR}")
print(f"saved_previews={PREVIEW_DIR}")
