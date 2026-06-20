from pathlib import Path
import numpy as np

from scrollguard.data_access import CropRequest, read_crop


def crop_cache_name(request: CropRequest) -> str:
    return (
        f"{request.scan_id}_z{request.z}"
        f"_y{request.y0}_{request.y1}"
        f"_x{request.x0}_{request.x1}.npy"
    )


def load_or_create_crop_cache(request: CropRequest, cache_dir: str | Path = "data_cache/crops") -> np.ndarray:
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    cache_path = cache_dir / crop_cache_name(request)

    if cache_path.exists():
        print(f"OK loaded cached crop: {cache_path}")
        return np.load(cache_path)

    crop = read_crop(request)
    np.save(cache_path, crop)
    print(f"OK saved crop cache: {cache_path}")
    return crop
