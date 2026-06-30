from pathlib import Path
import json

import numpy as np

from vc_segcheck.lamina import assign_lamina_index_field, save_lamina_field_report

OUT_CLEAN = Path("outputs/lcc_lamina_smoke/clean")
OUT_JUMP = Path("outputs/lcc_lamina_smoke/jump")


def main() -> None:
    h, w = 64, 64
    spacing = 6.0

    clean_coord = np.zeros((h, w), dtype=np.float32)
    clean_conf = np.ones((h, w), dtype=np.float32)

    clean_field = assign_lamina_index_field(
        lamina_coord=clean_coord,
        spacing_voxels=spacing,
        reference_coord=0.0,
        confidence=clean_conf,
    )
    clean_report = save_lamina_field_report(clean_field, OUT_CLEAN)

    if clean_report["index_histogram"] != {"0": h * w}:
        raise RuntimeError(f"Clean field should be all k=0, got {clean_report['index_histogram']}")

    jump_coord = clean_coord.copy()
    jump_coord[24:40, 24:40] += spacing

    jump_field = assign_lamina_index_field(
        lamina_coord=jump_coord,
        spacing_voxels=spacing,
        reference_coord=0.0,
        confidence=clean_conf,
    )
    jump_report = save_lamina_field_report(jump_field, OUT_JUMP)

    expected_jump_pixels = 16 * 16
    hist = jump_report["index_histogram"]

    if hist.get("1") != expected_jump_pixels:
        raise RuntimeError(f"Expected {expected_jump_pixels} k=1 pixels, got {hist}")

    if hist.get("0") != (h * w - expected_jump_pixels):
        raise RuntimeError(f"Expected remaining pixels k=0, got {hist}")

    summary = {
        "method": "scripts.lcc_lamina_smoke_test.v0",
        "spacing_voxels": spacing,
        "clean_histogram": clean_report["index_histogram"],
        "jump_histogram": jump_report["index_histogram"],
        "expected_jump_pixels": expected_jump_pixels,
    }
    out = Path("outputs/lcc_lamina_smoke")
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("OK LCC lamina-index smoke test passed")
    print(f"spacing_voxels={spacing}")
    print(f"clean_histogram={clean_report['index_histogram']}")
    print(f"jump_histogram={jump_report['index_histogram']}")
    print(f"out_dir={out}")


if __name__ == "__main__":
    main()
