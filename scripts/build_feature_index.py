from scrollguard.feature_index import build_feature_record, write_csv, write_jsonl

record = build_feature_record(
    feature_set="gate_a_tiny_crop_basic_features",
    source_crop_cache="data_cache/crops/Scroll1_z1000_y3520_3584_x4256_4320.npy",
    source_metadata="outputs/cached_tiny_crop_metadata.json",
    feature_dir="data_cache/features/gate_a_tiny_crop",
    preview_dir="outputs/features/gate_a_tiny_crop",
)

records = [record]

write_jsonl(records, "outputs/features/feature_index.jsonl")
write_csv(records, "outputs/features/feature_index.csv")

print("OK built feature index")
print("outputs/features/feature_index.jsonl")
print("outputs/features/feature_index.csv")
print(record)
