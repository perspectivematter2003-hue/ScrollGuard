from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from collections import deque
import json

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from vc_segcheck.gate import GatedJumpEdge


@dataclass
class JumpRegion:
    region_id: int
    edge_count: int
    bbox_row_min: int
    bbox_col_min: int
    bbox_row_max: int
    bbox_col_max: int
    mean_score: float


def _neighbors8(row: int, col: int, h: int, w: int):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            rr = row + dr
            cc = col + dc
            if 0 <= rr < h and 0 <= cc < w:
                yield rr, cc


def _accepted_edges(
    gated_edges: list[GatedJumpEdge],
    accepted_decision: str,
) -> list[GatedJumpEdge]:
    return [item for item in gated_edges if item.decision == accepted_decision]


def _edge_cells(item: GatedJumpEdge) -> tuple[tuple[int, int], tuple[int, int]]:
    edge = item.edge
    return (
        (int(edge.row0), int(edge.col0)),
        (int(edge.row1), int(edge.col1)),
    )


def group_jump_regions(
    gated_edges: list[GatedJumpEdge],
    shape: tuple[int, int],
    accepted_decision: str = "JUMP",
) -> list[JumpRegion]:
    h, w = int(shape[0]), int(shape[1])
    if h <= 0 or w <= 0:
        raise ValueError(f"Expected positive 2D shape, got {shape}")

    accepted = _accepted_edges(gated_edges, accepted_decision)
    if not accepted:
        return []

    edge_mask = np.zeros((h, w), dtype=bool)
    cell_to_edges: dict[tuple[int, int], list[int]] = {}

    for edge_idx, item in enumerate(accepted):
        for row, col in _edge_cells(item):
            if not (0 <= row < h and 0 <= col < w):
                raise ValueError(f"Edge endpoint out of bounds: {(row, col)} for shape={shape}")
            edge_mask[row, col] = True
            cell_to_edges.setdefault((row, col), []).append(edge_idx)

    visited = np.zeros((h, w), dtype=bool)
    components: list[set[tuple[int, int]]] = []

    for start_row, start_col in np.argwhere(edge_mask):
        start = (int(start_row), int(start_col))
        if visited[start]:
            continue

        queue: deque[tuple[int, int]] = deque([start])
        visited[start] = True
        cells: set[tuple[int, int]] = set()

        while queue:
            row, col = queue.popleft()
            cells.add((row, col))

            for rr, cc in _neighbors8(row, col, h, w):
                if edge_mask[rr, cc] and not visited[rr, cc]:
                    visited[rr, cc] = True
                    queue.append((rr, cc))

        components.append(cells)

    regions: list[JumpRegion] = []

    for cells in components:
        edge_indices: set[int] = set()
        for cell in cells:
            edge_indices.update(cell_to_edges.get(cell, []))

        items = [accepted[idx] for idx in sorted(edge_indices)]
        rows = [row for row, _ in cells]
        cols = [col for _, col in cells]
        scores = [float(item.edge.score) for item in items]

        regions.append(
            JumpRegion(
                region_id=len(regions),
                edge_count=len(items),
                bbox_row_min=int(min(rows)),
                bbox_col_min=int(min(cols)),
                bbox_row_max=int(max(rows)),
                bbox_col_max=int(max(cols)),
                mean_score=float(np.mean(scores)),
            )
        )

    regions.sort(key=lambda region: (-region.edge_count, region.region_id))
    for new_id, region in enumerate(regions):
        region.region_id = new_id

    return regions


def make_region_mask(
    gated_edges: list[GatedJumpEdge],
    regions: list[JumpRegion],
    shape: tuple[int, int],
) -> np.ndarray:
    h, w = int(shape[0]), int(shape[1])
    region_mask = np.zeros((h, w), dtype=np.int32)

    accepted = _accepted_edges(gated_edges, "JUMP")
    for region in regions:
        label = int(region.region_id) + 1
        for item in accepted:
            for row, col in _edge_cells(item):
                in_bbox = (
                    region.bbox_row_min <= row <= region.bbox_row_max
                    and region.bbox_col_min <= col <= region.bbox_col_max
                )
                if in_bbox:
                    region_mask[row, col] = label

    return region_mask


def save_region_report(
    lamina_index: np.ndarray,
    gated_edges: list[GatedJumpEdge],
    regions: list[JumpRegion],
    out_dir: str | Path,
) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    k = np.asarray(lamina_index, dtype=np.int32)
    if k.ndim != 2:
        raise ValueError(f"Expected 2D lamina_index, got shape={k.shape}")

    region_mask = make_region_mask(
        gated_edges=gated_edges,
        regions=regions,
        shape=k.shape,
    )

    report = {
        "method": "vc_segcheck.grouper.save_region_report.v0",
        "shape": list(k.shape),
        "num_regions": len(regions),
        "regions": [asdict(region) for region in regions],
    }

    (out_dir / "regions_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    np.save(out_dir / "region_mask.npy", region_mask)

    fig = plt.figure(figsize=(8, 4))

    ax1 = fig.add_axes([0.07, 0.12, 0.38, 0.78])
    im1 = ax1.imshow(k)
    ax1.set_title("Lamina index")
    fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

    ax2 = fig.add_axes([0.56, 0.12, 0.38, 0.78])
    im2 = ax2.imshow(region_mask)
    ax2.set_title("Jump regions")
    fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)

    fig.savefig(out_dir / "region_overlay.png", dpi=140)
    plt.close(fig)

    return report
