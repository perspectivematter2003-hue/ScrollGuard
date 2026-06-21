from pathlib import Path
import json
import csv

evidence_path = Path("outputs/review/gate_a_tiny_crop/evidence_package_top5.json")
quality_index_path = Path("outputs/quality/quality_index.csv")
feature_index_path = Path("outputs/features/feature_index.csv")
out_path = Path("outputs/review/gate_a_tiny_crop/evidence_report.md")

evidence = json.loads(evidence_path.read_text(encoding="utf-8"))

with quality_index_path.open("r", encoding="utf-8") as f:
    quality_rows = list(csv.DictReader(f))

with feature_index_path.open("r", encoding="utf-8") as f:
    feature_rows = list(csv.DictReader(f))

lines = []

lines.append("# ScrollGuard Evidence Report")
lines.append("")
lines.append("## Doctrine")
lines.append("")
lines.append(evidence["doctrine"])
lines.append("")
lines.append("## Package")
lines.append("")
lines.append(f"- Package name: `{evidence['package_name']}`")
lines.append(f"- Evidence count: `{evidence['evidence_count']}`")
lines.append("")
lines.append("## Crop metadata")
lines.append("")
crop = evidence["crop_metadata"]
lines.append(f"- Scan ID: `{crop['scan_id']}`")
lines.append(f"- Z slice: `{crop['z']}`")
lines.append(f"- Y range: `{crop['y_range']}`")
lines.append(f"- X range: `{crop['x_range']}`")
lines.append(f"- Shape: `{crop['shape']}`")
lines.append(f"- Dtype: `{crop['dtype']}`")
lines.append(f"- Mean value: `{crop['mean_value']}`")
lines.append("")
lines.append("## Feature index")
lines.append("")
for row in feature_rows:
    lines.append(f"- Feature set: `{row['feature_set']}`")
    lines.append(f"  - Feature dir: `{row['feature_dir']}`")
    lines.append(f"  - Contact sheet: `{row['contact_sheet']}`")
    lines.append(f"  - Basic method: `{row['basic_method']}`")
    lines.append(f"  - Texture method: `{row['texture_method']}`")
lines.append("")
lines.append("## Quality index")
lines.append("")
for row in quality_rows:
    lines.append(f"- Quality set: `{row['quality_set']}`")
    lines.append(f"  - Quality mean: `{row['quality_mean']}`")
    lines.append(f"  - Risk mean: `{row['risk_mean']}`")
    lines.append(f"  - Contact sheet: `{row['quality_contact_sheet']}`")
    lines.append(f"  - Method: `{row['method']}`")
lines.append("")
lines.append("## Top-risk evidence items")
lines.append("")

for item in evidence["evidence_items"]:
    lines.append(f"### Rank {item['rank']} — `{item['review_id']}`")
    lines.append("")
    lines.append(f"- Scan ID: `{item['scan_id']}`")
    lines.append(f"- Z: `{item['z']}`")
    lines.append(f"- Tile coordinate: `{item['tile_coordinate']}`")
    lines.append(f"- Voxel coordinate: `{item['voxel_coordinate']}`")
    lines.append(f"- Risk mean: `{item['ranking_values']['risk_mean']}`")
    lines.append(f"- Risk max: `{item['ranking_values']['risk_max']}`")
    lines.append(f"- Quality mean: `{item['ranking_values']['quality_mean']}`")
    lines.append(f"- Quality min: `{item['ranking_values']['quality_min']}`")
    lines.append("")
    lines.append("Feature stats:")
    for feature_name, stats in item["feature_stats"].items():
        lines.append(
            f"- `{feature_name}`: mean={stats['mean']}, min={stats['min']}, max={stats['max']}"
        )
    lines.append("")

out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("OK built evidence report")
print(f"output={out_path}")
print(f"items={evidence['evidence_count']}")
