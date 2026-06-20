from scrollguard.data_access import CropRequest, build_metadata, save_metadata
from scrollguard.cache import load_or_create_crop_cache

request = CropRequest(
    scan_id="Scroll1",
    z=1000,
    y0=3520,
    y1=3584,
    x0=4256,
    x1=4320,
)

crop = load_or_create_crop_cache(request)
metadata = build_metadata(request, crop)
save_metadata(metadata, "outputs/cached_tiny_crop_metadata.json")

print("OK cache test complete")
print(metadata)
