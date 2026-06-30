from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import tifffile


@dataclass
class SurfaceSample:
    row: int
    col: int
    x: float
    y: float
    z: float
    nx: float
    ny: float
    nz: float


@dataclass
class TifxyzSurface:
    x: np.ndarray
    y: np.ndarray
    z: np.ndarray
    mask: np.ndarray | None
    path: Path

    @property
    def shape(self) -> tuple[int, int]:
        return self.x.shape

    @property
    def _valid_mask(self) -> np.ndarray:
        if self.mask is not None:
            return self.mask.astype(bool)
        return (self.z > 0) & np.isfinite(self.z)

    def __getitem__(self, key):
        valid = self._valid_mask
        return self.x[key], self.y[key], self.z[key], valid[key]

    def compute_normals(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        x = self.x.astype(np.float32, copy=False)
        y = self.y.astype(np.float32, copy=False)
        z = self.z.astype(np.float32, copy=False)
        valid = self._valid_mask

        h, w = x.shape
        nx = np.full((h, w), np.nan, dtype=np.float32)
        ny = np.full((h, w), np.nan, dtype=np.float32)
        nz = np.full((h, w), np.nan, dtype=np.float32)

        if h < 3 or w < 3:
            return nx, ny, nz

        interior_valid = (
            valid[1:-1, 1:-1]
            & valid[1:-1, :-2]
            & valid[1:-1, 2:]
            & valid[:-2, 1:-1]
            & valid[2:, 1:-1]
        )

        tx_x = x[1:-1, 2:] - x[1:-1, :-2]
        tx_y = y[1:-1, 2:] - y[1:-1, :-2]
        tx_z = z[1:-1, 2:] - z[1:-1, :-2]

        ty_x = x[2:, 1:-1] - x[:-2, 1:-1]
        ty_y = y[2:, 1:-1] - y[:-2, 1:-1]
        ty_z = z[2:, 1:-1] - z[:-2, 1:-1]

        n_x = ty_y * tx_z - ty_z * tx_y
        n_y = ty_z * tx_x - ty_x * tx_z
        n_z = ty_x * tx_y - ty_y * tx_x

        norm = np.sqrt(n_x**2 + n_y**2 + n_z**2)
        norm = np.where(norm > 1e-10, norm, np.nan)

        n_x = np.where(interior_valid, n_x / norm, np.nan)
        n_y = np.where(interior_valid, n_y / norm, np.nan)
        n_z = np.where(interior_valid, n_z / norm, np.nan)

        nx[1:-1, 1:-1] = n_x.astype(np.float32)
        ny[1:-1, 1:-1] = n_y.astype(np.float32)
        nz[1:-1, 1:-1] = n_z.astype(np.float32)

        return nx, ny, nz


def load_tifxyz_surface(path: str | Path) -> TifxyzSurface:
    path = Path(path)

    required = ["x.tif", "y.tif", "z.tif"]
    missing = [name for name in required if not (path / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing tifxyz files in {path}: {missing}")

    x = tifffile.imread(path / "x.tif").astype(np.float32)
    y = tifffile.imread(path / "y.tif").astype(np.float32)
    z = tifffile.imread(path / "z.tif").astype(np.float32)

    if x.shape != y.shape or x.shape != z.shape:
        raise ValueError(f"Shape mismatch: x={x.shape}, y={y.shape}, z={z.shape}")

    mask_path = path / "mask.tif"
    mask = None
    if mask_path.exists():
        mask = tifffile.imread(mask_path).astype(bool)
        if mask.shape != x.shape:
            raise ValueError(f"Mask shape mismatch: mask={mask.shape}, xyz={x.shape}")

    return TifxyzSurface(x=x, y=y, z=z, mask=mask, path=path)


def sample_valid_surface_points(surface: TifxyzSurface, n: int) -> list[tuple[int, int]]:
    if n <= 0:
        raise ValueError("n must be positive")

    valid = surface._valid_mask
    rows, cols = np.where(valid)

    if len(rows) == 0:
        raise ValueError("Surface has no valid points")

    idx = np.linspace(0, len(rows) - 1, min(n, len(rows))).round().astype(int)
    return [(int(rows[i]), int(cols[i])) for i in idx]


def sample_surface_with_normals(path: str | Path, n: int) -> list[SurfaceSample]:
    surface = load_tifxyz_surface(path)
    nx, ny, nz = surface.compute_normals()

    points = sample_valid_surface_points(surface, n)
    samples: list[SurfaceSample] = []

    for row, col in points:
        x, y, z, valid = surface[row, col]

        if not bool(np.asarray(valid).reshape(-1)[0]):
            continue

        normal = np.array([nx[row, col], ny[row, col], nz[row, col]], dtype=float)
        if not np.isfinite(normal).all():
            continue

        samples.append(
            SurfaceSample(
                row=row,
                col=col,
                x=float(np.asarray(x).reshape(-1)[0]),
                y=float(np.asarray(y).reshape(-1)[0]),
                z=float(np.asarray(z).reshape(-1)[0]),
                nx=float(normal[0]),
                ny=float(normal[1]),
                nz=float(normal[2]),
            )
        )

    return samples
