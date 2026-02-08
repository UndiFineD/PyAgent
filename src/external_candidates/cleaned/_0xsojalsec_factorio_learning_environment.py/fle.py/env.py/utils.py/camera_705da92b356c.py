# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\env\utils\camera.py
from fle.env.entities import BoundingBox, Position
from pydantic import BaseModel


class Camera(BaseModel):
    centroid: Position
    raw_centroid: Position
    entity_count: int
    bounds: BoundingBox
    zoom: float
    position: Position
