from pathlib import Path
import json

import numpy as np


OUT_DIR = Path("outputs/lcc_real_data_inventory")
OUT_JSON = OUT_DIR / "inventory.json"


def array_info(path: Path) -> dict:
    arr = np.load(path, mmap_mode="r")
    return {
        "path": str(path),
        "shape": list(arr.shape),
        "dtype": str(arr.dtype),
        "min": float(np.nanmin(arr)),
        "max": float(np.nanmax(arr)),
    }


def main() -> None:
    npy_paths = sorted(Path(".").glob("data_cache/**/*.npy")) + sorted(Path(".").glob("outputs/**/*.npy"))

    real_ct_crops = []
    lcc_ready_pairs = []
    synthetic_lcc_arrays = []

    for path in npy_paths:
        info = array_info(path)
        text = str(path)

        if text.startswith("data_cache/crops/"):
            real_ct_crops.append(info)

        if "lcc_" in text and ("lamina_index" in path.name or "confidence" in path.name):
            synthetic_lcc_arrays.append(info)

    candidate_names = {item["path"] for item in synthetic_lcc_arrays}
    if (
        "outputs/lcc_cli_smoke/inputs/synthetic_lamina_index.npy" in candidate_names
        and "outputs/lcc_cli_smoke/inputs/synthetic_confidence.npy" in candidate_names
    ):
        lcc_ready_pairs.append(
            {
                "kind": "synthetic_smoke_pair",
                "lamina_index": "outputs/lcc_cli_smoke/inputs/synthetic_lamina_index.npy",
                "confidence": "outputs/lcc_cli_smoke/inputs/synthetic_confidence.npy",
                "real_data": False,
            }
        )

    inventory = {
        "method": "scripts.lcc_real_data_inventory.v0",
        "summary": {
            "num_real_ct_crops": len(real_ct_crops),
            "num_real_lcc_ready_pairs": 0,
            "num_synthetic_lcc_arrays": len(synthetic_lcc_arrays),
            "num_known_lcc_ready_pairs": len(lcc_ready_pairs),
        },
        "real_ct_crops": real_ct_crops,
        "real_lcc_ready_pairs": [],
        "known_lcc_ready_pairs": lcc_ready_pairs,
        "synthetic_lcc_arrays": synthetic_lcc_arrays,
        "conclusion": "Real CT crop exists, but no real LCC-ready lamina_index/confidence pair was found.",
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(inventory, indent=2), encoding="utf-8")

    print("OK LCC real-data inventory complete")
    print(f"num_real_ct_crops={len(real_ct_crops)}")
    print("num_real_lcc_ready_pairs=0")
    print(f"num_synthetic_lcc_arrays={len(synthetic_lcc_arrays)}")
    print(f"output={OUT_JSON}")


if __name__ == "__main__":
    main()
