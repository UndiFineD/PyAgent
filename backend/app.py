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
import random
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import psutil
from fastapi import APIRouter, Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

from .auth import require_auth, websocket_auth
from .memory_store import memory_store
from .rate_limiter import RateLimitMiddleware
from .logging_config import get_logger, setup_logging
from .session_manager import SessionManager
from .tracing import tracer  # noqa: F401 — initialises OTel TracerProvider on import
from .watchdog import watchdog
from .ws_crypto import decrypt_message, derive_shared_secret, encrypt_message, generate_keypair
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
_LOGS_DIR = _PROJECT_ROOT / ".github" / "agents" / "data"
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

_logger = setup_logging()
_logger.info("PyAgent backend starting", extra={"correlation_id": "", "endpoint": ""})


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Inject X-Correlation-ID into every response."""

    async def dispatch(self, request, call_next):  # type: ignore[override]
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response


app.add_middleware(CorrelationIdMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware)


class VersionHeaderMiddleware(BaseHTTPMiddleware):
    """Inject API version headers.

    * ``X-API-Version: 1``   — added on all ``/api/v1/`` responses.
    * ``Deprecation: true``  — added on bare ``/api/`` responses that have a v1 counterpart.
    """

    async def dispatch(self, request, call_next):  # type: ignore[override]
        response = await call_next(request)
        path = request.url.path
        if path.startswith("/api/v1/"):
            response.headers["X-API-Version"] = "1"
        elif path.startswith("/api/") and not path.startswith("/api/v1/"):
            response.headers["Deprecation"] = "true"
            response.headers["Link"] = (
                f'<{path.replace("/api/", "/api/v1/", 1)}>; rel="successor-version"'
            )
        return response


app.add_middleware(VersionHeaderMiddleware)

sessions = SessionManager()

# Protected router — all routes registered here require authentication.
# /health remains on `app` directly so load-balancers never need credentials.
_auth_router = APIRouter(dependencies=[Depends(require_auth)])


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    get_logger().info("Health check", extra={"correlation_id": "health", "endpoint": "/health"})
    return {"status": "ok"}


@app.get("/api/metrics/flm")
async def flm_metrics() -> dict:
    """Return simulated FLM token throughput metrics."""
    now = time.time()
    samples = [
        {
            "timestamp": now - (9 - i),
            "tokens_per_second": round(random.uniform(50, 500), 1),
            "model": "llama3-8b",
            "queue_depth": random.randint(0, 10),
        }
        for i in range(10)
    ]
    return {
        "samples": samples,
        "avg_tokens_per_second": round(
            sum(s["tokens_per_second"] for s in samples) / len(samples), 1
        ),
        "peak_tokens_per_second": max(s["tokens_per_second"] for s in samples),
        "model": "llama3-8b",
    }


# ── Plugin registry ───────────────────────────────────────────────────────────

PLUGIN_REGISTRY = [
    {
        "id": "coder-enhanced",
        "name": "CoderAgent Enhanced",
        "description": "Multi-pass code improvement with diff preview",
        "author": "PyAgent Core",
        "version": "1.0.0",
        "tags": ["coding"],
        "installed": False,
    },
    {
        "id": "sec-scanner",
        "name": "Security Scanner",
        "description": "OWASP Top 10 static analysis on staged files",
        "author": "PyAgent Security",
        "version": "0.9.0",
        "tags": ["security"],
        "installed": False,
    },
    {
        "id": "doc-gen",
        "name": "DocGen",
        "description": "Auto-generates docstrings and README updates",
        "author": "PyAgent Docs",
        "version": "1.1.0",
        "tags": ["docs"],
        "installed": True,
    },
    {
        "id": "rust-bench",
        "name": "Rust Benchmarker",
        "description": "Run criterion benchmarks and report regressions",
        "author": "PyAgent Rust",
        "version": "0.5.0",
        "tags": ["rust", "performance"],
        "installed": False,
    },
    {
        "id": "ci-monitor",
        "name": "CI Monitor",
        "description": "Watch GitHub Actions workflow runs and alert on failures",
        "author": "PyAgent CI",
        "version": "2.0.0",
        "tags": ["ci"],
        "installed": False,
    },
]


@app.get("/api/plugins")
async def list_plugins() -> dict:
    """Return the static plugin registry. No authentication required."""
    return {"plugins": PLUGIN_REGISTRY}


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


@_auth_router.get("/metrics/system", response_model=SystemMetricsResponse)
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


@_auth_router.get("/agent-log/{agent_id}")
async def read_agent_log(agent_id: str) -> dict[str, str]:
    """Return the current contents of docs/agents/<agent_id>.log.md."""
    path = _log_path(agent_id)
    if not path.exists():
        return {"content": ""}
    return {"content": path.read_text(encoding="utf-8")}


@_auth_router.put("/agent-log/{agent_id}")
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


@_auth_router.get("/agent-doc/{agent_id}")
async def read_agent_doc(agent_id: str) -> dict[str, str]:
    """Return the contents of .github/agents/<agent_id>.agent.md."""
    if agent_id not in _VALID_AGENT_IDS:
        raise HTTPException(status_code=400, detail=f"Unknown agent_id: {agent_id!r}")
    path = _AGENTS_DIR / f"{agent_id}.agent.md"
    if not path.exists():
        return {"content": ""}
    return {"content": path.read_text(encoding="utf-8")}


@_auth_router.put("/agent-doc/{agent_id}")
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
_IDEA_STEM_RE = _re.compile(r"^(idea(?P<rank>\d{6}))(?:-(?P<slug>.+))?$", _re.IGNORECASE)
_IDEA_PROJECT_ID_RE = _re.compile(r"prj\d{7}", _re.IGNORECASE)
_IDEA_MAPPING_LINE_RE = _re.compile(r"^Planned project mapping:\s*(.+)$", _re.IGNORECASE)
_PROJECT_STAGE_DIR_RE = _re.compile(r"^(prj\d{7})-", _re.IGNORECASE)

_IDEAS_FILE_ROOT = _PROJECT_ROOT / "docs" / "project" / "ideas"


class IdeaModel(BaseModel):
    """Single parsed idea row returned by GET /api/ideas.

    Attributes:
        idea_id: Canonical idea identifier from filename.
        rank: Numeric rank parsed from filename.
        title: Human-readable title derived from heading or filename.
        summary: Summary text derived from markdown content.
        source_path: Workspace-relative source markdown path.
        mapped_project_id: First mapped project ID, if any.
        mapped_project_ids: All mapped project IDs in first-seen order.
        implemented_project_ids: Mapped IDs currently in implemented lanes.
        implemented: True when any mapped ID is implemented for selected mode.

    """

    idea_id: str
    rank: _Opt[int] = None
    title: str
    summary: str
    source_path: str
    mapped_project_id: _Opt[str] = None
    mapped_project_ids: list[str] = []
    implemented_project_ids: list[str] = []
    implemented: bool = False


def _load_project_lane_map() -> dict[str, str]:
    """Load project lanes keyed by lower-case project ID.

    Returns:
        dict[str, str]: Project ID to lane mapping. Empty when the file is unavailable or malformed.

    """
    if not _PROJECTS_FILE.exists():
        return {}

    try:
        projects = json.loads(_PROJECTS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}

    lane_map: dict[str, str] = {}
    for item in projects:
        project_id = str(item.get("id", "")).lower().strip()
        if not project_id:
            continue
        lane_map[project_id] = str(item.get("lane", "")).strip()
    return lane_map


def _implemented_lanes_for_mode(mode: str) -> set[str]:
    """Resolve implemented lane set for the supplied mode.

    Args:
        mode: Implemented mode query value.

    Returns:
        set[str]: Normalized lane names treated as implemented.

    """
    normalized = mode.strip().lower()
    if normalized == "released_only":
        return {"released"}
    return {"discovery", "design", "in sprint", "review", "released"}


def _implemented_selector(implemented: str) -> str:
    """Normalize implemented query to include/exclude/only selector.

    Args:
        implemented: Raw implemented query string.

    Returns:
        str: One of ``include``, ``exclude``, or ``only``.

    """
    value = implemented.strip().lower()
    if value in {"include", "all"}:
        return "include"
    if value in {"only", "true", "1", "yes"}:
        return "only"
    if value in {"exclude", "false", "0", "no", ""}:
        return "exclude"
    return "exclude"


def _extract_mapped_project_ids(text: str) -> list[str]:
    """Extract mapped project IDs from markdown text.

    Args:
        text: Full markdown content for one idea file.

    Returns:
        list[str]: Unique project IDs in first-seen order.

    """
    mapping_value = ""
    for raw_line in text.splitlines():
        match = _IDEA_MAPPING_LINE_RE.match(raw_line.strip())
        if match is not None:
            mapping_value = match.group(1).strip()
            break

    if not mapping_value or mapping_value.lower() == "none yet":
        return []

    unique: list[str] = []
    seen: set[str] = set()
    for token in _IDEA_PROJECT_ID_RE.findall(mapping_value):
        project_id = token.lower()
        if project_id in seen:
            continue
        seen.add(project_id)
        unique.append(project_id)
    return unique


def _extract_title_summary(text: str, default_title: str) -> tuple[str, str]:
    """Extract title and summary with safe fallbacks.

    Args:
        text: Full markdown content.
        default_title: Fallback title from filename slug.

    Returns:
        tuple[str, str]: Resolved title and summary strings.

    """
    lines = text.splitlines()
    title = default_title
    summary = ""

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
            if heading:
                title = heading
                break

    for index, line in enumerate(lines):
        if line.strip().lower() == "## idea summary":
            for candidate in lines[index + 1 :]:
                candidate_stripped = candidate.strip()
                if not candidate_stripped:
                    continue
                if candidate_stripped.startswith("#"):
                    break
                summary = candidate_stripped
                break
            if summary:
                break

    if not summary:
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                continue
            if _IDEA_MAPPING_LINE_RE.match(stripped):
                continue
            summary = stripped
            break

    if not summary:
        summary = title

    return title, summary


def _parse_idea_file(path: Path, lane_map: dict[str, str], mode: str) -> _Opt[IdeaModel]:
    """Parse one idea markdown file into an API record.

    Args:
        path: Idea markdown path.
        lane_map: Project lane map keyed by project ID.
        mode: Implemented mode query value.

    Returns:
        _Opt[IdeaModel]: Parsed idea record, or None when parsing fails.

    """
    stem_match = _IDEA_STEM_RE.match(path.stem)
    if stem_match is None:
        return None

    idea_id = stem_match.group(1).lower()
    rank_text = stem_match.group("rank")
    slug = stem_match.group("slug") or idea_id
    default_title = slug.replace("-", " ").strip() or idea_id

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        logger.warning("Skipping malformed idea file %s: %s", path, exc)
        return None

    mapped_project_ids = _extract_mapped_project_ids(text)
    implemented_lanes = _implemented_lanes_for_mode(mode)
    implemented_project_ids = [
        project_id
        for project_id in mapped_project_ids
        if lane_map.get(project_id, "").lower() in implemented_lanes
    ]
    title, summary = _extract_title_summary(text, default_title)

    return IdeaModel(
        idea_id=idea_id,
        rank=int(rank_text),
        title=title,
        summary=summary,
        source_path=path.relative_to(_PROJECT_ROOT).as_posix(),
        mapped_project_id=mapped_project_ids[0] if mapped_project_ids else None,
        mapped_project_ids=mapped_project_ids,
        implemented_project_ids=implemented_project_ids,
        implemented=bool(implemented_project_ids),
    )


def _load_ideas(mode: str) -> list[IdeaModel]:
    """Load all parseable ideas from docs/project/ideas.

    Args:
        mode: Implemented mode query value.

    Returns:
        list[IdeaModel]: Parsed idea records.

    """
    if not _IDEAS_FILE_ROOT.exists():
        return []

    lane_map = _load_project_lane_map()
    ideas: list[IdeaModel] = []
    for path in sorted(_IDEAS_FILE_ROOT.glob("idea*.md")):
        parsed = _parse_idea_file(path, lane_map, mode)
        if parsed is not None:
            ideas.append(parsed)
    return ideas


def _idea_path_from_id(idea_id: str) -> _Opt[Path]:
    """Resolve a markdown path for a canonical idea ID.

    Args:
        idea_id: Canonical identifier like ``idea000123``.

    Returns:
        _Opt[Path]: Matched idea file path, or None if not found.

    """
    normalized = idea_id.strip().lower()
    if not _re.fullmatch(r"idea\d{6}", normalized):
        return None

    matches = sorted(_IDEAS_FILE_ROOT.glob(f"{normalized}*.md"))
    if not matches:
        return None
    return matches[0]


def _replace_first_heading(lines: list[str], title: str) -> list[str]:
    """Replace first markdown heading with *title*.

    Falls back to prepending a new H1 heading when none exists.
    """
    for i, line in enumerate(lines):
        if line.strip().startswith("#"):
            lines[i] = f"# {title.strip()}"
            return lines
    return [f"# {title.strip()}", "", *lines]


def _replace_idea_summary(lines: list[str], summary: str) -> list[str]:
    """Replace or append the ``## Idea Summary`` value line."""
    normalized = summary.strip()
    for i, line in enumerate(lines):
        if line.strip().lower() == "## idea summary":
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and not lines[j].strip().startswith("#"):
                lines[j] = normalized
            else:
                lines.insert(i + 1, normalized)
            return lines

    suffix = ["", "## Idea Summary", normalized]
    return [*lines, *suffix]


