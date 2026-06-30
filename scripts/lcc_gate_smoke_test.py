from pathlib import Path
import json

import numpy as np

from vc_segcheck.discontinuity import detect_lamina_discontinuities
from vc_segcheck.gate import gate_jump_edges, save_gate_report

OUT = Path("outputs/lcc_gate_smoke")


def main() -> None:
    h, w = 64, 64

    jump = np.zeros((h, w), dtype=np.int32)
    jump[24:40, 24:40] = 1

    high_conf = np.ones((h, w), dtype=np.float32)
    edges = detect_lamina_discontinuities(
        lamina_index=jump,
        confidence=high_conf,
        min_abs_delta_k=1,
        min_confidence=0.0,
    )

    gated_high = gate_jump_edges(
        edges=edges,
        confidence=high_conf,
        min_confidence=0.5,
    )
    high_report = save_gate_report(gated_high, OUT / "high_confidence")

    if high_report["decision_counts"].get("JUMP") != 64:
        raise RuntimeError(f"Expected 64 accepted jumps, got {high_report['decision_counts']}")

    low_conf = np.ones((h, w), dtype=np.float32)
    low_conf[23:41, 23:41] = 0.1

    gated_low = gate_jump_edges(
        edges=edges,
        confidence=low_conf,
        min_confidence=0.5,
    )
    low_report = save_gate_report(gated_low, OUT / "low_confidence")

    if low_report["decision_counts"].get("ABSTAIN") != 64:
        raise RuntimeError(f"Expected 64 abstains, got {low_report['decision_counts']}")

    summary = {
        "method": "scripts.lcc_gate_smoke_test.v0",
        "num_edges": len(edges),
        "high_confidence_decisions": high_report["decision_counts"],
        "low_confidence_decisions": low_report["decision_counts"],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("OK LCC gate smoke test passed")
    print(f"edges={len(edges)}")
    print(f"high_confidence_decisions={high_report['decision_counts']}")
    print(f"low_confidence_decisions={low_report['decision_counts']}")
    print(f"out_dir={OUT}")


if __name__ == "__main__":
    main()
