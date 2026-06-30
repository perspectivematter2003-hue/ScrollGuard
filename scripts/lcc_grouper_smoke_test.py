from pathlib import Path
import json

import numpy as np

from vc_segcheck.discontinuity import detect_lamina_discontinuities
from vc_segcheck.gate import gate_jump_edges
from vc_segcheck.grouper import group_jump_regions, save_region_report

OUT = Path("outputs/lcc_grouper_smoke")


def main() -> None:
    h, w = 64, 64

    clean = np.zeros((h, w), dtype=np.int32)
    confidence = np.ones((h, w), dtype=np.float32)

    clean_edges = detect_lamina_discontinuities(
        lamina_index=clean,
        confidence=confidence,
        min_abs_delta_k=1,
        min_confidence=0.0,
    )
    clean_gated = gate_jump_edges(
        edges=clean_edges,
        confidence=confidence,
        min_confidence=0.5,
    )
    clean_regions = group_jump_regions(
        gated_edges=clean_gated,
        shape=clean.shape,
    )

    if len(clean_regions) != 0:
        raise RuntimeError(f"Expected 0 clean regions, got {len(clean_regions)}")

    jump = np.zeros((h, w), dtype=np.int32)
    jump[24:40, 24:40] = 1

    jump_edges = detect_lamina_discontinuities(
        lamina_index=jump,
        confidence=confidence,
        min_abs_delta_k=1,
        min_confidence=0.0,
    )
    jump_gated = gate_jump_edges(
        edges=jump_edges,
        confidence=confidence,
        min_confidence=0.5,
    )
    jump_regions = group_jump_regions(
        gated_edges=jump_gated,
        shape=jump.shape,
    )

    if len(jump_edges) != 64:
        raise RuntimeError(f"Expected 64 jump edges, got {len(jump_edges)}")

    accepted_count = sum(1 for item in jump_gated if item.decision == "JUMP")
    if accepted_count != 64:
        raise RuntimeError(f"Expected 64 accepted jump edges, got {accepted_count}")

    if len(jump_regions) != 1:
        raise RuntimeError(f"Expected 1 jump region, got {len(jump_regions)}")

    region = jump_regions[0]
    if region.edge_count != 64:
        raise RuntimeError(f"Expected region edge_count=64, got {region.edge_count}")

    if not (22 <= region.bbox_row_min <= 24 and 39 <= region.bbox_row_max <= 41):
        raise RuntimeError(f"Unexpected region row bbox: {region}")

    if not (22 <= region.bbox_col_min <= 24 and 39 <= region.bbox_col_max <= 41):
        raise RuntimeError(f"Unexpected region col bbox: {region}")

    report = save_region_report(
        lamina_index=jump,
        gated_edges=jump_gated,
        regions=jump_regions,
        out_dir=OUT,
    )

    summary = {
        "method": "scripts.lcc_grouper_smoke_test.v0",
        "shape": [h, w],
        "clean_num_edges": len(clean_edges),
        "clean_num_regions": len(clean_regions),
        "jump_num_edges": len(jump_edges),
        "jump_accepted_edges": accepted_count,
        "jump_num_regions": len(jump_regions),
        "jump_region": report["regions"][0],
        "outputs": {
            "regions_report": str(OUT / "regions_report.json"),
            "region_overlay": str(OUT / "region_overlay.png"),
            "summary": str(OUT / "summary.json"),
        },
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("OK LCC grouper smoke test passed")
    print(f"clean_regions={len(clean_regions)}")
    print(f"jump_edges={len(jump_edges)}")
    print(f"jump_regions={len(jump_regions)}")
    print(f"region_edge_count={region.edge_count}")
    print(
        "region_bbox="
        f"({region.bbox_row_min}, {region.bbox_col_min}, "
        f"{region.bbox_row_max}, {region.bbox_col_max})"
    )
    print(f"out_dir={OUT}")


if __name__ == "__main__":
    main()
