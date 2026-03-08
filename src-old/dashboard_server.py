#!/usr/bin/env python3
# some environments have incompatible FastAPI/pydantic versions, so
# wrap imports in a try/except. we also prefer functools.lru_cache

from functools import lru_cache

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
except Exception:
    # FastAPI not available or pydantic version mismatch; define dummies
    HTTPException = Exception

    class _DummyApp:
        """Dummy FastAPI app for environments without FastAPI or with incompatible pydantic versions."""

        def __init__(self, *args, **kwargs) -> None:
            """No-op constructor."""
            pass

        def add_middleware(self, *args, **kwargs) -> None:
            """No-op middleware adder."""
            pass

        def get(self, *args, **kwargs) -> None:

            """Decorator for GET endpoints (no-op)."""
            def decorator(func) -> None:
                """No-op endpoint decorator."""
                return func

            return decorator

    FastAPI = _DummyApp

    class CORSMiddleware:
        """Dummy CORS middleware."""

        def __init__(self, *args, **kwargs) -> None:
            """No-op middleware."""
            pass

from typing import List, Dict, Any
import json
# import os

from pathlib import Path

app = FastAPI(title="PyAgent Unified Desktop API")

# Enable CORS for frontend interaction

from src.version import VERSION
__logic_category__ = "General"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

LOG_FILE = Path("logs/episodic_memory.jsonl")


@app.get("/api/status")
async def get_status() -> Dict[str, Any]:
    """Returns current status of the agent."""
    return {"status": "online", "agent": "PyAgent", "version": "2026.1.0"}


@app.get("/api/thoughts")
async def get_thoughts(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieve the latest episodic memories (agent thoughts/actions)."""
    if not LOG_FILE.exists():
        return []
    
    thoughts = []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[-limit:]:
                thoughts.append(json.loads(line))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return thoughts[::-1] # Return newest first


@app.get("/api/artifacts")
async def list_artifacts() -> List[Dict[str, Any]]:
    """List files in the 'src/classes/generated' or 'logs/screenshots' folders."""
    artifacts = []
    paths = [Path("src/classes/generated"), Path("logs/screenshots")]
    
    for p in paths:
        if p.exists():
            for item in p.iterdir():
                if item.is_file():
                    artifacts.append({
                        "name": item.name,
                        "path": str(item),
                        "size": item.stat().st_size,
                        "modified": item.stat().st_mtime
                    })
    return artifacts


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
