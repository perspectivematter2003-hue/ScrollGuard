from __future__ import annotations

from dataclasses import asdict, is_dataclass
from pathlib import Path
import csv
import json
from datetime import datetime, timezone
from typing import Any


def _to_plain_dict(item: Any) -> dict:
    if is_dataclass(item):
        return asdict(item)
    if isinstance(item, dict):
        return dict(item)
    raise TypeError(f"Expected dataclass or dict region, got {type(item)!r}")


def _region_row(region: dict) -> dict:
    row_min = int(region["bbox_row_min"])
    col_min = int(region["bbox_col_min"])
    row_max = int(region["bbox_row_max"])
    col_max = int(region["bbox_col_max"])

    return {
        "region_id": int(region["region_id"]),
        "edge_count": int(region["edge_count"]),
        "bbox_row_min": row_min,
        "bbox_col_min": col_min,
        "bbox_row_max": row_max,
        "bbox_col_max": col_max,
        "bbox_height": int(row_max - row_min + 1),
        "bbox_width": int(col_max - col_min + 1),
        "mean_score": float(region["mean_score"]),
        "review_priority": int(region["edge_count"]),
        "review_reason": "lamina_continuity_jump_region",
    }


def build_lcc_report(
    regions: list[Any],
    shape: tuple[int, int] | list[int],
    run_metadata: dict | None = None,
) -> dict:
    plain_regions = [_region_row(_to_plain_dict(region)) for region in regions]
    plain_regions.sort(key=lambda item: (-item["review_priority"], item["region_id"]))

    total_edges = sum(int(region["edge_count"]) for region in plain_regions)
    max_edges = max((int(region["edge_count"]) for region in plain_regions), default=0)
    mean_score = (
        sum(float(region["mean_score"]) for region in plain_regions) / len(plain_regions)
        if plain_regions
        else 0.0
    )

    return {
        "method": "vc_segcheck.reporting.build_lcc_report.v0",
        "schema_version": 1,
        "shape": [int(shape[0]), int(shape[1])],
        "run_metadata": run_metadata or {},
        "summary": {
            "num_regions": len(plain_regions),
            "total_region_edges": int(total_edges),
            "max_region_edge_count": int(max_edges),
            "mean_region_score": float(mean_score),
        },
        "regions": plain_regions,
    }


def build_evidence_bundle(
    report: dict,
    input_artifacts: dict | None = None,
    output_artifacts: dict | None = None,
) -> dict:
    return {
        "method": "vc_segcheck.reporting.build_evidence_bundle.v0",
        "schema_version": 1,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim": "LCC flags connected regions where a segmentation crosses lamina index boundaries.",
        "non_claims": [
            "does_not_claim_ink",
            "does_not_claim_letters",
            "does_not_claim_text",
            "does_not_claim_vc3d_export",
        ],
        "input_artifacts": input_artifacts or {},
        "output_artifacts": output_artifacts or {},
        "report_summary": report["summary"],
        "reviewable_region_count": int(report["summary"]["num_regions"]),
    }


def save_lcc_review_package(
    regions: list[Any],
    shape: tuple[int, int] | list[int],
    out_dir: str | Path,
    run_metadata: dict | None = None,
    input_artifacts: dict | None = None,
) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    report = build_lcc_report(
        regions=regions,
        shape=shape,
        run_metadata=run_metadata,
    )

    report_path = out_dir / "report.json"
    csv_path = out_dir / "review_regions.csv"
    evidence_path = out_dir / "evidence.json"

    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    fieldnames = [
        "region_id",
        "edge_count",
        "bbox_row_min",
        "bbox_col_min",
        "bbox_row_max",
        "bbox_col_max",
        "bbox_height",
        "bbox_width",
        "mean_score",
        "review_priority",
        "review_reason",
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for region in report["regions"]:
            writer.writerow(region)

    output_artifacts = {
        "report_json": str(report_path),
        "review_regions_csv": str(csv_path),
        "evidence_json": str(evidence_path),
    }

    evidence = build_evidence_bundle(
        report=report,
        input_artifacts=input_artifacts,
        output_artifacts=output_artifacts,
    )
    evidence_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")

    return {
        "method": "vc_segcheck.reporting.save_lcc_review_package.v0",
        "out_dir": str(out_dir),
        "report": report,
        "evidence": evidence,
        "outputs": output_artifacts,
    }
