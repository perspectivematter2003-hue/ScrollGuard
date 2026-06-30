from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json
from typing import Literal

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


Axis = Literal["x", "y"]


@dataclass
class ProfileRecord:
    vertex_id: int
    y: int
    x: int
    axis: str
    profile_start: int
    profile_end: int
    profile_length: int
    min_value: float
    max_value: float
    mean_value: float
    profile_png: str


def load_cached_crop(path: str | Path) -> np.ndarray:
    crop = np.load(Path(path))
    if crop.ndim != 2:
        raise ValueError(f"Expected 2D cached crop, got shape={crop.shape}")
    return np.asarray(crop)


def choose_grid_points(shape: tuple[int, int], n: int) -> list[tuple[int, int]]:
    if n <= 0:
        raise ValueError("--vertices must be positive")

    h, w = shape
    margin_y = max(2, h // 8)
    margin_x = max(2, w // 8)

    rows = int(np.ceil(np.sqrt(n)))
    cols = int(np.ceil(n / rows))

    ys = np.linspace(margin_y, h - margin_y - 1, rows).round().astype(int)
    xs = np.linspace(margin_x, w - margin_x - 1, cols).round().astype(int)

    points: list[tuple[int, int]] = []
    for y in ys:
        for x in xs:
            points.append((int(y), int(x)))
            if len(points) >= n:
                return points
    return points


def extract_axis_profile(
    crop: np.ndarray,
    y: int,
    x: int,
    axis: Axis,
    half_width: int,
) -> tuple[np.ndarray, int, int]:
    if half_width <= 0:
        raise ValueError("--half-width must be positive")

    h, w = crop.shape

    if axis == "y":
        start = max(0, y - half_width)
        end = min(h, y + half_width + 1)
        profile = crop[start:end, x]
    elif axis == "x":
        start = max(0, x - half_width)
        end = min(w, x + half_width + 1)
        profile = crop[y, start:end]
    else:
        raise ValueError(f"Unsupported axis={axis!r}")

    return np.asarray(profile, dtype=float), int(start), int(end)


def save_profile_png(
    crop: np.ndarray,
    profile: np.ndarray,
    y: int,
    x: int,
    axis: Axis,
    out_path: str | Path,
) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(8, 3))

    ax1 = fig.add_axes([0.06, 0.18, 0.34, 0.72])
    ax1.imshow(crop, cmap="gray")
    ax1.scatter([x], [y], s=18)
    if axis == "y":
        ax1.axvline(x)
    else:
        ax1.axhline(y)
    ax1.set_title(f"sample y={y}, x={x}, axis={axis}")
    ax1.set_xticks([])
    ax1.set_yticks([])

    ax2 = fig.add_axes([0.50, 0.18, 0.45, 0.72])
    ax2.plot(np.arange(len(profile)), profile)
    ax2.set_title("1D CT intensity profile")
    ax2.set_xlabel("sample index")
    ax2.set_ylabel("intensity")

    fig.savefig(out_path, dpi=140)
    plt.close(fig)


def run_cached_crop_profile_smoke(
    cached_crop: str | Path,
    vertices: int,
    out_dir: str | Path,
    axis: Axis = "y",
    half_width: int = 15,
) -> list[ProfileRecord]:
    crop = load_cached_crop(cached_crop)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    points = choose_grid_points(crop.shape, vertices)
    records: list[ProfileRecord] = []

    for idx, (y, x) in enumerate(points, start=1):
        profile, start, end = extract_axis_profile(crop, y, x, axis, half_width)
        png_path = out_dir / f"vertex_{idx:04d}.png"
        save_profile_png(crop, profile, y, x, axis, png_path)

        records.append(
            ProfileRecord(
                vertex_id=idx,
                y=y,
                x=x,
                axis=axis,
                profile_start=start,
                profile_end=end,
                profile_length=int(len(profile)),
                min_value=float(np.min(profile)),
                max_value=float(np.max(profile)),
                mean_value=float(np.mean(profile)),
                profile_png=str(png_path),
            )
        )

    summary = {
        "method": "vc_segcheck.sampler.run_cached_crop_profile_smoke.v0",
        "source": str(cached_crop),
        "crop_shape": list(crop.shape),
        "vertices": vertices,
        "axis": axis,
        "half_width": half_width,
        "server_access": False,
        "records": [asdict(r) for r in records],
    }
    (out_dir / "profiles.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    return records
