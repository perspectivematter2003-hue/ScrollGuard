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
from scrollguard.quality_scorer import (
    score_surface_quality,
    summarize_quality,
    save_quality_summary,
)


item = get_manifest_item("gate_a_tiny_crop")

feature_set = f"{item.name}_quality_v0"

feature_dir = item.feature_cache_dir
quality_cache_dir = item.quality_cache_dir
quality_out_dir = item.quality_output_dir

quality_cache_dir.mkdir(parents=True, exist_ok=True)
quality_out_dir.mkdir(parents=True, exist_ok=True)

gradient = np.load(feature_dir / "gradient_magnitude.npy")
local_std = np.load(feature_dir / "local_std.npy")
coherence = np.load(feature_dir / "texture_coherence.npy")

outputs = score_surface_quality(
    gradient_magnitude=gradient,
    local_std=local_std,
    texture_coherence=coherence,
)

for name, arr in outputs.items():
    np.save(quality_cache_dir / f"{name}.npy", arr)

for name in ["quality_map", "risk_map", "smoothness_score", "stability_score", "texture_score"]:
    plt.figure()
    plt.imshow(outputs[name], cmap="gray")
    plt.axis("off")
    out = quality_out_dir / f"{name}.png"
    plt.savefig(out, dpi=200, bbox_inches="tight", pad_inches=0)
    plt.close()

evidence_source = {
    "source_crop_cache": str(item.crop_cache_path),
    "source_metadata": f"outputs/{item.name}_metadata.json",
    "feature_dir": str(feature_dir),
    "feature_index": "outputs/features/feature_index.csv",
    "inputs": [
        "gradient_magnitude.npy",
        "local_std.npy",
        "texture_coherence.npy",
    ],
}

summary = summarize_quality(feature_set, outputs, evidence_source)
save_quality_summary(summary, quality_out_dir / "quality_summary.json")

print("OK scored surface quality v0")
print(f"crop_name={item.name}")
print(summary)
print(f"saved_quality_cache={quality_cache_dir}")
print(f"saved_quality_outputs={quality_out_dir}")
print("No Vesuvius server access used.")
