from pathlib import Path
import csv
import json
from typing import Iterable

import numpy as np


FIELDS = [
    "rank",
    "review_id",
    "scan_id",
    "z",
    "tile_y0",
    "tile_y1",
    "tile_x0",
    "tile_x1",
    "voxel_y0",
    "voxel_y1",
    "voxel_x0",
    "voxel_x1",
    "risk_mean",
    "risk_max",
    "quality_mean",
    "quality_min",
    "method",
]


def extract_review_tiles(
    risk_map: np.ndarray,
    quality_map: np.ndarray,
    metadata: dict,
    tile_size: int = 16,
) -> list[dict]:
    if risk_map.shape != quality_map.shape:
        raise ValueError("risk_map and quality_map shapes must match")

    y_base = metadata["y_range"][0]
    x_base = metadata["x_range"][0]
    scan_id = metadata["scan_id"]
    z = metadata["z"]

    records = []
    h, w = risk_map.shape

    for y0 in range(0, h, tile_size):
        for x0 in range(0, w, tile_size):
            y1 = min(y0 + tile_size, h)
            x1 = min(x0 + tile_size, w)

            risk_tile = risk_map[y0:y1, x0:x1]
            quality_tile = quality_map[y0:y1, x0:x1]

            records.append({
                "scan_id": scan_id,
                "z": z,
                "tile_y0": y0,
                "tile_y1": y1,
                "tile_x0": x0,
                "tile_x1": x1,
                "voxel_y0": y_base + y0,
                "voxel_y1": y_base + y1,
                "voxel_x0": x_base + x0,
                "voxel_x1": x_base + x1,
                "risk_mean": float(np.mean(risk_tile)),
                "risk_max": float(np.max(risk_tile)),
                "quality_mean": float(np.mean(quality_tile)),
                "quality_min": float(np.min(quality_tile)),
                "method": "scrollguard.review_priority.extract_review_tiles.v0",
            })

    records.sort(key=lambda r: (r["risk_mean"], r["risk_max"]), reverse=True)

    for idx, record in enumerate(records, start=1):
        record["rank"] = idx
        record["review_id"] = f"{scan_id}_z{z}_tile_{idx:04d}"

    return records


def write_jsonl(records: Iterable[dict], out_path: str | Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")


def write_csv(records: list[dict], out_path: str | Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for record in records:
            writer.writerow({field: record.get(field, "") for field in FIELDS})
