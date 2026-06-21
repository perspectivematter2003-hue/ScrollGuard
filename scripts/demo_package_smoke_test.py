from pathlib import Path
import json

package_dir = Path("outputs/demo_package/scrollguard_v0_demo")

required = [
    package_dir / "README.md",
    package_dir / "docs/project_status.md",
    package_dir / "docs/dashboard_v0.md",
    package_dir / "outputs/hello_scroll.png",
    package_dir / "outputs/metadata_index.csv",
    package_dir / "outputs/features/feature_index.csv",
    package_dir / "outputs/features/gate_a_tiny_crop/contact_sheet.png",
    package_dir / "outputs/quality/quality_index.csv",
    package_dir / "outputs/quality/gate_a_tiny_crop/quality_contact_sheet.png",
    package_dir / "outputs/review/gate_a_tiny_crop/review_priority.csv",
    package_dir / "outputs/review/gate_a_tiny_crop/review_priority_overlay.png",
    package_dir / "outputs/review/gate_a_tiny_crop/evidence_package_top5.json",
    package_dir / "outputs/review/gate_a_tiny_crop/evidence_report.md",
    package_dir / "outputs/review/gate_a_tiny_crop/review_tags.csv",
    package_dir / "audit_output.txt",
    package_dir / "manifest.json",
]

missing = [str(p) for p in required if not p.exists()]
if missing:
    raise FileNotFoundError("Missing demo package files:\n" + "\n".join(missing))

manifest = json.loads((package_dir / "manifest.json").read_text(encoding="utf-8"))
audit_text = (package_dir / "audit_output.txt").read_text(encoding="utf-8")

assert manifest["package_name"] == "scrollguard_v0_demo"
assert manifest["local_audit"] == "passed"
assert "OK full ScrollGuard local audit passed" in audit_text

print("OK demo package smoke test passed")
print(f"package_dir={package_dir}")
print(f"copied_files={len(manifest['copied_files'])}")
print("No Vesuvius server access used in this test.")
