# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LabelLLM\backend\app\api\router.py
from fastapi import APIRouter

from .v1.router import v1_router

router = APIRouter()
router.include_router(v1_router)


@router.get("/health")
async def health():
    return {"status": "ok"}
