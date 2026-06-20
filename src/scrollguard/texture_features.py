from dataclasses import dataclass, asdict
from pathlib import Path
import json

import numpy as np
from scipy import ndimage

from scrollguard.features import normalize01


@dataclass
class TextureFeatureSummary:
    input_shape: tuple[int, int]
    coherence_min: float
    coherence_max: float
    coherence_mean: float
    orientation_min: float
    orientation_max: float
    orientation_mean: float
    method: str


def structure_tensor_texture_features(img: np.ndarray, sigma: float = 1.5) -> dict[str, np.ndarray]:
    norm = normalize01(img)

    gy = ndimage.sobel(norm, axis=0)
    gx = ndimage.sobel(norm, axis=1)

    jxx = ndimage.gaussian_filter(gx * gx, sigma=sigma)
    jyy = ndimage.gaussian_filter(gy * gy, sigma=sigma)
    jxy = ndimage.gaussian_filter(gx * gy, sigma=sigma)

    trace = jxx + jyy
    diff = jxx - jyy
    root = np.sqrt(diff * diff + 4.0 * jxy * jxy)

    lambda1 = 0.5 * (trace + root)
    lambda2 = 0.5 * (trace - root)

    coherence = (lambda1 - lambda2) / (lambda1 + lambda2 + 1e-8)
    orientation = 0.5 * np.arctan2(2.0 * jxy, diff)

    return {
        "texture_coherence": coherence.astype(np.float32),
        "texture_orientation": orientation.astype(np.float32),
        "tensor_lambda1": lambda1.astype(np.float32),
        "tensor_lambda2": lambda2.astype(np.float32),
    }


def summarize_texture_features(features: dict[str, np.ndarray]) -> TextureFeatureSummary:
    coherence = features["texture_coherence"]
    orientation = features["texture_orientation"]

    return TextureFeatureSummary(
        input_shape=tuple(coherence.shape),
        coherence_min=float(np.min(coherence)),
        coherence_max=float(np.max(coherence)),
        coherence_mean=float(np.mean(coherence)),
        orientation_min=float(np.min(orientation)),
        orientation_max=float(np.max(orientation)),
        orientation_mean=float(np.mean(orientation)),
        method="scrollguard.texture_features.structure_tensor_texture_features.v0",
    )


def save_texture_summary(summary: TextureFeatureSummary, out_path: str | Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(asdict(summary), indent=2), encoding="utf-8")
