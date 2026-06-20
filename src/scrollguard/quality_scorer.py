from dataclasses import dataclass, asdict
from pathlib import Path
import json

import numpy as np


@dataclass
class QualityScoreSummary:
    feature_set: str
    input_shape: tuple[int, int]
    quality_min: float
    quality_max: float
    quality_mean: float
    risk_min: float
    risk_max: float
    risk_mean: float
    method: str
    evidence_source: dict


def normalize01_safe(arr: np.ndarray) -> np.ndarray:
    arr = arr.astype(np.float32)
    mn = float(np.min(arr))
    mx = float(np.max(arr))
    if mx <= mn:
        return np.zeros_like(arr, dtype=np.float32)
    return (arr - mn) / (mx - mn)


def score_surface_quality(
    gradient_magnitude: np.ndarray,
    local_std: np.ndarray,
    texture_coherence: np.ndarray,
) -> dict[str, np.ndarray]:
    grad_n = normalize01_safe(gradient_magnitude)
    std_n = normalize01_safe(local_std)
    coh_n = np.clip(texture_coherence.astype(np.float32), 0.0, 1.0)

    smoothness_score = 1.0 - grad_n
    stability_score = 1.0 - std_n
    texture_score = coh_n

    quality = (
        0.40 * texture_score +
        0.35 * smoothness_score +
        0.25 * stability_score
    )

    quality = np.clip(quality, 0.0, 1.0)
    risk = 1.0 - quality

    return {
        "quality_map": quality.astype(np.float32),
        "risk_map": risk.astype(np.float32),
        "smoothness_score": smoothness_score.astype(np.float32),
        "stability_score": stability_score.astype(np.float32),
        "texture_score": texture_score.astype(np.float32),
    }


def summarize_quality(
    feature_set: str,
    quality_outputs: dict[str, np.ndarray],
    evidence_source: dict,
) -> QualityScoreSummary:
    quality = quality_outputs["quality_map"]
    risk = quality_outputs["risk_map"]

    return QualityScoreSummary(
        feature_set=feature_set,
        input_shape=tuple(quality.shape),
        quality_min=float(np.min(quality)),
        quality_max=float(np.max(quality)),
        quality_mean=float(np.mean(quality)),
        risk_min=float(np.min(risk)),
        risk_max=float(np.max(risk)),
        risk_mean=float(np.mean(risk)),
        method="scrollguard.quality_scorer.score_surface_quality.v0",
        evidence_source=evidence_source,
    )


def save_quality_summary(summary: QualityScoreSummary, out_path: str | Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(asdict(summary), indent=2), encoding="utf-8")