def _replace_mapping_line(lines: list[str], mapped_project_ids: list[str]) -> list[str]:
    """Replace or append the planned project mapping line."""
    value = ", ".join(mapped_project_ids) if mapped_project_ids else "none yet"
    replacement = f"Planned project mapping: {value}"

    for i, line in enumerate(lines):
        if _IDEA_MAPPING_LINE_RE.match(line.strip()):
            lines[i] = replacement
            return lines

    if lines and lines[-1].strip() != "":
        lines.append("")
    lines.append(replacement)
    return lines


def _ensure_section_content(lines: list[str], heading: str, default_content: str) -> list[str]:
    """Ensure a markdown section exists and contains at least one content line."""
    target = heading.strip().lower()
    for i, line in enumerate(lines):
        if line.strip().lower() != target:
            continue

        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1

        if j < len(lines) and not lines[j].strip().startswith("#"):
            return lines

        lines.insert(i + 1, default_content)
        return lines

    if lines and lines[-1].strip() != "":
        lines.append("")
    lines.extend([heading, default_content])
    return lines


def _priority_sort_rank(idea: IdeaModel) -> int:
    """Return a numeric sort rank for idea priority.

    Priority buckets are resolved from title and summary text with support for
    both textual levels and P1-P4 shorthand.

    Args:
        idea: Parsed idea row.

    Returns:
        int: Priority rank where lower is higher priority.

    """
    haystack = f"{idea.title} {idea.summary}".lower()
    if "critical" in haystack or _re.search(r"\bp1\b", haystack):
        return 0
    if "high" in haystack or _re.search(r"\bp2\b", haystack):
        return 1
    if "medium" in haystack or _re.search(r"\bp3\b", haystack):
        return 2
    if "low" in haystack or _re.search(r"\bp4\b", haystack):
        return 3
    return 4


