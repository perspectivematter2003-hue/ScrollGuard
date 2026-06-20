from pathlib import Path
import csv
import json
from typing import Iterable


FIELDS = [
    "feature_set",
    "source_crop_cache",
    "source_metadata",
    "feature_dir",
    "preview_dir",
    "summary_file",
    "contact_sheet",
    "input_shape",
    "input_dtype",
    "gradient_mean",
    "local_std_mean",
    "method",
]


def build_feature_record(
    feature_set: str,
    source_crop_cache: str | Path,
    source_metadata: str | Path,
    feature_dir: str | Path,
    preview_dir: str | Path,
) -> dict:
    source_crop_cache = Path(source_crop_cache)
    source_metadata = Path(source_metadata)
    feature_dir = Path(feature_dir)
    preview_dir = Path(preview_dir)
    summary_file = preview_dir / "feature_summary.json"
    contact_sheet = preview_dir / "contact_sheet.png"

    summary = json.loads(summary_file.read_text(encoding="utf-8"))

    return {
        "feature_set": feature_set,
        "source_crop_cache": str(source_crop_cache),
        "source_metadata": str(source_metadata),
        "feature_dir": str(feature_dir),
        "preview_dir": str(preview_dir),
        "summary_file": str(summary_file),
        "contact_sheet": str(contact_sheet),
        "input_shape": summary["input_shape"],
        "input_dtype": summary["input_dtype"],
        "gradient_mean": summary["gradient_mean"],
        "local_std_mean": summary["local_std_mean"],
        "method": summary["method"],
    }


def write_jsonl(records: Iterable[dict], out_path: str | Path) -> None:
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
            writer.writerow({field: record.get(field, "") for field in FIELDS})
