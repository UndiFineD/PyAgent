# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\agents\models.py
import datetime
import enum
from typing import Any, Dict, Optional

from fle.commons.models.achievements import ProductionFlows
from pydantic import BaseModel


class TaskResponse(BaseModel):
    meta: Dict[str, Any] = {}
    success: bool


class Response(BaseModel):
    score: float
    achievements: Dict[Any, Any]
    flows: ProductionFlows
    task: TaskResponse
    step: int
    ticks: int
    code: str
    created_at: datetime.datetime
    response: str
    error: bool = False
    program_id: Optional[int] = None


class CompletionReason(enum.Enum):
    TIMEOUT = "timeout"
    SUCCESS = "success"
    RUNTIME_ERROR = "runtime_error"


class CompletionResult(BaseModel):
    step: int
    reason: CompletionReason
    metadata: Dict[str, Any] = {}