def _projects_valid() -> list[ProjectModel]:
    """Build validated list from the in-memory _PROJECTS list."""
    valid: list[ProjectModel] = []
    for entry in _PROJECTS:
        try:
            valid.append(ProjectModel(**entry))
        except Exception as exc:  # pydantic ValidationError
            logger.warning("Skipping malformed project entry %s: %s", entry.get("id"), exc)
    return valid


_LANE_RANK: dict[str, int] = {
    "ideas": 0,
    "discovery": 1,
    "design": 2,
    "in sprint": 3,
    "review": 4,
    "released": 5,
    "archived": 6,
}


def _canonical_lane_name(lane: str) -> str:
    """Normalize lane casing for persisted project records."""
    normalized = lane.strip().lower()
    mapping = {
        "ideas": "Ideas",
        "discovery": "Discovery",
        "design": "Design",
        "in sprint": "In Sprint",
        "review": "Review",
        "released": "Released",
        "archived": "Archived",
    }
    return mapping.get(normalized, lane)


def _build_stage_hint_map() -> dict[str, str]:
    """Infer minimum lane progression from project artifact files.

    Mapping rules:
      - ``*.design.md`` => at least ``Design``
      - ``*.test.md``   => at least ``In Sprint``
            - ``*.exec.md`` or ``*.ql.md`` => at least ``Review``

    Returns:
        dict[str, str]: Project ID to inferred lane.

    """
    project_docs_root = _PROJECT_ROOT / "docs" / "project"
    hints: dict[str, str] = {}
    if not project_docs_root.exists():
        return hints

    for stage_dir in project_docs_root.iterdir():
        if not stage_dir.is_dir():
            continue
        match = _PROJECT_STAGE_DIR_RE.match(stage_dir.name)
        if match is None:
            continue

        project_id = match.group(1).lower()
        inferred_lane: str | None = None

        has_design = any(stage_dir.glob("*.design.md"))
        has_test = any(stage_dir.glob("*.test.md"))
        has_review = any(stage_dir.glob("*.exec.md")) or any(stage_dir.glob("*.ql.md"))

        if has_review:
            inferred_lane = "Review"
        elif has_test:
            inferred_lane = "In Sprint"
        elif has_design:
            inferred_lane = "Design"

        if inferred_lane is None:
            continue

        existing = hints.get(project_id)
        if existing is None:
            hints[project_id] = inferred_lane
            continue

        if _LANE_RANK[inferred_lane.lower()] > _LANE_RANK[existing.lower()]:
            hints[project_id] = inferred_lane

    return hints


