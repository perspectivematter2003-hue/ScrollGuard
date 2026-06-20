from pathlib import Path
import json
import numpy as np

quality_cache_dir = Path("data_cache/quality/gate_a_tiny_crop")
quality_out_dir = Path("outputs/quality/gate_a_tiny_crop")

required_arrays = [
    quality_cache_dir / "quality_map.npy",
    quality_cache_dir / "risk_map.npy",
    quality_cache_dir / "smoothness_score.npy",
    quality_cache_dir / "stability_score.npy",
    quality_cache_dir / "texture_score.npy",
]

required_outputs = [
    quality_out_dir / "quality_map.png",
    quality_out_dir / "risk_map.png",
    quality_out_dir / "smoothness_score.png",
    quality_out_dir / "stability_score.png",
    quality_out_dir / "texture_score.png",
    quality_out_dir / "quality_summary.json",
]

missing = [str(p) for p in required_arrays + required_outputs if not p.exists()]
if missing:
    raise FileNotFoundError("Missing Month 4 files:\n" + "\n".join(missing))

arrays = {p.stem: np.load(p) for p in required_arrays}

base_shape = arrays["quality_map"].shape
for name, arr in arrays.items():
    assert arr.shape == base_shape, f"{name} shape mismatch"
    assert np.isfinite(arr).all(), f"{name} has NaN or infinity"
    assert arr.min() >= 0.0, f"{name} has values below 0"
    assert arr.max() <= 1.0, f"{name} has values above 1"

combined = arrays["quality_map"] + arrays["risk_map"]
assert np.allclose(combined, 1.0, atol=1e-5), "quality_map + risk_map must equal 1"

summary = json.loads((quality_out_dir / "quality_summary.json").read_text())

print("OK Month 4 smoke test passed")
print(f"quality_shape={base_shape}")
print(f"quality_mean={summary['quality_mean']}")
print(f"risk_mean={summary['risk_mean']}")
print(f"method={summary['method']}")
print("No Vesuvius server access used in this test.")
