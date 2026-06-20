from pathlib import Path
import json
import numpy as np

required_files = [
    Path("outputs/hello_scroll.png"),
    Path("outputs/gate_a_crop_metadata.json"),
    Path("outputs/cached_tiny_crop_metadata.json"),
    Path("outputs/metadata_index.csv"),
    Path("outputs/metadata_index.jsonl"),
    Path("outputs/cached_tiny_crop_preview.png"),
    Path("data_cache/crops/Scroll1_z1000_y3520_3584_x4256_4320.npy"),
]

missing = [str(p) for p in required_files if not p.exists()]
if missing:
    raise FileNotFoundError("Missing files:\n" + "\n".join(missing))

crop = np.load("data_cache/crops/Scroll1_z1000_y3520_3584_x4256_4320.npy")
metadata = json.loads(Path("outputs/cached_tiny_crop_metadata.json").read_text())

assert tuple(crop.shape) == tuple(metadata["shape"]), "Crop shape does not match metadata"
assert str(crop.dtype) == metadata["dtype"], "Crop dtype does not match metadata"

print("OK Month 2 smoke test passed")
print(f"crop_shape={crop.shape}")
print(f"crop_dtype={crop.dtype}")
print(f"metadata_scan_id={metadata['scan_id']}")
print("No Vesuvius server access used in this test.")
