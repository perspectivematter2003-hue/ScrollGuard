from __future__ import annotations

from pathlib import Path
import json
from typing import Any

import numpy as np

from vc_segcheck.discontinuity import detect_lamina_discontinuities, save_discontinuity_report
from vc_segcheck.gate import gate_jump_edges, save_gate_report
from vc_segcheck.grouper import group_jump_regions, save_region_report
from vc_segcheck.reporting import save_lcc_review_package


def run_lcc_pipeline(
    lamina_index: np.ndarray,
    confidence: np.ndarray,
    out_dir: str | Path,
    min_abs_delta_k: int = 1,
    min_detection_confidence: float = 0.0,
    min_gate_confidence: float = 0.5,
    run_metadata: dict[str, Any] | None = None,
) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    k = np.asarray(lamina_index, dtype=np.int32)
    conf = np.asarray(confidence, dtype=np.float32)

    if k.ndim != 2:
        raise ValueError(f"Expected 2D lamina_index, got shape={k.shape}")

    if conf.shape != k.shape:
        raise ValueError(f"confidence shape mismatch: {conf.shape} vs {k.shape}")

    edges = detect_lamina_discontinuities(
        lamina_index=k,
        confidence=conf,
        min_abs_delta_k=min_abs_delta_k,
        min_confidence=min_detection_confidence,
    )

    discontinuity_report = save_discontinuity_report(
        lamina_index=k,
        confidence=conf,
        edges=edges,
        out_dir=out_dir / "discontinuity",
    )

    gated_edges = gate_jump_edges(
        edges=edges,
        confidence=conf,
        min_confidence=min_gate_confidence,
    )

    gate_report = save_gate_report(
        gated_edges=gated_edges,
        out_dir=out_dir / "gate",
    )

    regions = group_jump_regions(
        gated_edges=gated_edges,
        shape=k.shape,
    )

    region_report = save_region_report(
        lamina_index=k,
        gated_edges=gated_edges,
        regions=regions,
        out_dir=out_dir / "regions",
    )

    review_package = save_lcc_review_package(
        regions=regions,
        shape=k.shape,
        out_dir=out_dir / "review_package",
        run_metadata=run_metadata or {},
        input_artifacts={
            "discontinuity_report_json": str(out_dir / "discontinuity" / "discontinuity_report.json"),
            "gate_report_json": str(out_dir / "gate" / "gate_report.json"),
            "regions_report_json": str(out_dir / "regions" / "regions_report.json"),
            "region_overlay_png": str(out_dir / "regions" / "region_overlay.png"),
        },
    )

    accepted_edges = sum(1 for item in gated_edges if item.decision == "JUMP")
    abstained_edges = sum(1 for item in gated_edges if item.decision == "ABSTAIN")

    summary = {
        "method": "vc_segcheck.pipeline.run_lcc_pipeline.v0",
        "shape": list(k.shape),
        "parameters": {
            "min_abs_delta_k": int(min_abs_delta_k),
            "min_detection_confidence": float(min_detection_confidence),
            "min_gate_confidence": float(min_gate_confidence),
        },
        "counts": {
            "num_jump_edges": len(edges),
            "num_accepted_edges": int(accepted_edges),
            "num_abstained_edges": int(abstained_edges),
            "num_regions": len(regions),
        },
        "reports": {
            "discontinuity": discontinuity_report,
            "gate": {
                "num_edges": gate_report["num_edges"],
                "decision_counts": gate_report["decision_counts"],
                "reason_counts": gate_report["reason_counts"],
            },
            "regions": region_report,
            "review_package_summary": review_package["report"]["summary"],
        },
        "outputs": {
            "discontinuity_dir": str(out_dir / "discontinuity"),
            "gate_dir": str(out_dir / "gate"),
            "regions_dir": str(out_dir / "regions"),
            "review_package_dir": str(out_dir / "review_package"),
            "summary_json": str(out_dir / "summary.json"),
        },
    }

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    return summary
