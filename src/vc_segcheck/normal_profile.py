from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from vc_segcheck.surface import SurfaceSample


@dataclass
class NormalProfile:
    sample_id: int
    row: int
    col: int
    center_xyz: tuple[float, float, float]
    normal_xyz: tuple[float, float, float]
    offsets: list[float]
    values: list[float]
    profile_png: str


def sample_trilinear(volume: np.ndarray, xyz: np.ndarray) -> float:
    x, y, z = [float(v) for v in xyz]
    depth, height, width = volume.shape

    if x < 0 or y < 0 or z < 0 or x > width - 1 or y > height - 1 or z > depth - 1:
        return float("nan")

    x0 = int(np.floor(x))
    y0 = int(np.floor(y))
    z0 = int(np.floor(z))
    x1 = min(x0 + 1, width - 1)
    y1 = min(y0 + 1, height - 1)
    z1 = min(z0 + 1, depth - 1)

    xd = x - x0
    yd = y - y0
    zd = z - z0

    c000 = volume[z0, y0, x0]
    c100 = volume[z0, y0, x1]
    c010 = volume[z0, y1, x0]
    c110 = volume[z0, y1, x1]
    c001 = volume[z1, y0, x0]
    c101 = volume[z1, y0, x1]
    c011 = volume[z1, y1, x0]
    c111 = volume[z1, y1, x1]

    c00 = c000 * (1 - xd) + c100 * xd
    c10 = c010 * (1 - xd) + c110 * xd
    c01 = c001 * (1 - xd) + c101 * xd
    c11 = c011 * (1 - xd) + c111 * xd

    c0 = c00 * (1 - yd) + c10 * yd
    c1 = c01 * (1 - yd) + c11 * yd

    return float(c0 * (1 - zd) + c1 * zd)


def sample_profile_along_normal(
    volume: np.ndarray,
    center_xyz: tuple[float, float, float],
    normal_xyz: tuple[float, float, float],
    half_width: int = 15,
    step: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    normal = np.asarray(normal_xyz, dtype=float)
    norm = float(np.linalg.norm(normal))
    if not np.isfinite(norm) or norm <= 1e-12:
        raise ValueError(f"Invalid normal: {normal_xyz}")

    normal = normal / norm
    center = np.asarray(center_xyz, dtype=float)

    offsets = np.arange(-half_width, half_width + 1, dtype=float) * float(step)
    values = np.array(
        [sample_trilinear(volume, center + offset * normal) for offset in offsets],
        dtype=float,
    )
    return offsets, values


def save_normal_profile_png(
    offsets: np.ndarray,
    values: np.ndarray,
    out_path: str | Path,
    title: str,
) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(6, 3))
    ax = fig.add_axes([0.12, 0.18, 0.82, 0.70])
    ax.plot(offsets, values)
    ax.axvline(0.0)
    ax.set_title(title)
    ax.set_xlabel("normal offset / voxels")
    ax.set_ylabel("CT intensity")
    fig.savefig(out_path, dpi=140)
    plt.close(fig)


def run_normal_profile_sampler(
    volume: np.ndarray,
    samples: list[SurfaceSample],
    out_dir: str | Path,
    half_width: int = 15,
    step: float = 1.0,
) -> list[NormalProfile]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    records: list[NormalProfile] = []

    for idx, sample in enumerate(samples, start=1):
        center_xyz = (sample.x, sample.y, sample.z)
        normal_xyz = (sample.nx, sample.ny, sample.nz)
        offsets, values = sample_profile_along_normal(
            volume=volume,
            center_xyz=center_xyz,
            normal_xyz=normal_xyz,
            half_width=half_width,
            step=step,
        )

        png_path = out_dir / f"normal_profile_{idx:04d}.png"
        save_normal_profile_png(
            offsets=offsets,
            values=values,
            out_path=png_path,
            title=f"sample={idx} row={sample.row} col={sample.col}",
        )

        records.append(
            NormalProfile(
                sample_id=idx,
                row=sample.row,
                col=sample.col,
                center_xyz=center_xyz,
                normal_xyz=normal_xyz,
                offsets=[float(x) for x in offsets],
                values=[float(x) for x in values],
                profile_png=str(png_path),
            )
        )

    summary = {
        "method": "vc_segcheck.normal_profile.run_normal_profile_sampler.v0",
        "volume_shape_zyx": list(volume.shape),
        "half_width": half_width,
        "step": step,
        "profiles": [asdict(record) for record in records],
    }
    (out_dir / "normal_profiles.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    return records
