from pathlib import Path
import json
import numpy as np

feature_dir = Path("data_cache/features/gate_a_tiny_crop")
preview_dir = Path("outputs/features/gate_a_tiny_crop")

required_arrays = [
    feature_dir / "normalized.npy",
    feature_dir / "gradient_x.npy",
    feature_dir / "gradient_y.npy",
    feature_dir / "gradient_magnitude.npy",
    feature_dir / "local_mean.npy",
    feature_dir / "local_std.npy",
]

required_outputs = [
    preview_dir / "normalized.png",
    preview_dir / "gradient_magnitude.png",
    preview_dir / "local_std.png",
    preview_dir / "feature_summary.json",
]

missing = [str(p) for p in required_arrays + required_outputs if not p.exists()]
if missing:
    raise FileNotFoundError("Missing Month 3 files:\n" + "\n".join(missing))

arrays = {p.stem: np.load(p) for p in required_arrays}

base_shape = arrays["normalized"].shape
for name, arr in arrays.items():
    assert arr.shape == base_shape, f"{name} shape mismatch: {arr.shape} != {base_shape}"
    assert np.isfinite(arr).all(), f"{name} contains NaN or infinity"

summary = json.loads((preview_dir / "feature_summary.json").read_text())

print("OK Month 3 smoke test passed")
print(f"feature_shape={base_shape}")
print(f"summary_method={summary['method']}")
print(f"gradient_mean={summary['gradient_mean']}")
print(f"local_std_mean={summary['local_std_mean']}")
print("No Vesuvius server access used in this test.")
