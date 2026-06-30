from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class SpacingEstimate:
    profile_id: int
    spacing_voxels: float
    confidence: float
    peak_lag: int
    valid: bool
    reason: str


def _finite_centered(values: np.ndarray) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return arr
    arr = arr - float(np.mean(arr))
    return arr


def estimate_spacing_autocorr(
    values: list[float] | np.ndarray,
    min_lag: int = 2,
    max_lag: int = 15,
) -> SpacingEstimate:
    arr = _finite_centered(np.asarray(values, dtype=float))

    if arr.size < (max_lag + 3):
        return SpacingEstimate(
            profile_id=-1,
            spacing_voxels=float("nan"),
            confidence=0.0,
            peak_lag=-1,
            valid=False,
            reason=f"too_few_finite_values:{arr.size}",
        )

    energy = float(np.dot(arr, arr))
    if not np.isfinite(energy) or energy <= 1e-9:
        return SpacingEstimate(
            profile_id=-1,
            spacing_voxels=float("nan"),
            confidence=0.0,
            peak_lag=-1,
            valid=False,
            reason="low_energy",
        )

    acf_full = np.correlate(arr, arr, mode="full")
    acf = acf_full[arr.size - 1 :]
    acf = acf / max(float(acf[0]), 1e-9)

    max_lag = min(max_lag, len(acf) - 1)
    if max_lag < min_lag:
        return SpacingEstimate(
            profile_id=-1,
            spacing_voxels=float("nan"),
            confidence=0.0,
            peak_lag=-1,
            valid=False,
            reason="lag_window_invalid",
        )

    window = acf[min_lag : max_lag + 1]
    local_idx = int(np.argmax(window))
    peak_lag = int(min_lag + local_idx)
    confidence = float(window[local_idx])

    valid = bool(np.isfinite(confidence) and confidence >= 0.25)

    return SpacingEstimate(
        profile_id=-1,
        spacing_voxels=float(peak_lag),
        confidence=confidence,
        peak_lag=peak_lag,
        valid=valid,
        reason="ok" if valid else "low_autocorr_confidence",
    )


def estimate_spacing_from_profiles_json(
    profiles_json: str | Path,
    out_dir: str | Path,
    min_lag: int = 2,
    max_lag: int = 15,
) -> list[SpacingEstimate]:
    profiles_json = Path(profiles_json)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    data = json.loads(profiles_json.read_text(encoding="utf-8"))
    profiles = data["profiles"]

    estimates: list[SpacingEstimate] = []

    for idx, profile in enumerate(profiles, start=1):
        est = estimate_spacing_autocorr(
            values=profile["values"],
            min_lag=min_lag,
            max_lag=max_lag,
        )
        est.profile_id = idx
        estimates.append(est)

    valid_spacings = np.array([e.spacing_voxels for e in estimates if e.valid], dtype=float)
    valid_conf = np.array([e.confidence for e in estimates if e.valid], dtype=float)

    summary = {
        "method": "vc_segcheck.spacing.estimate_spacing_from_profiles_json.v0",
        "source_profiles_json": str(profiles_json),
        "min_lag": min_lag,
        "max_lag": max_lag,
        "num_profiles": len(estimates),
        "num_valid": int(sum(e.valid for e in estimates)),
        "median_spacing_voxels": float(np.median(valid_spacings)) if valid_spacings.size else None,
        "mean_confidence": float(np.mean(valid_conf)) if valid_conf.size else None,
        "estimates": [asdict(e) for e in estimates],
    }

    report_path = out_dir / "spacing_report.json"
    report_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    fig = plt.figure(figsize=(7, 3))
    ax = fig.add_axes([0.10, 0.18, 0.84, 0.70])
    if valid_spacings.size:
        ax.hist(valid_spacings, bins=np.arange(min_lag, max_lag + 2) - 0.5)
    ax.set_title("Estimated lamina spacing from normal profiles")
    ax.set_xlabel("spacing / voxels")
    ax.set_ylabel("count")
    fig.savefig(out_dir / "spacing_histogram.png", dpi=140)
    plt.close(fig)

    return estimates
