from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np


def run_bad_cli_case(
    case_name: str,
    lamina: np.ndarray,
    confidence: np.ndarray,
    expected_error: str,
) -> None:
    with tempfile.TemporaryDirectory(prefix=f"vc_segcheck_{case_name}_") as tmp:
        tmp_path = Path(tmp)
        lamina_path = tmp_path / "lamina.npy"
        confidence_path = tmp_path / "confidence.npy"
        out_dir = tmp_path / "out"

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
            str(out_dir),
        ]

        result = subprocess.run(
            cmd,
            check=False,
            text=True,
            capture_output=True,
        )

        combined_output = result.stdout + result.stderr

        if result.returncode == 0:
            raise RuntimeError(f"{case_name}: expected CLI failure, got success")

        if expected_error not in combined_output:
            raise RuntimeError(
                f"{case_name}: expected error text not found: {expected_error!r}\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            )

        print(f"OK bad-input case failed safely: {case_name}")
        print(f"returncode={result.returncode}")
        print(f"matched_error={expected_error}")


def main() -> None:
    run_bad_cli_case(
        case_name="shape_mismatch",
        lamina=np.zeros((8, 8), dtype=np.int32),
        confidence=np.ones((8, 7), dtype=np.float32),
        expected_error="confidence shape mismatch",
    )

    run_bad_cli_case(
        case_name="non_2d_lamina",
        lamina=np.zeros((2, 8, 8), dtype=np.int32),
        confidence=np.ones((2, 8, 8), dtype=np.float32),
        expected_error="Expected 2D lamina_index",
    )

    print("OK LCC CLI validation smoke test passed")


if __name__ == "__main__":
    main()
