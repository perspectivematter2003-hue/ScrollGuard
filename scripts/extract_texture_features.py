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
from scrollguard.texture_features import (
    structure_tensor_texture_features,
    summarize_texture_features,
    save_texture_summary,
)


item = get_manifest_item("gate_a_tiny_crop")

CACHE_PATH = item.crop_cache_path
FEATURE_DIR = item.feature_cache_dir
PREVIEW_DIR = item.feature_output_dir

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
print(f"crop_name={item.name}")
print(summary)
print("No Vesuvius server access used.")
