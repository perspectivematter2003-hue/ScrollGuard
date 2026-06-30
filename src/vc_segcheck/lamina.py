from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class LaminaField:
    lamina_coord: np.ndarray
    lamina_index: np.ndarray
    confidence: np.ndarray
    spacing_voxels: float
    reference_coord: float


def assign_lamina_index_field(
    lamina_coord: np.ndarray,
    spacing_voxels: float,
    reference_coord: float = 0.0,
    confidence: np.ndarray | None = None,
) -> LaminaField:
    coord = np.asarray(lamina_coord, dtype=float)

    if spacing_voxels <= 0:
        raise ValueError(f"spacing_voxels must be positive, got {spacing_voxels}")

    raw = (coord - float(reference_coord)) / float(spacing_voxels)
    k = np.rint(raw).astype(np.int32)

    if confidence is None:
        conf = np.ones(coord.shape, dtype=np.float32)
    else:
        conf = np.asarray(confidence, dtype=np.float32)
        if conf.shape != coord.shape:
            raise ValueError(f"confidence shape mismatch: {conf.shape} vs {coord.shape}")

    return LaminaField(
        lamina_coord=coord.astype(np.float32),
        lamina_index=k,
        confidence=conf,
        spacing_voxels=float(spacing_voxels),
        reference_coord=float(reference_coord),
    )


def save_lamina_field_report(field: LaminaField, out_dir: str | Path) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    unique, counts = np.unique(field.lamina_index, return_counts=True)
    histogram = {str(int(k)): int(v) for k, v in zip(unique, counts)}

    report = {
        "method": "vc_segcheck.lamina.save_lamina_field_report.v0",
        "shape": list(field.lamina_index.shape),
        "spacing_voxels": field.spacing_voxels,
        "reference_coord": field.reference_coord,
        "index_histogram": histogram,
        "mean_confidence": float(np.mean(field.confidence)),
        "min_confidence": float(np.min(field.confidence)),
    }

    (out_dir / "lamina_field_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    np.save(out_dir / "lamina_coord.npy", field.lamina_coord)
    np.save(out_dir / "lamina_index.npy", field.lamina_index)
    np.save(out_dir / "lamina_confidence.npy", field.confidence)

    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_axes([0.12, 0.10, 0.78, 0.82])
    im = ax.imshow(field.lamina_index)
    ax.set_title("Lamina index field")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.savefig(out_dir / "lamina_index.png", dpi=140)
    plt.close(fig)

    return report
