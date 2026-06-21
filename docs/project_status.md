# ScrollGuard Project Status

## Current status

Full local audit passed.

Completed:

- Gate A real Vesuvius CT crop
- Local crop cache
- Metadata JSON
- Metadata index
- Basic feature extraction
- Texture-continuity feature extraction
- Feature index
- Surface-quality scorer v0
- Risk map
- Quality index
- Review-priority tile ranking
- Review-priority overlay
- Top-5 evidence package
- Streamlit Dashboard v0
- Local smoke tests for Month 2, Month 3, Month 4, review evidence, and dashboard

## Current pipeline

data cache
→ metadata
→ feature extraction
→ texture features
→ quality/risk scoring
→ review-priority ranking
→ evidence package
→ dashboard

## Current rule

No Vesuvius server access is needed for local audits.

## Next work

1. Add evidence index / report builder.
2. Add simple reviewer tagging file.
3. Improve dashboard with reviewer accept/reject notes.
4. Prepare GitHub-ready README.
5. Prepare early progress-prize style demo package.

## Last verified

Full local audit passed through dashboard smoke test.
