from pathlib import Path
import csv
import json

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]

def p(relative: str) -> Path:
    return ROOT / relative

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def read_csv(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

st.set_page_config(page_title="ScrollGuard Dashboard v0", layout="wide")

st.title("ScrollGuard Dashboard v0")
st.caption("Local evidence dashboard: no Vesuvius server access used.")

st.header("Gate A CT Crop")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Original CT crop")
    st.image(str(p("outputs/hello_scroll.png")))

with col2:
    st.subheader("Cached crop preview")
    st.image(str(p("outputs/cached_tiny_crop_preview.png")))

st.header("Month 3 Feature Review")
st.image(str(p("outputs/features/gate_a_tiny_crop/contact_sheet.png")))

feature_index = read_csv(p("outputs/features/feature_index.csv"))
st.subheader("Feature Index")
st.dataframe(feature_index, width="stretch")

st.header("Month 4 Quality / Risk Review")
st.image(str(p("outputs/quality/gate_a_tiny_crop/quality_contact_sheet.png")))

quality_index = read_csv(p("outputs/quality/quality_index.csv"))
st.subheader("Quality Index")
st.dataframe(quality_index, width="stretch")

st.header("Review-Priority Tiles")
st.image(str(p("outputs/review/gate_a_tiny_crop/review_priority_overlay.png")))

review_rows = read_csv(p("outputs/review/gate_a_tiny_crop/review_priority.csv"))
st.subheader("Review Priority Ranking")
st.dataframe(review_rows, width="stretch")

st.header("Top-5 Evidence Package")
evidence = read_json(p("outputs/review/gate_a_tiny_crop/evidence_package_top5.json"))

st.write({
    "package_name": evidence["package_name"],
    "evidence_count": evidence["evidence_count"],
    "scan_id": evidence["crop_metadata"]["scan_id"],
    "z": evidence["crop_metadata"]["z"],
    "shape": evidence["crop_metadata"]["shape"],
})

for item in evidence["evidence_items"]:
    with st.expander(f"Rank {item['rank']} — {item['review_id']}"):
        st.json(item)

st.success("Dashboard v0 loaded from local ScrollGuard outputs.")
