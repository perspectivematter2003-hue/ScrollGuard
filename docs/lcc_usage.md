# LCC CLI Usage

`vc-segcheck lcc` runs the Lamina-Continuity Check pipeline.

LCC detects connected regions where lamina index continuity breaks. In practice, it flags places where a surface appears to jump from one papyrus lamina to another instead of staying on the same lamina.

## What LCC does

LCC takes a 2D lamina-index array and a matching 2D confidence array, then:

1. detects neighboring pixels/vertices with suspicious lamina-index jumps,
2. applies a confidence gate,
3. groups accepted jump edges into review regions,
4. writes a review package with evidence files.

The output is meant for review and triage.

## What LCC does not claim

LCC does **not** claim:

- ink detection
- letter detection
- text readability
- VC3D export
- dashboard output
- machine learning inference

LCC only flags review regions where lamina-continuity appears broken.

## Required inputs

The CLI currently expects:

1. a 2D lamina index `.npy` file
2. a 2D confidence `.npy` file

Both arrays must have the same shape.

Example:

```text
lamina_index.npy   shape=(H, W)
confidence.npy     shape=(H, W)
```

## CLI command

From the repository root:

```bash
PYTHONPATH=src python -m vc_segcheck.cli lcc \
  --lamina-index path/to/lamina_index.npy \
  --confidence path/to/confidence.npy \
  --out outputs/lcc_run \
  --min-abs-delta-k 1 \
  --min-detection-confidence 0.0 \
  --min-gate-confidence 0.5
```

## Expected outputs

A successful run writes files under the output directory.

Expected output files include:

```text
summary.json
discontinuity/discontinuity_report.json
gate/gate_report.json
regions/regions_report.json
regions/region_overlay.png
review_package/report.json
review_package/review_regions.csv
review_package/evidence.json
```

The CLI also prints:

```text
OK vc-segcheck LCC pipeline complete
```

## Minimal smoke test

Run:

```bash
PYTHONPATH=src python scripts/lcc_cli_smoke_test.py
```

Current synthetic smoke expected values:

```text
num_jump_edges=64
num_accepted_edges=64
num_abstained_edges=0
num_regions=1
```

## Evidence discipline

LCC is a review-region flagging tool.

It does not hallucinate letters, claim readability, or infer ink. Every output should remain tied to explicit input arrays and generated evidence files.
