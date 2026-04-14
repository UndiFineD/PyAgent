# Code Structure Index

Domain index for `backend` paths.

Format: `## <file>` followed by `- line: code` entries.

## backend/__main__.py

- 15: import os
- 17: import uvicorn
- 19: from .app import app

## backend/auth.py

- 32: from __future__ import annotations
- 34: import hmac
- 35: import logging
- 36: import os
- 37: from typing import Any, Optional
- 39: import jwt
- 40: from fastapi import Header, HTTPException, WebSocket, status
- 42: _log = logging.getLogger(__name__)
- 48: API_KEY: str = os.getenv("PYAGENT_API_KEY", "")
- 49: JWT_SECRET: str = os.getenv("PYAGENT_JWT_SECRET", "")
- 50: JWT_ALGORITHM: str = "HS256"
- 53: DEV_MODE: bool = not API_KEY and not JWT_SECRET
- 67: def verify_api_key(expected: str, provided: Optional[str]) -> bool:
- 79: def verify_jwt(token: Optional[str]) -> Optional[dict[str, Any]]:
- 98: async def require_auth(
- 127: async def websocket_auth(websocket: WebSocket) -> Optional[dict[str, Any]]:

## backend/automem_benchmark_store.py

- 16: from __future__ import annotations
- 18: import datetime as dt
- 19: import json
- 20: import os
- 21: import uuid
- 22: from typing import Any
- 25: import asyncpg as _asyncpg  # type: ignore[import]
- 31: class AutoMemBenchmarkStore:
- 34: def __init__(self, dsn: str \| None = None) -> None:
- 39: def _decode_json_value(value: Any) -> Any:
- 46: def _is_tolerable_extension_error(exc: BaseException) -> bool:
- 66: async def _ensure_pool(self) -> Any:
- 68: raise RuntimeError("asyncpg is required for AutoMem benchmark persistence")
- 75: async def _ensure_schema(self) -> None:
- 101: ON automem_benchmark_runs(created_at DESC)
- 105: async def _bootstrap_minimal_benchmark_schema(self) -> None:
- 184: FOREIGN KEY (agent_id) REFERENCES automem_agents(agent_id)
- 193: ON memories(agent_id)
- 199: ON memories(importance DESC)
- 205: ON memories(created_at DESC)
- 211: ON memories(access_count DESC)
- 233: async def _benchmark_schema_missing_objects(self) -> list[str]:
- 278: SELECT format_type(a.atttypid, a.atttypmod)
- 293: SELECT format_type(a.atttypid, a.atttypmod)
- 307: async def save_report(self, payload: dict[str, Any]) -> dict[str, Any]:
- 312: raise RuntimeError("Benchmark payload missing run_id")
- 325: ON CONFLICT (run_id)
- 340: ON CONFLICT (key)
- 347: async def latest_report(self) -> dict[str, Any] \| None:
- 356: raise RuntimeError("Invalid benchmark_latest payload shape in automem_kv")
- 371: raise RuntimeError("Invalid benchmark payload shape in automem_benchmark_runs")
- 373: async def get_run(self, run_id: str) -> dict[str, Any] \| None:
- 377: raise ValueError("run_id must not be blank")
- 394: raise RuntimeError("Invalid benchmark payload shape in automem_benchmark_runs")
- 396: async def list_runs(self, limit: int = 20) -> list[dict[str, Any]]:
- 416: raise RuntimeError("Invalid benchmark payload shape in automem_benchmark_runs")
- 419: async def kv_get(self, key: str) -> Any \| None:
- 423: raise ValueError("key must not be blank")
- 439: async def kv_set(self, key: str, value: Any) -> Any:
- 443: raise ValueError("key must not be blank")
- 451: ON CONFLICT (key)
- 459: async def kv_delete(self, key: str) -> bool:
- 463: raise ValueError("key must not be blank")
- 470: async def run_benchmark(
- 499: raise ValueError(f"Unsupported benchmark backends: {invalid}")
- 501: from src.core.memory.BenchmarkRunner import BenchmarkRunner
- 563: automem_benchmark_store = AutoMemBenchmarkStore()

## backend/logging_config.py

- 15: from __future__ import annotations
- 17: import logging
- 19: from pythonjsonlogger.json import JsonFormatter
- 22: def setup_logging(level: str = "INFO") -> logging.Logger:
- 43: def get_logger(name: str = "pyagent.backend") -> logging.Logger:

## backend/memory_store.py

- 24: from __future__ import annotations
- 26: import asyncio
- 27: import json
- 28: import re
- 29: import uuid
- 30: from collections import defaultdict
- 31: from datetime import datetime, timezone
- 32: from pathlib import Path
- 33: from typing import Optional
- 39: _PROJECT_ROOT = Path(__file__).resolve().parent.parent
- 40: _AGENTS_DATA_DIR = _PROJECT_ROOT / "data" / "agents"
- 43: _AGENT_ID_RE = re.compile(r"^[a-zA-Z0-9_-]+$")
- 46: def _memory_path(agent_id: str) -> Path:
- 52: raise ValueError(f"Invalid agent_id ? only [a-zA-Z0-9_-] are allowed: {agent_id!r}")
- 61: class MemoryStore:
- 64: def __init__(self) -> None:
- 72: def _lock_for(self, agent_id: str) -> asyncio.Lock:
- 75: def _read_raw(self, path: Path) -> list[dict]:
- 83: def _write_raw(self, path: Path, entries: list[dict]) -> None:
- 91: async def append(self, agent_id: str, entry: dict) -> dict:
- 111: async def read(self, agent_id: str, limit: Optional[int] = None) -> list[dict]:
- 125: async def clear(self, agent_id: str) -> None:
- 133: memory_store = MemoryStore()

## backend/models.py

- 15: from __future__ import annotations
- 17: from typing import Any, Literal, Optional
- 19: from pydantic import BaseModel, Field
- 24: class InitMessage(BaseModel):
- 32: class RunTaskMessage(BaseModel):
- 41: class ControlMessage(BaseModel):
- 49: class SpeechTranscriptMessage(BaseModel):
- 59: class SignalMessage(BaseModel):
- 71: class TaskStartedMessage(BaseModel):
- 79: class TaskDeltaMessage(BaseModel):
- 88: class TaskCompleteMessage(BaseModel):
- 97: class TaskErrorMessage(BaseModel):
- 106: class ActionRequestMessage(BaseModel):

## backend/rate_limiter.py

- 15: from __future__ import annotations
- 17: import asyncio
- 18: import os
- 19: import time
- 20: from typing import Callable
- 22: from fastapi import Request, Response
- 23: from fastapi.responses import JSONResponse
- 24: from starlette.middleware.base import BaseHTTPMiddleware
- 25: from starlette.types import ASGIApp
- 27: _RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))
- 28: _RATE_LIMIT_WINDOW: float = float(os.getenv("RATE_LIMIT_WINDOW", "60"))
- 31: _EXEMPT_PATHS: frozenset[str] = frozenset({
- 41: class TokenBucket:
- 49: def __init__(self, rate: int, window: float) -> None:
- 57: async def consume(self) -> bool:
- 70: class RateLimitMiddleware(BaseHTTPMiddleware):
- 79: def __init__(self, app: ASGIApp, rate: int = _RATE_LIMIT_REQUESTS,
- 88: def _client_ip(self, request: Request) -> str:
- 97: async def _get_bucket(self, ip: str) -> TokenBucket:
- 104: async def dispatch(self, request: Request, call_next: Callable) -> Response:

## backend/session_manager.py

- 15: from __future__ import annotations
- 17: import uuid
- 19: from fastapi import WebSocket
- 22: class SessionManager:
- 25: def __init__(self) -> None:
- 28: async def connect(self, websocket: WebSocket) -> str:
- 33: def disconnect(self, session_id: str) -> None:
- 36: def get(self, session_id: str) -> WebSocket \| None:
- 39: def all_sessions(self) -> dict[str, WebSocket]:

## backend/tracing.py

- 15: from __future__ import annotations
- 17: from opentelemetry import trace
- 18: from opentelemetry.sdk.trace import TracerProvider
- 19: from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter, SpanExporter
- 21: _TRACER_NAME = "pyagent.backend"
- 24: def setup_tracing(exporter: SpanExporter \| None = None) -> trace.Tracer:
- 41: tracer: trace.Tracer = setup_tracing()

## backend/watchdog.py

- 16: from __future__ import annotations
- 18: import asyncio
- 19: import time
- 20: from collections import defaultdict
- 21: from typing import Any
- 24: class AgentWatchdog:
- 31: def __init__(self, timeout_s: float = 30.0, max_retries: int = 3) -> None:
- 37: async def run(self, agent_id: str, coro: Any) -> dict:
- 65: def status(self) -> dict:
- 75: def dead_letter_queue(self) -> list[dict]:
- 81: watchdog = AgentWatchdog()

## backend/ws_crypto.py

- 15: from __future__ import annotations
- 17: import os
- 19: from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
- 20: from cryptography.hazmat.primitives.ciphers.aead import AESGCM
- 21: from cryptography.hazmat.primitives.serialization import (
- 29: def generate_keypair() -> tuple[bytes, bytes]:
- 48: def derive_shared_secret(private_key_bytes: bytes, peer_public_key_bytes: bytes) -> bytes:
- 58: from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey
- 65: def encrypt_message(key: bytes, plaintext: bytes) -> bytes:
- 83: def decrypt_message(key: bytes, ciphertext: bytes) -> bytes:
- 99: raise ValueError("Ciphertext too short ? nonce missing")

## backend/ws_handler.py

- 15: from __future__ import annotations
- 17: import asyncio
- 18: import json
- 19: import logging
- 20: import re
- 21: from datetime import datetime, timezone
- 22: from typing import Any
- 24: from fastapi import WebSocket
- 26: from .models import (
- 31: from .session_manager import SessionManager
- 33: logger = logging.getLogger(__name__)
- 36: def _build_task_text(data: dict[str, Any]) -> str:
- 63: def _iter_text_chunks(text: str) -> list[str]:
- 77: async def handle_message(
- 91: await _handle_run_task(websocket, data)
- 93: await _handle_control(websocket, data)
- 95: await _handle_speech(websocket, data)
- 97: await _handle_signal(sessions, session_id, data)
- 105: async def _handle_run_task(websocket: WebSocket, data: dict[str, Any]) -> None:
- 137: async def _handle_control(websocket: WebSocket, data: dict[str, Any]) -> None:
- 146: async def _handle_speech(websocket: WebSocket, data: dict[str, Any]) -> None:
- 157: async def _handle_signal(

## backend/app.py

- 15: from __future__ import annotations
- 17: import json
- 18: import logging
- 19: import os
- 20: import random
- 21: import time
- 22: import uuid
- 23: from datetime import date, datetime, timezone
- 24: from pathlib import Path
- 25: from typing import Any
- 27: import psutil
- 28: from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
- 29: from fastapi.middleware.cors import CORSMiddleware
- 30: from fastapi.responses import JSONResponse
- 31: from pydantic import BaseModel
- 32: from starlette.middleware.base import BaseHTTPMiddleware
- 34: from .auth import require_auth, websocket_auth
- 35: from .automem_benchmark_store import automem_benchmark_store
- 36: from .memory_store import memory_store
- 37: from .rate_limiter import RateLimitMiddleware
- 38: from .logging_config import get_logger, setup_logging
- 39: from .session_manager import SessionManager
- 40: from .tracing import tracer  # noqa: F401 — initialises OTel TracerProvider on import
- 41: from .watchdog import watchdog
- 42: from .ws_crypto import decrypt_message, derive_shared_secret, encrypt_message, generate_keypair
- 43: from .ws_handler import handle_message
- 56: def _filter_iface(name: str) -> bool:
- 71: def _load_projects() -> list[dict]:
- 92: def _log_path(agent_id: str) -> Path:
- 100: def _legacy_log_path(agent_id: str) -> Path:
- 107: def _resolve_log_read_path(agent_id: str) -> Path:
- 137: class CorrelationIdMiddleware(BaseHTTPMiddleware):
- 140: async def dispatch(self, request, call_next):  # type: ignore[override]
- 159: class VersionHeaderMiddleware(BaseHTTPMiddleware):
- 166: async def dispatch(self, request, call_next):  # type: ignore[override]
- 194: async def health() -> dict[str, str]:
- 202: async def livez() -> dict[str, str]:
- 210: async def readyz() -> dict[str, Any]:
- 231: async def flm_metrics() -> dict:
- 255: PLUGIN_REGISTRY = [
- 305: async def list_plugins() -> dict:
- 312: class NetworkInterface(BaseModel):
- 320: class MemoryMetrics(BaseModel):
- 328: class DiskMetrics(BaseModel):
- 335: class SystemMetricsResponse(BaseModel):
- 345: class AutoMemBenchmarkRunRequest(BaseModel):
- 353: class AutoMemKvWriteRequest(BaseModel):
- 360: async def get_system_metrics() -> SystemMetricsResponse:
- 414: async def automem_benchmark_latest() -> dict[str, Any]:
- 429: async def automem_benchmark_run(body: AutoMemBenchmarkRunRequest) -> dict[str, Any]:
- 444: async def automem_benchmark_runs(
- 457: async def automem_benchmark_run_by_id(run_id: str) -> dict[str, Any]:
- 472: async def automem_kv_get(key: str) -> dict[str, Any]:
- 487: async def automem_kv_set(key: str, body: AutoMemKvWriteRequest) -> dict[str, Any]:
- 499: async def automem_kv_delete(key: str) -> dict[str, Any]:
- 510: class AgentLogBody(BaseModel):
- 517: async def read_agent_log(agent_id: str) -> dict[str, str]:
- 526: async def write_agent_log(agent_id: str, body: AgentLogBody) -> dict[str, str]:
- 537: class AgentDocBody(BaseModel):
- 544: async def read_agent_doc(agent_id: str) -> dict[str, str]:
- 555: async def write_agent_doc(agent_id: str, body: AgentDocBody) -> dict[str, str]:
- 568: from typing import Literal, Optional as _Opt  # noqa: E402
- 575: class ProjectModel(BaseModel):
- 591: import re as _re  # noqa: E402
- 602: class IdeaModel(BaseModel):
- 629: def _load_project_lane_map() -> dict[str, str]:
- 653: def _implemented_lanes_for_mode(mode: str) -> set[str]:
- 669: def _implemented_selector(implemented: str) -> str:
- 689: def _extract_mapped_project_ids(text: str) -> list[str]:
- 720: def _extract_title_summary(text: str, default_title: str) -> tuple[str, str]:
- 774: def _parse_idea_file(path: Path, lane_map: dict[str, str], mode: str) -> _Opt[IdeaModel]:
- 823: def _load_ideas(mode: str) -> list[IdeaModel]:
- 845: def _idea_path_from_id(idea_id: str) -> _Opt[Path]:
- 865: def _replace_first_heading(lines: list[str], title: str) -> list[str]:
- 877: def _replace_idea_summary(lines: list[str], summary: str) -> list[str]:
- 895: def _replace_mapping_line(lines: list[str], mapped_project_ids: list[str]) -> list[str]:
- 911: def _ensure_section_content(lines: list[str], heading: str, default_content: str) -> list[str]:
- 934: def _priority_sort_rank(idea: IdeaModel) -> int:
- 959: def _projects_valid() -> list[ProjectModel]:
- 981: def _canonical_lane_name(lane: str) -> str:
- 996: def _build_stage_hint_map() -> dict[str, str]:
- 1048: def _sync_project_lanes_from_stage_artifacts() -> bool:
- 1088: def _save_projects() -> None:
- 1096: async def get_projects(lane: _Opt[str] = None) -> list[ProjectModel]:
- 1111: async def get_ideas(
- 1178: class IdeaPatch(BaseModel):
- 1188: async def patch_idea(idea_id: str, patch: IdeaPatch) -> IdeaModel:
- 1249: class ProjectPatch(BaseModel):
- 1264: async def patch_project(project_id: str, patch: ProjectPatch) -> ProjectModel:
- 1277: class ProjectCreate(ProjectModel):
- 1282: async def create_project(body: ProjectCreate) -> ProjectModel:
- 1294: async def watchdog_status() -> dict:
- 1309: class PipelineRunRequest(BaseModel):
- 1316: async def run_pipeline(body: PipelineRunRequest) -> dict:
- 1333: async def pipeline_status(pipeline_id: str) -> dict:
- 1343: class MemoryEntryRequest(BaseModel):
- 1352: async def read_agent_memory(
- 1365: async def append_agent_memory(
- 1381: async def clear_agent_memory(agent_id: str) -> None:
- 1395: async def websocket_endpoint(websocket: WebSocket) -> None:
- 1404: import base64
- 1405: from cryptography.exceptions import InvalidTag
- 1430: async def _encrypted_send(text: str) -> None:
