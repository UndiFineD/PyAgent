# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\env.py\utils.py\camera_705da92b356c.py
# NOTE: extracted with static-only rules; review before use

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
