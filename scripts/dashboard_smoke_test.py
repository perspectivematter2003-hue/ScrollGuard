from pathlib import Path

required = [
    Path("apps/scrollguard_dashboard.py"),
    Path("scripts/run_dashboard.sh"),
    Path("docs/dashboard_v0.md"),
    Path("outputs/hello_scroll.png"),
    Path("outputs/cached_tiny_crop_preview.png"),
    Path("outputs/features/gate_a_tiny_crop/contact_sheet.png"),
    Path("outputs/quality/gate_a_tiny_crop/quality_contact_sheet.png"),
    Path("outputs/review/gate_a_tiny_crop/review_priority_overlay.png"),
    Path("outputs/review/gate_a_tiny_crop/evidence_package_top5.json"),
]

missing = [str(p) for p in required if not p.exists()]
if missing:
    raise FileNotFoundError("Missing dashboard files:\n" + "\n".join(missing))

dashboard_text = Path("apps/scrollguard_dashboard.py").read_text(encoding="utf-8")
assert "use_container_width" not in dashboard_text, "Old Streamlit use_container_width still present"
assert 'width="stretch"' in dashboard_text, "Expected Streamlit width='stretch' setting"

print("OK dashboard smoke test passed")
print("Dashboard v0 files exist.")
print("No Vesuvius server access used in this test.")
