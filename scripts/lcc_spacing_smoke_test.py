from pathlib import Path
import json
import subprocess
import sys

from vc_segcheck.spacing import estimate_spacing_from_profiles_json

PROFILE_JSON = Path("profiles/lcc_normal_profile_smoke/normal_profiles.json")
OUT = Path("outputs/lcc_spacing_smoke")


def main() -> None:
    if not PROFILE_JSON.exists():
        subprocess.run(
            [sys.executable, "scripts/lcc_normal_profile_smoke_test.py"],
            check=True,
            env={"PYTHONPATH": "src"},
        )

    estimates = estimate_spacing_from_profiles_json(
        profiles_json=PROFILE_JSON,
        out_dir=OUT,
        min_lag=2,
        max_lag=15,
    )

    report = json.loads((OUT / "spacing_report.json").read_text(encoding="utf-8"))

    median_spacing = report["median_spacing_voxels"]
    num_valid = report["num_valid"]

    if num_valid < 20:
        raise RuntimeError(f"Too few valid spacing estimates: {num_valid}")

    if not (5.0 <= float(median_spacing) <= 7.5):
        raise RuntimeError(f"Unexpected median spacing: {median_spacing}")

    print("OK LCC spacing smoke test passed")
    print(f"profiles={len(estimates)}")
    print(f"valid={num_valid}")
    print(f"median_spacing_voxels={median_spacing}")
    print(f"mean_confidence={report['mean_confidence']}")
    print(f"out_dir={OUT}")


if __name__ == "__main__":
    main()
