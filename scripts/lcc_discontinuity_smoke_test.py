from pathlib import Path
import json

import numpy as np

from vc_segcheck.discontinuity import detect_lamina_discontinuities, save_discontinuity_report

OUT = Path("outputs/lcc_discontinuity_smoke")


def main() -> None:
    h, w = 64, 64
    confidence = np.ones((h, w), dtype=np.float32)

    clean = np.zeros((h, w), dtype=np.int32)
    clean_edges = detect_lamina_discontinuities(
        lamina_index=clean,
        confidence=confidence,
        min_abs_delta_k=1,
        min_confidence=0.5,
    )
    clean_report = save_discontinuity_report(
        lamina_index=clean,
        confidence=confidence,
        edges=clean_edges,
        out_dir=OUT / "clean",
    )

    if clean_report["num_jump_edges"] != 0:
        raise RuntimeError(f"Clean field should have 0 jump edges, got {clean_report['num_jump_edges']}")

    jump = clean.copy()
    jump[24:40, 24:40] = 1

    jump_edges = detect_lamina_discontinuities(
        lamina_index=jump,
        confidence=confidence,
        min_abs_delta_k=1,
        min_confidence=0.5,
    )
    jump_report = save_discontinuity_report(
        lamina_index=jump,
        confidence=confidence,
        edges=jump_edges,
        out_dir=OUT / "jump",
    )

    expected_edges = 64
    if jump_report["num_jump_edges"] != expected_edges:
        raise RuntimeError(
            f"Expected {expected_edges} jump boundary edges, got {jump_report['num_jump_edges']}"
        )

    summary = {
        "method": "scripts.lcc_discontinuity_smoke_test.v0",
        "clean_jump_edges": clean_report["num_jump_edges"],
        "jump_edges": jump_report["num_jump_edges"],
        "expected_jump_edges": expected_edges,
        "jump_delta_histogram": jump_report["delta_k_histogram"],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("OK LCC discontinuity smoke test passed")
    print(f"clean_jump_edges={clean_report['num_jump_edges']}")
    print(f"jump_edges={jump_report['num_jump_edges']}")
    print(f"expected_jump_edges={expected_edges}")
    print(f"delta_histogram={jump_report['delta_k_histogram']}")
    print(f"out_dir={OUT}")


if __name__ == "__main__":
    main()
