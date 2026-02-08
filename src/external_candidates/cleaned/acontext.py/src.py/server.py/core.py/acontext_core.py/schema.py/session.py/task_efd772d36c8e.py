# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\schema\session\task.py
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel

from ..utils import asUUID


class TaskStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class TaskData(BaseModel):
    task_description: str
    progresses: Optional[list[str]] = None
    user_preferences: Optional[list[str]] = None
    sop_thinking: Optional[str] = None


class TaskSchema(BaseModel):
    id: asUUID
    session_id: asUUID

    order: int
    status: TaskStatus
    data: TaskData
    space_digested: bool
    raw_message_ids: list[asUUID]

    def to_string(self) -> str:
        return f"Task {self.order}: {self.data.task_description} (Status: {self.status})"
