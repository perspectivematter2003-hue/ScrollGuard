#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    manifest = [
        {
            "name": "candidate_large_crop_cache_guard_test",
            "scan_id": "Scroll1",
            "z": 1000,
            "y0": 3520,
            "y1": 3776,
            "x0": 4256,
            "x1": 4512,
        }
    ]

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(manifest, f, indent=2)
        tmp_path = Path(f.name)

    try:
        result = subprocess.run(
            [sys.executable, "scripts/manifest_cache_check.py", str(tmp_path)],
            text=True,
            capture_output=True,
        )

        combined = result.stdout + result.stderr

        if result.returncode == 0:
            print(combined)
            raise SystemExit("ERROR missing crop manifest unexpectedly passed")

        if "Cache-only mode refuses server access" not in combined:
            print(combined)
            raise SystemExit("ERROR missing crop failure did not explain cache-only refusal")

        print("OK manifest missing-cache smoke test passed")
        print("Missing manifest crop was blocked before any server access.")
        print("No Vesuvius server access used.")
    finally:
        tmp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
