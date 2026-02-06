# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-X-AnyLabeling-Server\app\api\health.py
from datetime import datetime, timezone

from app.schemas.response import HealthResponse
from fastapi import APIRouter

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint.

    Returns:
        Health status with models loaded count.
    """
    from app.main import loader

    return HealthResponse(
        status="healthy",
        models_loaded=len(loader.models),
        timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    )
