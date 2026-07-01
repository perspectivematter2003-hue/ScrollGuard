# ScrollGuard

ScrollGuard is a Vesuvius Challenge side-project focused on surface-quality scoring, review triage, and evidence tracking for Herculaneum scroll CT outputs.

Core doctrine:

AI proposes, verifier decides. Never hallucinate letters. Every output must have an evidence trail back to the CT data.

## Current status

Full local audit passes.

Completed:

- Gate A real Vesuvius CT crop
- Local crop cache
- Metadata JSON
- Metadata index
- Basic image feature extraction
- Texture-continuity feature extraction
- Feature index
- Surface-quality scorer v0
- Risk map
- Quality index
- Review-priority tile ranking
- Review-priority overlay
- Top-5 evidence package
- Human review tags
- Streamlit Dashboard v0
- Full local audit script

## Pipeline

data cache
→ metadata
→ feature extraction
→ texture features
→ quality/risk scoring
→ review-priority ranking
→ evidence package
→ dashboard

## Run local audit

./scripts/full_local_audit.sh

This audit uses local files only. It does not contact the Vesuvius server.

## Run dashboard

./scripts/run_dashboard.sh

Then open:

http://localhost:8501

## Important outputs

- outputs/hello_scroll.png
- outputs/metadata_index.csv
- outputs/features/feature_index.csv
- outputs/quality/quality_index.csv
- outputs/review/gate_a_tiny_crop/review_priority.csv
- outputs/review/gate_a_tiny_crop/evidence_package_top5.json
- outputs/review/gate_a_tiny_crop/evidence_report.md
- outputs/review/gate_a_tiny_crop/review_tags.csv

## Current limitation

This is a tiny-crop prototype. It proves the ScrollGuard workflow locally, but it is not yet validated on many real segments or community surface outputs.

## Next work

- Evidence index / report package
- Larger cached crop test
- More robust quality scoring
- Reviewer feedback loop
- Progress-prize demo package
## Demo package documentation

See `docs/demo_package_v0.md` for the v0 demo ZIP purpose, build commands, and artifact rules.


## LCC CLI documentation

See `docs/lcc_usage.md` for the current `vc-segcheck lcc` CLI usage, required `.npy` inputs, expected outputs, smoke test command, full local audit command, and evidence discipline.
