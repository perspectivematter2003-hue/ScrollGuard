from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json

import numpy as np

from vc_segcheck.discontinuity import JumpEdge


@dataclass
class GatedJumpEdge:
    edge: JumpEdge
    decision: str
    reason: str
    local_confidence: float


def gate_jump_edges(
    edges: list[JumpEdge],
    confidence: np.ndarray,
    min_confidence: float = 0.5,
) -> list[GatedJumpEdge]:
    conf = np.asarray(confidence, dtype=np.float32)

    gated: list[GatedJumpEdge] = []

    for edge in edges:
        c0 = float(conf[edge.row0, edge.col0])
        c1 = float(conf[edge.row1, edge.col1])
        local_conf = min(c0, c1)

        if local_conf < min_confidence:
            gated.append(
                GatedJumpEdge(
                    edge=edge,
                    decision="ABSTAIN",
                    reason="low_confidence",
                    local_confidence=local_conf,
                )
            )
        else:
            gated.append(
                GatedJumpEdge(
                    edge=edge,
                    decision="JUMP",
                    reason="passed_confidence_gate",
                    local_confidence=local_conf,
                )
            )

    return gated


def save_gate_report(gated_edges: list[GatedJumpEdge], out_dir: str | Path) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    decision_counts: dict[str, int] = {}
    reason_counts: dict[str, int] = {}

    for item in gated_edges:
        decision_counts[item.decision] = decision_counts.get(item.decision, 0) + 1
        reason_counts[item.reason] = reason_counts.get(item.reason, 0) + 1

    report = {
        "method": "vc_segcheck.gate.save_gate_report.v0",
        "num_edges": len(gated_edges),
        "decision_counts": decision_counts,
        "reason_counts": reason_counts,
        "gated_edges": [asdict(item) for item in gated_edges],
    }

    (out_dir / "gate_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
