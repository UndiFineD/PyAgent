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
import time
from pathlib import Path

import psutil
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .session_manager import SessionManager
from .ws_handler import handle_message

logger = logging.getLogger(__name__)

# ── System-metrics differential state ───────────────────────────────────────
_prev_net: dict = {}
_prev_net_ts: float = 0.0
_prev_disk: tuple = (0, 0)
_prev_disk_ts: float = 0.0

_FILTERED_PREFIXES = ("lo", "loopback", "docker", "veth", "br-", "virbr", "vmnet", "vbox")


def _filter_iface(name: str) -> bool:
    """Return True if the interface should be INCLUDED (not filtered)."""
    lower = name.lower()
    return not any(lower.startswith(p) for p in _FILTERED_PREFIXES)


# Project root is two levels up from this file (backend/app.py → backend/ → project root)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_LOGS_DIR = _PROJECT_ROOT / "docs" / "agents"
_AGENTS_DIR = _PROJECT_ROOT / ".github" / "agents"

# ── Project data ─────────────────────────────────────────────────────────────
_PROJECTS_FILE = _PROJECT_ROOT / "data" / "projects.json"


def _load_projects() -> list[dict]:
    """Load data/projects.json at module startup. Returns [] on missing/corrupt file."""
    if not _PROJECTS_FILE.exists():
        logger.warning("data/projects.json not found at %s", _PROJECTS_FILE)
        return []
    try:
        return json.loads(_PROJECTS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to load data/projects.json: %s", exc)
        return []


_PROJECTS: list[dict] = _load_projects()

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


# ── System-metrics models ────────────────────────────────────────────────────

class NetworkInterface(BaseModel):
    """Per-NIC network throughput in KB/s."""

    interface: str
    tx_kbps: float
    rx_kbps: float


class MemoryMetrics(BaseModel):
    """System memory usage snapshot."""

    used_mb: float
    total_mb: float
    percent: float


class DiskMetrics(BaseModel):
    """Aggregate disk I/O throughput in KB/s."""

    read_kbps: float
    write_kbps: float


class SystemMetricsResponse(BaseModel):
    """Full system metrics payload returned by GET /api/metrics/system."""

    cpu_percent: float
    memory: MemoryMetrics
    network: list[NetworkInterface]
    disk: DiskMetrics
    sampled_at: float


@app.get("/api/metrics/system", response_model=SystemMetricsResponse)
async def get_system_metrics() -> SystemMetricsResponse:
    """Return real-time CPU, memory, network IO, and disk IO metrics."""
    global _prev_net, _prev_net_ts, _prev_disk, _prev_disk_ts

    now = time.monotonic()
    cpu = psutil.cpu_percent(interval=None)
    vm = psutil.virtual_memory()
    net_raw = psutil.net_io_counters(pernic=True)
    disk_raw = psutil.disk_io_counters()

    # Network delta KB/s
    dt_net = now - _prev_net_ts if _prev_net_ts else 0.0
    network_entries = []
    for iface, counters in net_raw.items():
        if not _filter_iface(iface):
            continue
        if dt_net > 0 and iface in _prev_net:
            prev = _prev_net[iface]
            tx_kbps = max(0.0, (counters.bytes_sent - prev.bytes_sent) / dt_net / 1024)
            rx_kbps = max(0.0, (counters.bytes_recv - prev.bytes_recv) / dt_net / 1024)
        else:
            tx_kbps, rx_kbps = 0.0, 0.0
        network_entries.append(
            NetworkInterface(interface=iface, tx_kbps=round(tx_kbps, 2), rx_kbps=round(rx_kbps, 2))
        )
    _prev_net = net_raw
    _prev_net_ts = now

    # Disk delta KB/s
    dt_disk = now - _prev_disk_ts if _prev_disk_ts else 0.0
    if dt_disk > 0 and disk_raw:
        read_kbps = max(0.0, (disk_raw.read_bytes - _prev_disk[0]) / dt_disk / 1024)
        write_kbps = max(0.0, (disk_raw.write_bytes - _prev_disk[1]) / dt_disk / 1024)
    else:
        read_kbps, write_kbps = 0.0, 0.0
    _prev_disk = (disk_raw.read_bytes if disk_raw else 0, disk_raw.write_bytes if disk_raw else 0)
    _prev_disk_ts = now

    return SystemMetricsResponse(
        cpu_percent=round(cpu, 1),
        memory=MemoryMetrics(
            used_mb=round(vm.used / 1024 / 1024, 1),
            total_mb=round(vm.total / 1024 / 1024, 1),
            percent=round(vm.percent, 1),
        ),
        network=network_entries,
        disk=DiskMetrics(read_kbps=round(read_kbps, 2), write_kbps=round(write_kbps, 2)),
        sampled_at=time.time(),
    )


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


# ── Project models + endpoint ─────────────────────────────────────────────────

from typing import Literal, Optional as _Opt  # noqa: E402

_LaneLit = Literal["Ideas", "Discovery", "Design", "In Sprint", "Review", "Released", "Archived"]
_PriorityLit = Literal["P1", "P2", "P3", "P4"]
_BudgetLit = Literal["XS", "S", "M", "L", "XL", "unknown"]


class ProjectModel(BaseModel):
    """Single project entry from data/projects.json."""

    id: str
    name: str
    lane: _LaneLit
    summary: str
    branch: _Opt[str] = None
    pr: _Opt[int] = None
    priority: _PriorityLit = "P3"
    budget_tier: _BudgetLit = "M"
    tags: list[str] = []
    created: _Opt[str] = None
    updated: _Opt[str] = None


import re as _re  # noqa: E402

_PROJECT_ID_RE = _re.compile(r"^prj\d{7}$")


def _projects_validated(projects: list[dict]) -> list[ProjectModel]:
    """Validate a raw project list, skipping malformed entries with a warning."""
    valid: list[ProjectModel] = []
    for entry in projects:
        try:
            valid.append(ProjectModel(**entry))
        except Exception as exc:  # pydantic ValidationError
            logger.warning("Skipping malformed project entry %s: %s", entry.get("id"), exc)
    return valid


def _write_projects(projects: list[dict]) -> None:
    """Persist project list to disk atomically and refresh the in-memory cache."""
    tmp = _PROJECTS_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(projects, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(_PROJECTS_FILE)
    _PROJECTS[:] = projects  # keep the cached list object in sync


@app.get("/api/projects", response_model=list[ProjectModel])
async def get_projects(lane: _Opt[str] = None) -> list[ProjectModel]:
    """Return all projects, always reading from disk so restarts are never needed."""
    if not _PROJECTS_FILE.exists():
        raise HTTPException(status_code=500, detail="data/projects.json not found")
    projects = _load_projects()
    valid = _projects_validated(projects)
    if lane:
        return [p for p in valid if p.lane == lane]
    return valid


class ProjectPatch(BaseModel):
    """Fields that may be patched on an existing project."""

    name: _Opt[str] = None
    lane: _Opt[_LaneLit] = None
    summary: _Opt[str] = None
    branch: _Opt[str] = None
    pr: _Opt[int] = None
    priority: _Opt[_PriorityLit] = None
    budget_tier: _Opt[_BudgetLit] = None
    tags: _Opt[list[str]] = None
    updated: _Opt[str] = None


@app.patch("/api/projects/{project_id}", response_model=ProjectModel)
async def patch_project(project_id: str, patch: ProjectPatch) -> ProjectModel:
    """Update fields on an existing project. Always reads from disk first."""
    if not _PROJECT_ID_RE.match(project_id):
        raise HTTPException(status_code=400, detail="Invalid project_id format")
    projects = _load_projects()
    for i, entry in enumerate(projects):
        if entry.get("id") == project_id:
            updates = {k: v for k, v in patch.model_dump().items() if v is not None}
            projects[i] = {**entry, **updates}
            _write_projects(projects)
            return ProjectModel(**projects[i])
    raise HTTPException(status_code=404, detail=f"Project {project_id!r} not found")


class ProjectCreate(ProjectModel):
    """Full project payload required to create a new entry."""


@app.post("/api/projects", response_model=ProjectModel, status_code=201)
async def create_project(body: ProjectCreate) -> ProjectModel:
    """Append a new project entry. Always reads from disk first to check for duplicates."""
    if not _PROJECT_ID_RE.match(body.id):
        raise HTTPException(status_code=400, detail="Invalid project_id format")
    projects = _load_projects()
    if any(e.get("id") == body.id for e in projects):
        raise HTTPException(status_code=409, detail=f"Project {body.id!r} already exists")
    projects.append(body.model_dump())
    _write_projects(projects)
    return body


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
