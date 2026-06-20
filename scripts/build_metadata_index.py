from pathlib import Path

from scrollguard.metadata_index import load_metadata_files, write_csv, write_jsonl

metadata_files = sorted(Path("outputs").glob("*metadata.json"))
records = load_metadata_files(metadata_files)

write_jsonl(records, "outputs/metadata_index.jsonl")
write_csv(records, "outputs/metadata_index.csv")

print(f"OK indexed {len(records)} metadata file(s)")
print("outputs/metadata_index.jsonl")
print("outputs/metadata_index.csv")
