from scrollguard.quality_index import build_quality_record, write_csv, write_jsonl

record = build_quality_record(
    quality_set="gate_a_tiny_crop_quality_v0",
    quality_cache_dir="data_cache/quality/gate_a_tiny_crop",
    quality_output_dir="outputs/quality/gate_a_tiny_crop",
)

records = [record]

write_jsonl(records, "outputs/quality/quality_index.jsonl")
write_csv(records, "outputs/quality/quality_index.csv")

print("OK built quality index")
print("outputs/quality/quality_index.jsonl")
print("outputs/quality/quality_index.csv")
print(record)
