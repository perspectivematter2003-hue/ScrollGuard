from pathlib import Path
import zipfile

zip_path = Path("outputs/demo_package/scrollguard_v0_demo.zip")

if not zip_path.exists():
    raise FileNotFoundError(f"Missing ZIP: {zip_path}. Run scripts/build_demo_zip.py first.")

required = {
    "scrollguard_v0_demo/README.md",
    "scrollguard_v0_demo/manifest.json",
    "scrollguard_v0_demo/audit_output.txt",
    "scrollguard_v0_demo/docs/project_status.md",
    "scrollguard_v0_demo/docs/dashboard_v0.md",
    "scrollguard_v0_demo/outputs/hello_scroll.png",
    "scrollguard_v0_demo/outputs/review/gate_a_tiny_crop/evidence_report.md",
    "scrollguard_v0_demo/outputs/review/gate_a_tiny_crop/evidence_package_top5.json",
    "scrollguard_v0_demo/outputs/review/gate_a_tiny_crop/review_priority_overlay.png",
}

with zipfile.ZipFile(zip_path, "r") as z:
    names = set(z.namelist())

missing = sorted(required - names)
if missing:
    raise FileNotFoundError("Missing files inside ZIP:\n" + "\n".join(missing))

print("OK demo ZIP smoke test passed")
print(f"zip_path={zip_path}")
print(f"zip_size_bytes={zip_path.stat().st_size}")
print(f"zip_file_count={len(names)}")
