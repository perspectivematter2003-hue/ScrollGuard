from pathlib import Path
import json

import numpy as np

from vc_segcheck.pipeline import run_lcc_pipeline

OUT = Path("outputs/lcc_pipeline_smoke")


def main() -> None:
    h, w = 64, 64

    jump = np.zeros((h, w), dtype=np.int32)
    jump[24:40, 24:40] = 1

    confidence = np.ones((h, w), dtype=np.float32)

    summary = run_lcc_pipeline(
        lamina_index=jump,
        confidence=confidence,
        out_dir=OUT,
        min_abs_delta_k=1,
        min_detection_confidence=0.0,
        min_gate_confidence=0.5,
        run_metadata={
            "smoke_test": "lcc_pipeline_smoke_test",
            "source": "synthetic_64x64_lamina_jump_patch",
        },
    )

    counts = summary["counts"]

    if counts["num_jump_edges"] != 64:
        raise RuntimeError(f"Expected 64 jump edges, got {counts}")

    if counts["num_accepted_edges"] != 64:
        raise RuntimeError(f"Expected 64 accepted edges, got {counts}")

    if counts["num_abstained_edges"] != 0:
        raise RuntimeError(f"Expected 0 abstained edges, got {counts}")

    if counts["num_regions"] != 1:
        raise RuntimeError(f"Expected 1 region, got {counts}")

    review_summary = summary["reports"]["review_package_summary"]
    if review_summary["num_regions"] != 1:
        raise RuntimeError(f"Expected review package num_regions=1, got {review_summary}")

    if review_summary["total_region_edges"] != 64:
        raise RuntimeError(f"Expected total_region_edges=64, got {review_summary}")

    required_outputs = [
        OUT / "summary.json",
        OUT / "discontinuity" / "discontinuity_report.json",
        OUT / "gate" / "gate_report.json",
        OUT / "regions" / "regions_report.json",
        OUT / "regions" / "region_overlay.png",
        OUT / "review_package" / "report.json",
        OUT / "review_package" / "review_regions.csv",
        OUT / "review_package" / "evidence.json",
    ]

    missing = [str(path) for path in required_outputs if not path.exists()]
    if missing:
        raise RuntimeError(f"Missing expected outputs: {missing}")

    smoke_summary = {
        "method": "scripts.lcc_pipeline_smoke_test.v0",
        "pipeline_summary": summary,
        "required_outputs": [str(path) for path in required_outputs],
    }
    (OUT / "smoke_summary.json").write_text(json.dumps(smoke_summary, indent=2), encoding="utf-8")

    print("OK LCC pipeline smoke test passed")
    print(f"counts={counts}")
    print(f"review_summary={review_summary}")
    print(f"out_dir={OUT}")


if __name__ == "__main__":
    main()
