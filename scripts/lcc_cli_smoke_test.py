from pathlib import Path
import json
import subprocess
import sys

import numpy as np

OUT = Path("outputs/lcc_cli_smoke")
INPUTS = OUT / "inputs"
RUN_OUT = OUT / "cli_run"


def main() -> None:
    h, w = 64, 64

    INPUTS.mkdir(parents=True, exist_ok=True)

    lamina = np.zeros((h, w), dtype=np.int32)
    lamina[24:40, 24:40] = 1

    confidence = np.ones((h, w), dtype=np.float32)

    lamina_path = INPUTS / "synthetic_lamina_index.npy"
    confidence_path = INPUTS / "synthetic_confidence.npy"

    np.save(lamina_path, lamina)
    np.save(confidence_path, confidence)

    cmd = [
        sys.executable,
        "-m",
        "vc_segcheck.cli",
        "lcc",
        "--lamina-index",
        str(lamina_path),
        "--confidence",
        str(confidence_path),
        "--out",
        str(RUN_OUT),
        "--min-abs-delta-k",
        "1",
        "--min-detection-confidence",
        "0.0",
        "--min-gate-confidence",
        "0.5",
    ]

    result = subprocess.run(
        cmd,
        check=True,
        text=True,
        capture_output=True,
    )

    summary_path = RUN_OUT / "summary.json"
    if not summary_path.exists():
        raise RuntimeError(f"Missing CLI summary output: {summary_path}")

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    counts = summary["counts"]

    if counts["num_jump_edges"] != 64:
        raise RuntimeError(f"Expected 64 jump edges, got {counts}")

    if counts["num_accepted_edges"] != 64:
        raise RuntimeError(f"Expected 64 accepted edges, got {counts}")

    if counts["num_abstained_edges"] != 0:
        raise RuntimeError(f"Expected 0 abstained edges, got {counts}")

    if counts["num_regions"] != 1:
        raise RuntimeError(f"Expected 1 region, got {counts}")

    expected_stdout = "OK vc-segcheck LCC pipeline complete"
    if expected_stdout not in result.stdout:
        raise RuntimeError(f"Missing expected CLI stdout. Got:\n{result.stdout}")

    required_outputs = [
        RUN_OUT / "summary.json",
        RUN_OUT / "discontinuity" / "discontinuity_report.json",
        RUN_OUT / "gate" / "gate_report.json",
        RUN_OUT / "regions" / "regions_report.json",
        RUN_OUT / "review_package" / "report.json",
        RUN_OUT / "review_package" / "review_regions.csv",
        RUN_OUT / "review_package" / "evidence.json",
    ]

    missing = [str(path) for path in required_outputs if not path.exists()]
    if missing:
        raise RuntimeError(f"Missing expected CLI outputs: {missing}")

    smoke_summary = {
        "method": "scripts.lcc_cli_smoke_test.v0",
        "command": cmd,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "counts": counts,
        "required_outputs": [str(path) for path in required_outputs],
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(smoke_summary, indent=2), encoding="utf-8")

    print("OK LCC CLI smoke test passed")
    print(f"counts={counts}")
    print(f"out_dir={OUT}")


if __name__ == "__main__":
    main()
