# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_labelllm.py\backend.py\app.py\models.py\file_43b75a06f8fa.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LabelLLM\backend\app\models\file.py

import time

from uuid import UUID, uuid4

from beanie import Document

from pydantic import BaseModel, Field


class File(Document):
    file_id: UUID

    creator_id: str

    create_time: int


class FileCreate(BaseModel):
    file_id: UUID = Field(default_factory=uuid4)

    creator_id: str

    create_time: int = Field(default_factory=lambda: int(time.time()))


class FileUpdate(BaseModel):
    pass
