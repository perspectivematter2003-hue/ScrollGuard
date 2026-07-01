from pathlib import Path
import json
import csv

import numpy as np

from vc_segcheck.discontinuity import detect_lamina_discontinuities
from vc_segcheck.gate import gate_jump_edges
from vc_segcheck.grouper import group_jump_regions, save_region_report
from vc_segcheck.reporting import save_lcc_review_package

OUT = Path("outputs/lcc_reporting_smoke")


def main() -> None:
    h, w = 64, 64

    jump = np.zeros((h, w), dtype=np.int32)
    jump[24:40, 24:40] = 1

    confidence = np.ones((h, w), dtype=np.float32)

    edges = detect_lamina_discontinuities(
        lamina_index=jump,
        confidence=confidence,
        min_abs_delta_k=1,
        min_confidence=0.0,
    )

    gated = gate_jump_edges(
        edges=edges,
        confidence=confidence,
        min_confidence=0.5,
    )

    regions = group_jump_regions(
        gated_edges=gated,
        shape=jump.shape,
    )

    if len(edges) != 64:
        raise RuntimeError(f"Expected 64 jump edges, got {len(edges)}")

    if len(regions) != 1:
        raise RuntimeError(f"Expected 1 region, got {len(regions)}")

    region_report = save_region_report(
        lamina_index=jump,
        gated_edges=gated,
        regions=regions,
        out_dir=OUT / "regions",
    )

    package = save_lcc_review_package(
        regions=regions,
        shape=jump.shape,
        out_dir=OUT,
        run_metadata={
            "smoke_test": "lcc_reporting_smoke_test",
            "source": "synthetic_64x64_lamina_jump_patch",
        },
        input_artifacts={
            "regions_report_json": str(OUT / "regions" / "regions_report.json"),
            "region_overlay_png": str(OUT / "regions" / "region_overlay.png"),
        },
    )

    report = package["report"]
    evidence = package["evidence"]

    if report["summary"]["num_regions"] != 1:
        raise RuntimeError(f"Expected report num_regions=1, got {report['summary']}")

    if report["summary"]["total_region_edges"] != 64:
        raise RuntimeError(f"Expected total_region_edges=64, got {report['summary']}")

    first_region = report["regions"][0]
    if first_region["edge_count"] != 64:
        raise RuntimeError(f"Expected first region edge_count=64, got {first_region}")

    if first_region["review_reason"] != "lamina_continuity_jump_region":
        raise RuntimeError(f"Unexpected review reason: {first_region}")

    if evidence["reviewable_region_count"] != 1:
        raise RuntimeError(f"Expected evidence reviewable_region_count=1, got {evidence}")

    csv_path = OUT / "review_regions.csv"
    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    if len(rows) != 1:
        raise RuntimeError(f"Expected 1 CSV row, got {len(rows)}")

    summary = {
        "method": "scripts.lcc_reporting_smoke_test.v0",
        "shape": [h, w],
        "num_edges": len(edges),
        "num_regions": len(regions),
        "region_report_num_regions": region_report["num_regions"],
        "report_summary": report["summary"],
        "first_review_row": rows[0],
        "outputs": package["outputs"],
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("OK LCC reporting smoke test passed")
    print(f"num_edges={len(edges)}")
    print(f"num_regions={len(regions)}")
    print(f"report_summary={report['summary']}")
    print(f"review_csv_rows={len(rows)}")
    print(f"out_dir={OUT}")


if __name__ == "__main__":
    main()
