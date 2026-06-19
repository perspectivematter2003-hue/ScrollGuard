from scrollguard.data_access import CropRequest, read_crop, build_metadata, save_metadata

request = CropRequest(
    scan_id="Scroll1",
    z=1000,
    y0=3520,
    y1=3584,
    x0=4256,
    x1=4320,
)

crop = read_crop(request)
metadata = build_metadata(request, crop)
save_metadata(metadata, "outputs/gate_a_crop_metadata.json")

print("OK metadata saved")
print(metadata)
