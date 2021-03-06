from dataclasses import dataclass
from typing import Tuple, List

from dataclasses_json import DataClassJsonMixin


@dataclass(frozen=True)
class BoundingBox(DataClassJsonMixin):
    left_top: Tuple[int, int]
    right_bottom: Tuple[int, int]


@dataclass
class DetectedObject(DataClassJsonMixin):
    bbox: BoundingBox
    confidence: float
    label: int
    class_name: str


@dataclass
class DetectedObjects(DataClassJsonMixin):
    detected_objects: List[DetectedObject]
