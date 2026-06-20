from pathlib import Path
import csv
import json
from typing import Iterable


FIELDS = [
    "scan_id",
    "z",
    "y_range",
    "x_range",
    "shape",
    "dtype",
    "min_value",
    "max_value",
    "mean_value",
    "created_unix_time",
    "method",
    "source_file",
]


def load_metadata_files(paths: Iterable[Path]) -> list[dict]:
    records = []
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        data["source_file"] = str(path)
        records.append(data)
    return records


def write_jsonl(records: list[dict], out_path: str | Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")


def write_csv(records: list[dict], out_path: str | Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for record in records:
            row = {field: record.get(field, "") for field in FIELDS}
            writer.writerow(row)
