# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_labelllm.py\backend.py\app.py\schemas.py\message_c75758a78d1b.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LabelLLM\backend\app\schemas\message.py

from typing import Literal

from uuid import UUID

from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    message_id: UUID = Field(description="消息ID")

    parent_id: UUID | None = Field(description="父消息ID", default=None)

    message_type: Literal["send", "receive"] = Field(description="消息类型")

    content: str = Field(description="消息内容")


class Message(MessageBase):
    user_id: str = Field(description="用户ID", default="")
