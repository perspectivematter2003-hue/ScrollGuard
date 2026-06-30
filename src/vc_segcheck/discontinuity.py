from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class JumpEdge:
    row0: int
    col0: int
    row1: int
    col1: int
    k0: int
    k1: int
    delta_k: int
    score: float


def detect_lamina_discontinuities(
    lamina_index: np.ndarray,
    confidence: np.ndarray | None = None,
    min_abs_delta_k: int = 1,
    min_confidence: float = 0.5,
) -> list[JumpEdge]:
    k = np.asarray(lamina_index, dtype=np.int32)

    if k.ndim != 2:
        raise ValueError(f"Expected 2D lamina_index, got shape={k.shape}")

    if confidence is None:
        conf = np.ones(k.shape, dtype=np.float32)
    else:
        conf = np.asarray(confidence, dtype=np.float32)
        if conf.shape != k.shape:
            raise ValueError(f"confidence shape mismatch: {conf.shape} vs {k.shape}")

    edges: list[JumpEdge] = []

    h, w = k.shape

    # Horizontal neighbor edges: (r,c) -> (r,c+1)
    for r in range(h):
        for c in range(w - 1):
            local_conf = min(float(conf[r, c]), float(conf[r, c + 1]))
            if local_conf < min_confidence:
                continue

            dk = int(k[r, c + 1] - k[r, c])
            if abs(dk) >= min_abs_delta_k:
                edges.append(
                    JumpEdge(
                        row0=r,
                        col0=c,
                        row1=r,
                        col1=c + 1,
                        k0=int(k[r, c]),
                        k1=int(k[r, c + 1]),
                        delta_k=dk,
                        score=float(abs(dk) * local_conf),
                    )
                )

    # Vertical neighbor edges: (r,c) -> (r+1,c)
    for r in range(h - 1):
        for c in range(w):
            local_conf = min(float(conf[r, c]), float(conf[r + 1, c]))
            if local_conf < min_confidence:
                continue

            dk = int(k[r + 1, c] - k[r, c])
            if abs(dk) >= min_abs_delta_k:
                edges.append(
                    JumpEdge(
                        row0=r,
                        col0=c,
                        row1=r + 1,
                        col1=c,
                        k0=int(k[r, c]),
                        k1=int(k[r + 1, c]),
                        delta_k=dk,
                        score=float(abs(dk) * local_conf),
                    )
                )

    return edges


def save_discontinuity_report(
    lamina_index: np.ndarray,
    confidence: np.ndarray | None,
    edges: list[JumpEdge],
    out_dir: str | Path,
) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    k = np.asarray(lamina_index, dtype=np.int32)

    edge_mask = np.zeros(k.shape, dtype=np.float32)
    for edge in edges:
        edge_mask[edge.row0, edge.col0] = max(edge_mask[edge.row0, edge.col0], edge.score)
        edge_mask[edge.row1, edge.col1] = max(edge_mask[edge.row1, edge.col1], edge.score)

    delta_hist: dict[str, int] = {}
    for edge in edges:
        key = str(int(edge.delta_k))
        delta_hist[key] = delta_hist.get(key, 0) + 1

    report = {
        "method": "vc_segcheck.discontinuity.save_discontinuity_report.v0",
        "shape": list(k.shape),
        "num_jump_edges": len(edges),
        "delta_k_histogram": delta_hist,
        "edges": [asdict(edge) for edge in edges],
    }

    (out_dir / "discontinuity_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    np.save(out_dir / "jump_edge_mask.npy", edge_mask)

    fig = plt.figure(figsize=(8, 4))

    ax1 = fig.add_axes([0.07, 0.12, 0.38, 0.78])
    im1 = ax1.imshow(k)
    ax1.set_title("Lamina index")
    fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

    ax2 = fig.add_axes([0.56, 0.12, 0.38, 0.78])
    im2 = ax2.imshow(edge_mask)
    ax2.set_title("Jump edge score")
    fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)

    fig.savefig(out_dir / "discontinuity_overlay.png", dpi=140)
    plt.close(fig)

    return report
