# ScrollGuard Evidence Report

## Doctrine

AI proposes, verifier decides. Never hallucinate letters. Every output must have evidence trail back to CT data.

## Package

- Package name: `gate_a_tiny_crop_top5_review_evidence`
- Evidence count: `5`

## Crop metadata

- Scan ID: `Scroll1`
- Z slice: `1000`
- Y range: `[3520, 3584]`
- X range: `[4256, 4320]`
- Shape: `[64, 64]`
- Dtype: `uint8`
- Mean value: `78.326171875`

## Feature index

- Feature set: `gate_a_tiny_crop_basic_features`
  - Feature dir: `data_cache/features/gate_a_tiny_crop`
  - Contact sheet: `outputs/features/gate_a_tiny_crop/contact_sheet.png`
  - Basic method: `scrollguard.features.basic_image_features.v0`
  - Texture method: `scrollguard.texture_features.structure_tensor_texture_features.v0`

## Quality index

- Quality set: `gate_a_tiny_crop_quality_v0`
  - Quality mean: `0.6975411176681519`
  - Risk mean: `0.30245888233184814`
  - Contact sheet: `outputs/quality/gate_a_tiny_crop/quality_contact_sheet.png`
  - Method: `scrollguard.quality_scorer.score_surface_quality.v0`

## Top-risk evidence items

### Rank 1 — `Scroll1_z1000_tile_0001`

- Scan ID: `Scroll1`
- Z: `1000`
- Tile coordinate: `{'tile_y0': 0, 'tile_y1': 16, 'tile_x0': 16, 'tile_x1': 32}`
- Voxel coordinate: `{'voxel_y0': 3520, 'voxel_y1': 3536, 'voxel_x0': 4272, 'voxel_x1': 4288}`
- Risk mean: `0.3811179995536804`
- Risk max: `0.6192857027053833`
- Quality mean: `0.6188820004463196`
- Quality min: `0.3807142972946167`

Feature stats:
- `gradient_magnitude`: mean=0.849617600440979, min=0.0, max=2.1475093364715576
- `local_std`: mean=0.20007118582725525, min=0.06618829816579819, max=0.3467682898044586
- `texture_coherence`: mean=0.7539802193641663, min=0.10410631448030472, max=0.9934315085411072
- `quality_map`: mean=0.6188820004463196, min=0.3807142972946167, max=0.8989313244819641
- `risk_map`: mean=0.3811179995536804, min=0.10106867551803589, max=0.6192857027053833

### Rank 2 — `Scroll1_z1000_tile_0002`

- Scan ID: `Scroll1`
- Z: `1000`
- Tile coordinate: `{'tile_y0': 16, 'tile_y1': 32, 'tile_x0': 16, 'tile_x1': 32}`
- Voxel coordinate: `{'voxel_y0': 3536, 'voxel_y1': 3552, 'voxel_x0': 4272, 'voxel_x1': 4288}`
- Risk mean: `0.34701070189476013`
- Risk max: `0.53633052110672`
- Quality mean: `0.6529892683029175`
- Quality min: `0.46366947889328003`

Feature stats:
- `gradient_magnitude`: mean=0.6250324249267578, min=0.0, max=1.4749858379364014
- `local_std`: mean=0.13857656717300415, min=0.04531341418623924, max=0.2749931216239929
- `texture_coherence`: mean=0.6369062662124634, min=0.05473437160253525, max=0.9543468952178955
- `quality_map`: mean=0.6529892683029175, min=0.46366947889328003, max=0.8960589170455933
- `risk_map`: mean=0.34701070189476013, min=0.10394108295440674, max=0.53633052110672

### Rank 3 — `Scroll1_z1000_tile_0003`

- Scan ID: `Scroll1`
- Z: `1000`
- Tile coordinate: `{'tile_y0': 0, 'tile_y1': 16, 'tile_x0': 32, 'tile_x1': 48}`
- Voxel coordinate: `{'voxel_y0': 3520, 'voxel_y1': 3536, 'voxel_x0': 4288, 'voxel_x1': 4304}`
- Risk mean: `0.3452908992767334`
- Risk max: `0.5475670099258423`
- Quality mean: `0.6547091007232666`
- Quality min: `0.4524330198764801`

Feature stats:
- `gradient_magnitude`: mean=0.5258780717849731, min=0.0, max=1.3353893756866455
- `local_std`: mean=0.12305781245231628, min=0.028979811817407608, max=0.2534165680408478
- `texture_coherence`: mean=0.5728352069854736, min=0.07187818735837936, max=0.9149622321128845
- `quality_map`: mean=0.6547091007232666, min=0.4524330198764801, max=0.8621594309806824
- `risk_map`: mean=0.3452908992767334, min=0.13784056901931763, max=0.5475670099258423

### Rank 4 — `Scroll1_z1000_tile_0004`

- Scan ID: `Scroll1`
- Z: `1000`
- Tile coordinate: `{'tile_y0': 16, 'tile_y1': 32, 'tile_x0': 32, 'tile_x1': 48}`
- Voxel coordinate: `{'voxel_y0': 3536, 'voxel_y1': 3552, 'voxel_x0': 4288, 'voxel_x1': 4304}`
- Risk mean: `0.3325774073600769`
- Risk max: `0.5384430885314941`
- Quality mean: `0.6674225926399231`
- Quality min: `0.46155688166618347`

Feature stats:
- `gradient_magnitude`: mean=0.4919207692146301, min=0.0, max=1.1282627582550049
- `local_std`: mean=0.10615981370210648, min=0.040732257068157196, max=0.17948085069656372
- `texture_coherence`: mean=0.5603266954421997, min=0.04949041083455086, max=0.9309725165367126
- `quality_map`: mean=0.6674225926399231, min=0.46155688166618347, max=0.8342302441596985
- `risk_map`: mean=0.3325774073600769, min=0.1657697558403015, max=0.5384430885314941

### Rank 5 — `Scroll1_z1000_tile_0005`

- Scan ID: `Scroll1`
- Z: `1000`
- Tile coordinate: `{'tile_y0': 32, 'tile_y1': 48, 'tile_x0': 48, 'tile_x1': 64}`
- Voxel coordinate: `{'voxel_y0': 3552, 'voxel_y1': 3568, 'voxel_x0': 4304, 'voxel_x1': 4320}`
- Risk mean: `0.3309711813926697`
- Risk max: `0.5873632431030273`
- Quality mean: `0.6690287590026855`
- Quality min: `0.41263678669929504`

Feature stats:
- `gradient_magnitude`: mean=0.5889673233032227, min=0.0, max=1.5625942945480347
- `local_std`: mean=0.13083241879940033, min=0.04451199993491173, max=0.25407397747039795
- `texture_coherence`: mean=0.6483526229858398, min=0.05761405825614929, max=0.9656857848167419
- `quality_map`: mean=0.6690287590026855, min=0.41263678669929504, max=0.9151573777198792
- `risk_map`: mean=0.3309711813926697, min=0.08484262228012085, max=0.5873632431030273

