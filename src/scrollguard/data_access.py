from dataclasses import dataclass, asdict
from pathlib import Path
import json
import time
from typing import Tuple, Any

import numpy as np
import vesuvius


@dataclass
class CropRequest:
    scan_id: str
    z: int
    y0: int
    y1: int
    x0: int
    x1: int


@dataclass
class CropMetadata:
    scan_id: str
    z: int
    y_range: Tuple[int, int]
    x_range: Tuple[int, int]
    shape: Tuple[int, int]
    dtype: str
    min_value: float
    max_value: float
    mean_value: float
    created_unix_time: float
    method: str


def load_volume(scan_id: str) -> Any:
    return vesuvius.Volume(scan_id)


def read_crop(request: CropRequest) -> np.ndarray:
    volume = load_volume(request.scan_id)
    crop = volume[request.z, request.y0:request.y1, request.x0:request.x1]
    return np.asarray(crop)


def build_metadata(request: CropRequest, crop: np.ndarray) -> CropMetadata:
    return CropMetadata(
        scan_id=request.scan_id,
        z=request.z,
        y_range=(request.y0, request.y1),
        x_range=(request.x0, request.x1),
        shape=tuple(crop.shape),
        dtype=str(crop.dtype),
        min_value=float(np.min(crop)),
        max_value=float(np.max(crop)),
        mean_value=float(np.mean(crop)),
        created_unix_time=time.time(),
        method="scrollguard.data_access.read_crop.v0",
    )


def save_metadata(metadata: CropMetadata, out_path: str | Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(asdict(metadata), indent=2), encoding="utf-8")
