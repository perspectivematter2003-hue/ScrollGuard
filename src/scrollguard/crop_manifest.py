from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from scrollguard.cache import crop_cache_name
from scrollguard.data_access import CropRequest


@dataclass(frozen=True)
class CropManifestItem:
    name: str
    request: CropRequest

    @property
    def crop_cache_path(self) -> Path:
        return Path("data_cache/crops") / crop_cache_name(self.request)

    @property
    def feature_cache_dir(self) -> Path:
        return Path("data_cache/features") / self.name

    @property
    def feature_output_dir(self) -> Path:
        return Path("outputs/features") / self.name

    @property
    def quality_cache_dir(self) -> Path:
        return Path("data_cache/quality") / self.name

    @property
    def quality_output_dir(self) -> Path:
        return Path("outputs/quality") / self.name

    @property
    def review_output_dir(self) -> Path:
        return Path("outputs/review") / self.name


def load_crop_manifest(manifest_path: str | Path = "configs/crops_manifest.json") -> list[CropManifestItem]:
    manifest_path = Path(manifest_path)
    raw_items = json.loads(manifest_path.read_text(encoding="utf-8"))

    items: list[CropManifestItem] = []
    for raw in raw_items:
        request = CropRequest(
            scan_id=raw["scan_id"],
            z=raw["z"],
            y0=raw["y0"],
            y1=raw["y1"],
            x0=raw["x0"],
            x1=raw["x1"],
        )
        items.append(CropManifestItem(name=raw["name"], request=request))

    return items


def get_manifest_item(name: str, manifest_path: str | Path = "configs/crops_manifest.json") -> CropManifestItem:
    for item in load_crop_manifest(manifest_path):
        if item.name == name:
            return item

    raise KeyError(f"Crop manifest item not found: {name}")
