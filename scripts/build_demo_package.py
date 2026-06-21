from pathlib import Path
import json
import shutil
import subprocess
import time

PACKAGE_DIR = Path("outputs/demo_package/scrollguard_v0_demo")

FILES = [
    "README.md",
    "docs/project_status.md",
    "docs/dashboard_v0.md",
    "outputs/hello_scroll.png",
    "outputs/cached_tiny_crop_preview.png",
    "outputs/metadata_index.csv",
    "outputs/features/feature_index.csv",
    "outputs/features/gate_a_tiny_crop/contact_sheet.png",
    "outputs/quality/quality_index.csv",
    "outputs/quality/gate_a_tiny_crop/quality_contact_sheet.png",
    "outputs/review/gate_a_tiny_crop/review_priority.csv",
    "outputs/review/gate_a_tiny_crop/review_priority_overlay.png",
    "outputs/review/gate_a_tiny_crop/evidence_package_top5.json",
    "outputs/review/gate_a_tiny_crop/evidence_report.md",
    "outputs/review/gate_a_tiny_crop/review_tags.csv",
]

PACKAGE_DIR.mkdir(parents=True, exist_ok=True)

copied = []
missing = []

for file_name in FILES:
    src = Path(file_name)
    if not src.exists():
        missing.append(file_name)
        continue

    dst = PACKAGE_DIR / file_name
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    copied.append(file_name)

if missing:
    raise FileNotFoundError("Missing files for demo package:\n" + "\n".join(missing))

audit = subprocess.run(
    ["./scripts/full_local_audit.sh"],
    capture_output=True,
    text=True,
    check=True,
)

(PACKAGE_DIR / "audit_output.txt").write_text(audit.stdout, encoding="utf-8")

manifest = {
    "package_name": "scrollguard_v0_demo",
    "created_unix_time": time.time(),
    "doctrine": "AI proposes, verifier decides. Never hallucinate letters. Every output must have an evidence trail back to CT data.",
    "local_audit": "passed",
    "vesuvius_server_access": "not used during package build except prior cached Gate A crop",
    "copied_files": copied,
}

(PACKAGE_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

print("OK built ScrollGuard demo package")
print(f"package_dir={PACKAGE_DIR}")
print(f"copied_files={len(copied)}")
print("audit=passed")