def _sync_project_lanes_from_stage_artifacts() -> bool:
    """Auto-advance project lanes using agent stage artifacts.

    Returns:
        bool: True if any project lane changed.

    """
    hints = _build_stage_hint_map()
    if not hints:
        return False

    changed = False
    for i, entry in enumerate(_PROJECTS):
        project_id = str(entry.get("id", "")).lower().strip()
        if not project_id:
            continue

        hinted_lane = hints.get(project_id)
        if hinted_lane is None:
            continue

        current_lane = str(entry.get("lane", "Ideas")).strip()
        current_rank = _LANE_RANK.get(current_lane.lower(), 0)
        hinted_rank = _LANE_RANK.get(hinted_lane.lower(), 0)

        if hinted_rank <= current_rank:
            continue

        _PROJECTS[i] = {
            **entry,
            "lane": _canonical_lane_name(hinted_lane),
            "updated": datetime.now(timezone.utc).date().isoformat(),
        }
        changed = True

    if changed:
        _save_projects()
    return changed


def _save_projects() -> None:
    """Persist _PROJECTS to disk atomically."""
    tmp = _PROJECTS_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(_PROJECTS, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(_PROJECTS_FILE)


@_auth_router.get("/projects", response_model=list[ProjectModel])
async def get_projects(lane: _Opt[str] = None) -> list[ProjectModel]:
    """Return all projects from data/projects.json, optionally filtered by lane."""
    if not _PROJECTS and not _PROJECTS_FILE.exists():
        raise HTTPException(status_code=500, detail="data/projects.json not found")

    # Keep project lane progression in sync with generated stage artifacts.
    _sync_project_lanes_from_stage_artifacts()

    valid = _projects_valid()
    if lane:
        return [p for p in valid if p.lane == lane]
    return valid


@_auth_router.get("/ideas", response_model=list[IdeaModel])
async def get_ideas(
    implemented: str = "false",
    implemented_mode: str = "active_or_released",
    q: str = "",
    sort: str = "rank",
    order: str = "asc",
) -> list[IdeaModel]:
    """Return idea records parsed from docs/project/ideas.

    Args:
        implemented: Filter selector (supports false/true and exclude/include/only).
        implemented_mode: Implemented lane mode (active_or_released or released_only).
        q: Optional case-insensitive substring match over idea_id, title, summary, and source_path.
        sort: Sort field; rank is the default.
        order: Sort order; asc is the default.

    Returns:
        list[IdeaModel]: Filtered and sorted idea rows.

    """
    mode = implemented_mode.strip().lower() or "active_or_released"
    ideas = _load_ideas(mode=mode)

    selector = _implemented_selector(implemented)
    if selector == "exclude":
        ideas = [idea for idea in ideas if not idea.implemented]
    elif selector == "only":
        ideas = [idea for idea in ideas if idea.implemented]

    needle = q.strip().lower()
    if needle:
        ideas = [
            idea for idea in ideas
            if needle in idea.idea_id.lower()
            or needle in idea.title.lower()
            or needle in idea.summary.lower()
            or needle in idea.source_path.lower()
        ]

    normalized_sort = sort.strip().lower()
    normalized_order = order.strip().lower()
    if normalized_sort == "idea_id":
        ideas = sorted(ideas, key=lambda item: item.idea_id, reverse=(normalized_order == "desc"))
    elif normalized_sort == "priority":
        ideas = sorted(
            ideas,
            key=lambda item: (
                _priority_sort_rank(item),
                item.rank if item.rank is not None else 10_000_000,
                item.idea_id,
            ),
            reverse=(normalized_order == "desc"),
        )
    else:
        desc = normalized_order == "desc"
        ideas = sorted(
            ideas,
            key=lambda item: (
                -(item.rank if item.rank is not None else 10_000_000) if desc
                else (item.rank if item.rank is not None else 10_000_000),
                item.idea_id,
            ),
        )

    return ideas


class IdeaPatch(BaseModel):
    """Editable fields for one idea markdown file."""

    title: _Opt[str] = None
    summary: _Opt[str] = None
    mapped_project_ids: _Opt[list[str]] = None
    ensure_swot_risk_data: bool = False


@_auth_router.patch("/ideas/{idea_id}", response_model=IdeaModel)
async def patch_idea(idea_id: str, patch: IdeaPatch) -> IdeaModel:
    """Patch one idea markdown document and return the parsed idea row."""
    path = _idea_path_from_id(idea_id)
    if path is None:
        raise HTTPException(status_code=404, detail=f"Idea {idea_id!r} not found")

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise HTTPException(status_code=500, detail=f"Failed to read idea file: {exc}") from exc

    lines = text.splitlines()

    if patch.title is not None:
        title = patch.title.strip()
        if not title:
            raise HTTPException(status_code=400, detail="title cannot be empty")
        lines = _replace_first_heading(lines, title)

    if patch.summary is not None:
        summary = patch.summary.strip()
        if not summary:
            raise HTTPException(status_code=400, detail="summary cannot be empty")
        lines = _replace_idea_summary(lines, summary)

    if patch.mapped_project_ids is not None:
        normalized_ids: list[str] = []
        seen: set[str] = set()
        for raw_project_id in patch.mapped_project_ids:
            project_id = raw_project_id.strip().lower()
            if not project_id:
                continue
            if not _PROJECT_ID_RE.match(project_id):
                raise HTTPException(status_code=400, detail=f"Invalid project id: {project_id!r}")
            if project_id in seen:
                continue
            seen.add(project_id)
            normalized_ids.append(project_id)
        lines = _replace_mapping_line(lines, normalized_ids)

    if patch.ensure_swot_risk_data:
        default_swot = "Strength: pending analysis; Weakness: pending analysis; Opportunity: pending analysis; Threat: pending analysis."
        default_risk = "Risk: pending analysis; Likelihood: M; Impact: M; Mitigation: define owner and controls."
        lines = _ensure_section_content(lines, "## SWOT Data", default_swot)
        lines = _ensure_section_content(lines, "## Risk Data", default_risk)

    new_text = "\n".join(lines)
    if text.endswith("\n"):
        new_text += "\n"

    try:
        path.write_text(new_text, encoding="utf-8")
    except OSError as exc:
        raise HTTPException(status_code=500, detail=f"Failed to save idea file: {exc}") from exc

    parsed = _parse_idea_file(path, _load_project_lane_map(), mode="active_or_released")
    if parsed is None:
        raise HTTPException(status_code=500, detail="Idea parse failed after update")
    return parsed


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


@_auth_router.patch("/projects/{project_id}", response_model=ProjectModel)
async def patch_project(project_id: str, patch: ProjectPatch) -> ProjectModel:
    """Update one or more fields on an existing project and persist to disk."""
    if not _PROJECT_ID_RE.match(project_id):
        raise HTTPException(status_code=400, detail="Invalid project_id format")
    for i, entry in enumerate(_PROJECTS):
        if entry.get("id") == project_id:
            updates = {k: v for k, v in patch.model_dump().items() if v is not None}
            _PROJECTS[i] = {**entry, **updates}
            _save_projects()
            return ProjectModel(**_PROJECTS[i])
    raise HTTPException(status_code=404, detail=f"Project {project_id!r} not found")


class ProjectCreate(ProjectModel):
    """Full project payload required to create a new entry."""


@_auth_router.post("/projects", response_model=ProjectModel, status_code=201)
async def create_project(body: ProjectCreate) -> ProjectModel:
    """Append a new project entry and persist to disk."""
    if not _PROJECT_ID_RE.match(body.id):
        raise HTTPException(status_code=400, detail="Invalid project_id format")
    if any(e.get("id") == body.id for e in _PROJECTS):
        raise HTTPException(status_code=409, detail=f"Project {body.id!r} already exists")
    _PROJECTS.append(body.model_dump())
    _save_projects()
    return body


@_auth_router.get("/watchdog/status")
async def watchdog_status() -> dict:
    """Return the current AgentWatchdog state (DLQ size, retry counts, config)."""
    return watchdog.status()


# ── Pipeline execution endpoints ─────────────────────────────────────────────

_pipelines: dict = {}

_PIPELINE_STAGES = [
    "0master", "1project", "2think", "3design", "4plan",
    "5test", "6code", "7exec", "8ql", "9git",
]


class PipelineRunRequest(BaseModel):
    """Request body for POST /api/pipeline/run."""

    task: str = ""


@_auth_router.post("/pipeline/run")
async def run_pipeline(body: PipelineRunRequest) -> dict:
    """Create a new pipeline run and return its ID."""
    pipeline_id = str(uuid.uuid4())
    _pipelines[pipeline_id] = {
        "id": pipeline_id,
        "task": body.task,
        "status": "running",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "stages": {
            stage: {"status": "pending", "log": ""}
            for stage in _PIPELINE_STAGES
        },
    }
    return {"pipeline_id": pipeline_id, "status": "running"}


@_auth_router.get("/pipeline/status/{pipeline_id}")
async def pipeline_status(pipeline_id: str) -> dict:
    """Return the current status of a pipeline run."""
    pipeline = _pipelines.get(pipeline_id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline


# ── Agent memory endpoints ────────────────────────────────────────────────────

class MemoryEntryRequest(BaseModel):
    """Request body for the agent-memory append endpoint."""

    role: str  # "user" | "assistant" | "system"
    content: str
    session_id: _Opt[str] = None


@_auth_router.get("/agent-memory/{agent_id}")
async def read_agent_memory(
    agent_id: str,
    limit: _Opt[int] = None,
) -> list[dict]:
    """Return stored memory entries for *agent_id*, newest-first."""
    try:
        entries = await memory_store.read(agent_id, limit=limit)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return entries


@_auth_router.post("/agent-memory/{agent_id}", status_code=201)
async def append_agent_memory(
    agent_id: str,
    body: MemoryEntryRequest,
) -> dict:
    """Append a memory entry for *agent_id* and return the stored entry."""
    try:
        stored = await memory_store.append(
            agent_id,
            {"role": body.role, "content": body.content, "session_id": body.session_id},
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return stored


@_auth_router.delete("/agent-memory/{agent_id}", status_code=204)
async def clear_agent_memory(agent_id: str) -> None:
    """Clear all memory entries for *agent_id*."""
    try:
        await memory_store.clear(agent_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


app.include_router(_auth_router, prefix="/api")
app.include_router(_auth_router, prefix="/api/v1")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """WebSocket endpoint for real-time communication with E2E encryption.

    After authentication a one-round X25519 ECDH handshake is performed:
      1. Server sends its ephemeral public key (base64 text frame).
      2. Client sends its ephemeral public key (base64 text frame).
      3. Both sides independently derive the 32-byte AES-256 session key.
    All subsequent messages are encrypted with AES-256-GCM.
    """
    import base64
    from cryptography.exceptions import InvalidTag

    await websocket.accept()
    auth = await websocket_auth(websocket)
    if auth is None:
        return  # websocket_auth already closed the connection with 4401

    # ── E2E key exchange ─────────────────────────────────────────────────────
    server_priv, server_pub = generate_keypair()
    await websocket.send_text(base64.b64encode(server_pub).decode())

    try:
        client_pub_b64 = await websocket.receive_text()
        client_pub = base64.b64decode(client_pub_b64)
    except Exception:
        await websocket.close(code=1011)
        return

    session_key = derive_shared_secret(server_priv, client_pub)

    # Wrap websocket.send_text to transparently encrypt all outgoing messages.
    # ws_handler.py calls websocket.send_text directly, so wrapping here avoids
    # modifying the handler or any sub-handler.
    _original_send_text = websocket.send_text

    async def _encrypted_send(text: str) -> None:
        payload = base64.b64encode(encrypt_message(session_key, text.encode("utf-8"))).decode()
        await _original_send_text(payload)

    websocket.send_text = _encrypted_send  # type: ignore[method-assign]
    # ─────────────────────────────────────────────────────────────────────────

    session_id = await sessions.connect(websocket)
    logger.info("WebSocket connected (E2E): %s (auth=%s)", session_id, auth.get("auth"))
    try:
        while True:
            raw_b64 = await websocket.receive_text()
            try:
                raw = decrypt_message(session_key, base64.b64decode(raw_b64)).decode("utf-8")
            except (InvalidTag, ValueError, Exception) as exc:
                logger.warning("WebSocket decrypt failed for %s: %s", session_id, exc)
                await websocket.close(code=1011)
                sessions.disconnect(session_id)
                return

            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"type": "error", "error": "Invalid JSON"}))
                continue
            await handle_message(sessions, session_id, websocket, data)
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected: %s", session_id)
        sessions.disconnect(session_id)
