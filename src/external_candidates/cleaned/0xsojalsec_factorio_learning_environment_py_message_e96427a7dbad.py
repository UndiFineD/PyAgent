# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\commons.py\models.py\message_e96427a7dbad.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\commons\models\message.py

from typing import Any, Dict

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str

    content: str

    metadata: Dict[str, Any] = Field(default_factory=dict)
