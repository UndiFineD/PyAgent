# Extracted from: C:\DEV\PyAgent\.external\agentkit\backend\app\app\api\v1\api.py
# -*- coding: utf-8 -*-
from app.api.v1.endpoints import chat, sql, statistics
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(
    sql.router,
    prefix="/sql",
    tags=["sql"],
)
api_router.include_router(
    chat.router,
    prefix="/chat",
    tags=["chat"],
)
api_router.include_router(
    statistics.router,
    prefix="/statistics",
    tags=["statistics"],
)
