# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-X-AnyLabeling-Server\app\schemas\response.py
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .shape import Shape


class ErrorDetail(BaseModel):
    """Error detail schema."""

    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class SuccessResponse(BaseModel):
    """Success response schema."""

    success: bool = True
    data: Any


class ErrorResponse(BaseModel):
    """Error response schema."""

    success: bool = False
    error: ErrorDetail


class HealthResponse(BaseModel):
    """Health check response schema."""

    status: str
    models_loaded: int
    timestamp: str


class PredictResponse(BaseModel):
    """Prediction response data schema."""

    shapes: List[Shape] = []
    description: str = ""
    replace: Optional[bool] = None

    class Config:
        exclude_none = True
