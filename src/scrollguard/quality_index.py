from pathlib import Path
import csv
import json
from typing import Iterable


FIELDS = [
    "quality_set",
    "source_crop_cache",
    "source_metadata",
    "feature_index",
    "quality_cache_dir",
    "quality_output_dir",
    "quality_summary",
    "quality_contact_sheet",
    "input_shape",
    "quality_mean",
    "risk_mean",
    "method",
]


def build_quality_record(
    quality_set: str,
    quality_cache_dir: str | Path,
    quality_output_dir: str | Path,
) -> dict:
    quality_cache_dir = Path(quality_cache_dir)
    quality_output_dir = Path(quality_output_dir)

    summary_file = quality_output_dir / "quality_summary.json"
    contact_sheet = quality_output_dir / "quality_contact_sheet.png"

    summary = json.loads(summary_file.read_text(encoding="utf-8"))
    evidence = summary["evidence_source"]

    return {
        "quality_set": quality_set,
        "source_crop_cache": evidence["source_crop_cache"],
        "source_metadata": evidence["source_metadata"],
        "feature_index": evidence["feature_index"],
        "quality_cache_dir": str(quality_cache_dir),
        "quality_output_dir": str(quality_output_dir),
        "quality_summary": str(summary_file),
        "quality_contact_sheet": str(contact_sheet),
        "input_shape": summary["input_shape"],
        "quality_mean": summary["quality_mean"],
        "risk_mean": summary["risk_mean"],
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
