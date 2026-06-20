from dataclasses import dataclass, asdict
from pathlib import Path
import json

import numpy as np
from scipy import ndimage


@dataclass
class FeatureSummary:
    input_shape: tuple[int, int]
    input_dtype: str
    gradient_min: float
    gradient_max: float
    gradient_mean: float
    local_std_min: float
    local_std_max: float
    local_std_mean: float
    method: str


def normalize01(img: np.ndarray) -> np.ndarray:
    img = img.astype(np.float32)
    mn = float(np.min(img))
    mx = float(np.max(img))
    if mx <= mn:
        return np.zeros_like(img, dtype=np.float32)
    return (img - mn) / (mx - mn)


def basic_image_features(img: np.ndarray) -> dict[str, np.ndarray]:
    norm = normalize01(img)

    gy = ndimage.sobel(norm, axis=0)
    gx = ndimage.sobel(norm, axis=1)
    gradient_mag = np.sqrt(gx * gx + gy * gy)

    local_mean = ndimage.uniform_filter(norm, size=7)
    local_mean_sq = ndimage.uniform_filter(norm * norm, size=7)
    local_var = np.maximum(local_mean_sq - local_mean * local_mean, 0.0)
    local_std = np.sqrt(local_var)

    return {
        "normalized": norm,
        "gradient_x": gx,
        "gradient_y": gy,
        "gradient_magnitude": gradient_mag,
        "local_mean": local_mean,
        "local_std": local_std,
    }


def summarize_features(img: np.ndarray, features: dict[str, np.ndarray]) -> FeatureSummary:
    gradient = features["gradient_magnitude"]
    local_std = features["local_std"]

    return FeatureSummary(
        input_shape=tuple(img.shape),
        input_dtype=str(img.dtype),
        gradient_min=float(np.min(gradient)),
        gradient_max=float(np.max(gradient)),
        gradient_mean=float(np.mean(gradient)),
        local_std_min=float(np.min(local_std)),
        local_std_max=float(np.max(local_std)),
        local_std_mean=float(np.mean(local_std)),
        method="scrollguard.features.basic_image_features.v0",
    )


def save_feature_summary(summary: FeatureSummary, out_path: str | Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(asdict(summary), indent=2), encoding="utf-8")
