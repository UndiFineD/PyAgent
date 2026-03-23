#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""FastAPI backend worker — WebSocket + signaling endpoints."""
from __future__ import annotations

import json
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .session_manager import SessionManager
from .ws_handler import handle_message

logger = logging.getLogger(__name__)

# Project root is two levels up from this file (backend/app.py → backend/ → project root)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_LOGS_DIR    = _PROJECT_ROOT / "docs" / "agents"
_AGENTS_DIR  = _PROJECT_ROOT / ".github" / "agents"

# Allowlist of valid agent IDs — prevents any path-traversal attack
_VALID_AGENT_IDS = frozenset({
    "0master", "1project", "2think", "3design", "4plan",
    "5test", "6code", "7exec", "8ql", "9git",
})


def _log_path(agent_id: str) -> Path:
    if agent_id not in _VALID_AGENT_IDS:
        raise HTTPException(status_code=400, detail=f"Unknown agent_id: {agent_id!r}")
    return _LOGS_DIR / f"{agent_id}.log.md"


app = FastAPI(title="PyAgent Backend Worker", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions = SessionManager()


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


# ── Agent log file endpoints ─────────────────────────────────────────────────

class AgentLogBody(BaseModel):
    """Request body for the agent-log write endpoint."""

    content: str


@app.get("/api/agent-log/{agent_id}")
async def read_agent_log(agent_id: str) -> dict[str, str]:
    """Return the current contents of docs/agents/<agent_id>.log.md."""
    path = _log_path(agent_id)
    if not path.exists():
        return {"content": ""}
    return {"content": path.read_text(encoding="utf-8")}


@app.put("/api/agent-log/{agent_id}")
async def write_agent_log(agent_id: str, body: AgentLogBody) -> dict[str, str]:
    """Overwrite docs/agents/<agent_id>.log.md with the supplied content."""
    path = _log_path(agent_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.content, encoding="utf-8")
    logger.debug("Saved agent log: %s (%d bytes)", path.name, len(body.content))
    return {"status": "ok", "path": str(path.relative_to(_PROJECT_ROOT))}


# ── Agent definition file endpoints ──────────────────────────────────────────

class AgentDocBody(BaseModel):
    """Request body for the agent-doc write endpoint."""

    content: str


@app.get("/api/agent-doc/{agent_id}")
async def read_agent_doc(agent_id: str) -> dict[str, str]:
    """Return the contents of .github/agents/<agent_id>.agent.md."""
    if agent_id not in _VALID_AGENT_IDS:
        raise HTTPException(status_code=400, detail=f"Unknown agent_id: {agent_id!r}")
    path = _AGENTS_DIR / f"{agent_id}.agent.md"
    if not path.exists():
        return {"content": ""}
    return {"content": path.read_text(encoding="utf-8")}


@app.put("/api/agent-doc/{agent_id}")
async def write_agent_doc(agent_id: str, body: AgentDocBody) -> dict[str, str]:
    """Overwrite .github/agents/<agent_id>.agent.md with the supplied content."""
    if agent_id not in _VALID_AGENT_IDS:
        raise HTTPException(status_code=400, detail=f"Unknown agent_id: {agent_id!r}")
    path = _AGENTS_DIR / f"{agent_id}.agent.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.content, encoding="utf-8")
    logger.debug("Saved agent doc: %s (%d bytes)", path.name, len(body.content))
    return {"status": "ok", "path": str(path.relative_to(_PROJECT_ROOT))}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """WebSocket endpoint for real-time communication."""
    session_id = await sessions.connect(websocket)
    logger.info("WebSocket connected: %s", session_id)
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_text(
                    json.dumps({"type": "error", "error": "Invalid JSON"})
                )
                continue
            await handle_message(sessions, session_id, websocket, data)
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected: %s", session_id)
        sessions.disconnect(session_id)
