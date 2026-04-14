# Code Structure Index

Domain index for `src` paths.

Format: `## <file>` followed by `- line: code` entries.

## src/MemoryTransactionManager.py

- 20: from src.transactions.MemoryTransactionManager import MemoryTransaction, validate  # noqa: F401
- 22: __all__ = ["MemoryTransaction", "validate"]

## src/__init__.py

- 17: __all__ = ["core"]

## src/agents/BaseAgent.py

- 30: from __future__ import annotations
- 32: import asyncio
- 33: import logging
- 34: import uuid
- 35: from abc import ABC, abstractmethod
- 36: from dataclasses import dataclass, field
- 37: from enum import Enum, auto
- 38: from typing import Any
- 40: logger = logging.getLogger(__name__)
- 43: class AgentLifecycle(Enum):
- 52: class AgentManifest:
- 78: class BaseAgent(ABC):
- 91: def __init__(
- 107: def manifest(self) -> AgentManifest:
- 112: def agent_id(self) -> str:
- 117: def state(self) -> AgentLifecycle:
- 125: def start(self) -> None:
- 139: def stop(self) -> None:
- 146: def reset(self) -> None:
- 165: async def run(self, task: dict[str, Any]) -> dict[str, Any]:
- 184: async def dispatch(self, task: dict[str, Any]) -> dict[str, Any]:
- 206: def validate(cls) -> bool:
- 210: def __repr__(self) -> str:

## src/agents/__init__.py

- 22: from __future__ import annotations
- 24: from src.agents.BaseAgent import AgentLifecycle, AgentManifest, BaseAgent
- 26: __all__ = ["BaseAgent", "AgentLifecycle", "AgentManifest"]

## src/benchmarks/simple.py

- 17: def run() -> dict[str, float]:

## src/chat/api.py

- 16: from __future__ import annotations
- 18: from typing import Any
- 20: from fastapi import FastAPI, HTTPException
- 21: from pydantic import BaseModel
- 23: from chat.models import ChatRoom
- 24: from MemoryTransactionManager import MemoryTransaction  # ensure atomic updates
- 27: from prometheus_client import Counter
- 30: class _CounterValue:
- 33: def __init__(self) -> None:
- 37: def set(self, value: int) -> None:
- 41: def get(self) -> int:
- 45: class Counter:
- 48: def __init__(self, _name: str, _documentation: str) -> None:
- 52: def inc(self) -> None:
- 57: app = FastAPI()
- 60: rooms: dict[str, ChatRoom] = {}
- 63: messages_counter = Counter("chat_messages_total", "Total number of messages posted to chat rooms")
- 66: class RoomCreateRequest(BaseModel):
- 73: class MessageRequest(BaseModel):
- 81: def create_room(request: RoomCreateRequest) -> dict[str, str]:
- 86: raise HTTPException(status_code=400, detail="room already exists")
- 92: def post_message(room_name: str, request: MessageRequest) -> dict[str, str]:
- 98: raise HTTPException(status_code=404, detail="room not found")
- 106: def get_history(room_name: str) -> list[dict[str, Any]]:
- 110: raise HTTPException(status_code=404, detail="room not found")

## src/chat/mcp_tools.py

- 15: from __future__ import annotations
- 17: from typing import Any
- 19: import httpx
- 26: def send_chat_message(room: str, sender: str, text: str) -> Any:
- 40: send_message_tool = send_chat_message

## src/chat/models.py

- 15: from __future__ import annotations
- 17: from typing import Any, Optional
- 20: class ChatRoom:
- 28: def __init__(self, name: str, participants: Optional[list[str]] = None) -> None:
- 35: def post(self, sender: str, text: str) -> None:
- 40: def history(self) -> list[dict[str, Any]]:

## src/chat/streaming.py

- 22: from __future__ import annotations
- 24: import asyncio
- 25: import json
- 26: from collections.abc import AsyncGenerator, AsyncIterator
- 27: from typing import Any
- 34: async def word_chunks(text: str, delay: float = 0.0) -> AsyncGenerator[str, None]:
- 56: async def collect(stream: AsyncIterator[str]) -> str:
- 69: def _sse_event(data: str, event: str \| None = None, id: str \| None = None) -> str:
- 93: async def stream_to_sse(
- 117: yield _sse_event(payload, event=event, id=str(idx))
- 119: yield _sse_event("[DONE]", event=done_event)
- 127: class StreamingChatSession:
- 140: def __init__(self, room_name: str) -> None:
- 150: def is_finished(self) -> bool:
- 155: def full_text(self) -> str:
- 163: async def stream(self, source: AsyncIterator[str]) -> AsyncGenerator[str, None]:
- 179: def clear(self) -> None:
- 184: def to_dict(self) -> dict[str, Any]:

## src/chat/utils.py

- 16: from __future__ import annotations
- 18: from chat.models import ChatRoom
- 21: def create_personal_room(human: str) -> ChatRoom:

## src/context_manager/__init__.py

- 16: from __future__ import annotations
- 19: class ContextManager:
- 22: def __init__(self, max_tokens: int):
- 27: async def push(self, text: str) -> None:
- 40: def snapshot(self) -> str:

## src/context_manager/window.py

- 22: from __future__ import annotations
- 24: import time
- 25: from dataclasses import dataclass, field
- 26: from typing import Any
- 30: class ContextSegment:
- 55: def token_count(self) -> int:
- 59: def to_dict(self) -> dict[str, Any]:
- 71: class ContextWindow:
- 85: def __init__(self, max_tokens: int) -> None:
- 94: def segments(self) -> list[ContextSegment]:
- 99: def token_count(self) -> int:
- 107: async def push(
- 147: def snapshot(self) -> str:
- 151: def clear(self) -> None:
- 155: def to_dict(self) -> dict[str, Any]:
- 167: async def _prune(self) -> None:

## src/core/ContextTransactionManager.py

- 17: from src.transactions.ContextTransactionManager import (  # noqa: F401
- 23: def validate() -> bool:
- 28: __all__ = ["ContextTransaction", "RecursionGuardError", "validate"]

## src/core/ProcessTransactionManager.py

- 17: from src.transactions.ProcessTransactionManager import ProcessTransaction  # noqa: F401
- 20: def validate() -> bool:
- 25: __all__ = ["ProcessTransaction", "validate"]

## src/core/StorageTransactionManager.py

- 17: from src.transactions.StorageTransactionManager import (  # noqa: F401
- 23: def validate() -> bool:
- 28: __all__ = ["StorageTransaction", "EncryptionConfigError", "validate"]

## src/core/UnifiedTransactionManager.py

- 17: from __future__ import annotations
- 19: from dataclasses import dataclass, field
- 20: from typing import Any
- 21: from uuid import uuid4
- 24: def validate() -> bool:
- 30: class TransactionEnvelope:
- 39: class OperationResult:
- 47: class UnifiedTransactionManager:
- 50: def __init__(self) -> None:
- 55: def begin(self, operations: list[dict[str, Any]]) -> str:
- 63: def execute(self, tx_id: str, fail_on_operation_id: str \| None = None) -> list[OperationResult]:
- 107: def commit(self, tx_id: str) -> bool:
- 112: def rollback(self, tx_id: str) -> bool:

## src/core/agent_registry.py

- 16: from __future__ import annotations
- 18: from dataclasses import dataclass
- 19: from typing import Any, Optional
- 23: class AgentRegistry:
- 28: def __post_init__(self) -> None:
- 33: def register(self, name: str, obj: Any) -> None:
- 38: def get(self, name: str) -> Optional[Any]:
- 44: def validate() -> None:

## src/core/agent_state_manager.py

- 17: from __future__ import annotations
- 19: from dataclasses import dataclass
- 20: from time import time
- 21: from typing import Any
- 25: class AgentState:
- 40: class AgentStateManager:
- 47: def __init__(self) -> None:
- 51: def upsert(self, agent_id: str, status: str, metadata: dict[str, Any] \| None = None) -> None:
- 66: raise ValueError("agent_id must not be blank")
- 68: raise ValueError("status must not be blank")
- 76: def get(self, agent_id: str) -> AgentState \| None:
- 88: def remove(self, agent_id: str) -> bool:
- 100: def count(self) -> int:
- 110: def validate() -> None:
- 122: raise RuntimeError("agent state upsert/get failed")
- 124: raise RuntimeError("agent state metadata roundtrip failed")
- 127: raise RuntimeError("agent count tracking failed")
- 130: raise RuntimeError("agent state removal failed")

## src/core/audit/AuditEvent.py

- 17: from __future__ import annotations
- 19: from dataclasses import dataclass
- 20: from typing import Any
- 22: from src.core.audit.exceptions import AuditSerializationError
- 24: AUDIT_SCHEMA_VERSION = 1
- 27: def _canonicalize_value(value: object) -> object:
- 48: class AuditEvent:
- 78: def to_canonical_dict(self) -> dict[str, object]:
- 108: def to_json_dict(self, previous_hash: str, event_hash: str, sequence: int) -> dict[str, object]:
- 127: def from_json_dict(cls, data: dict[str, object]) -> AuditEvent:
- 150: raise AuditSerializationError(f"Missing required key: {key}")
- 154: raise AuditSerializationError("Field 'payload' must be a dictionary.")
- 158: raise AuditSerializationError("Field 'schema_version' must be an integer.")
- 176: def validate() -> bool:
- 186: __all__ = ["AUDIT_SCHEMA_VERSION", "AuditEvent", "validate"]

## src/core/audit/AuditHasher.py

- 17: from __future__ import annotations
- 19: import hashlib
- 20: import json
- 21: import re
- 23: from src.core.audit.AuditEvent import AuditEvent
- 25: _HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")
- 28: class AuditHasher:
- 32: def canonical_event_bytes(event: AuditEvent) -> bytes:
- 47: def compute_event_hash(previous_hash: str, canonical_event_bytes: bytes) -> str:
- 65: def validate_hash_format(hash_value: str) -> bool:
- 78: def validate() -> bool:
- 88: __all__ = ["AuditHasher", "validate"]

## src/core/audit/AuditTrailCore.py

- 17: from __future__ import annotations
- 19: import json
- 20: from datetime import datetime, timezone
- 21: from pathlib import Path
- 22: from typing import Any
- 23: from uuid import uuid4
- 25: from src.core.audit.AuditEvent import AUDIT_SCHEMA_VERSION, AuditEvent
- 26: from src.core.audit.AuditHasher import AuditHasher
- 27: from src.core.audit.AuditVerificationResult import AuditVerificationResult
- 28: from src.core.audit.exceptions import (
- 35: GENESIS_PREVIOUS_HASH = "0" * 64
- 38: class AuditTrailCore:
- 41: def __init__(self, audit_file_path: str, *, fail_closed: bool = True) -> None:
- 54: def append_event(self, event: AuditEvent) -> str:
- 85: def append_event_dict(
- 135: def iter_records(self) -> list[dict[str, object]]:
- 158: raise AuditSerializationError("Audit record must decode to a JSON object.")
- 166: def verify_file(self) -> AuditVerificationResult:
- 301: def get_last_hash(self) -> str:
- 317: def get_last_sequence(self) -> int:
- 333: def _append_record(self, record: dict[str, object]) -> None:
- 353: def _invalid_result(
- 387: def validate() -> bool:
- 397: __all__ = ["GENESIS_PREVIOUS_HASH", "AuditTrailCore", "validate"]

## src/core/audit/AuditTrailMixin.py

- 17: from __future__ import annotations
- 19: from typing import TYPE_CHECKING
- 21: from src.core.audit.exceptions import AuditTrailError
- 24: from src.core.audit.AuditTrailCore import AuditTrailCore
- 27: class AuditTrailMixin:
- 30: def _get_audit_trail_core(self) -> AuditTrailCore \| None:
- 39: def audit_emit_event(
- 85: def audit_emit_success(self, action: str, payload: dict[str, object]) -> str \| None:
- 98: def audit_emit_failure(self, action: str, payload: dict[str, object]) -> str \| None:
- 112: def validate() -> bool:
- 122: __all__ = ["AuditTrailMixin", "validate"]

## src/core/audit/AuditVerificationResult.py

- 17: from dataclasses import dataclass
- 21: class AuditVerificationResult:
- 44: def validate() -> bool:
- 54: __all__ = ["AuditVerificationResult", "validate"]

## src/core/audit/__init__.py

- 17: from src.core.audit.AuditEvent import AUDIT_SCHEMA_VERSION, AuditEvent
- 18: from src.core.audit.AuditHasher import AuditHasher
- 19: from src.core.audit.AuditTrailCore import GENESIS_PREVIOUS_HASH, AuditTrailCore
- 20: from src.core.audit.AuditTrailMixin import AuditTrailMixin
- 21: from src.core.audit.AuditVerificationResult import AuditVerificationResult
- 22: from src.core.audit.exceptions import (
- 31: def validate() -> bool:
- 41: __all__ = [

## src/core/audit/exceptions.py

- 18: class AuditTrailError(Exception):
- 22: class AuditSerializationError(AuditTrailError):
- 26: class AuditChainLinkError(AuditTrailError):
- 30: class AuditIntegrityError(AuditTrailError):
- 34: class AuditPersistenceError(AuditTrailError):
- 38: def validate() -> bool:
- 48: __all__ = [

## src/core/base/__init__.py

- 18: def validate() -> bool:

## src/core/config.py

- 23: from __future__ import annotations
- 25: import json
- 26: import os
- 27: from dataclasses import asdict, dataclass, field
- 28: from pathlib import Path
- 29: from typing import Any
- 35: _DEFAULT_MAX_TOKENS = 4096
- 36: _DEFAULT_TIMEOUT = 30.0
- 37: _DEFAULT_LLM_MODEL = "flm-default"
- 41: class AgentConfig:
- 71: def __post_init__(self) -> None:
- 73: raise ValueError("AgentConfig.name must be a non-empty string")
- 75: raise ValueError(f"max_tokens must be positive, got {self.max_tokens}")
- 77: raise ValueError(f"timeout must be positive, got {self.timeout}")
- 79: raise ValueError("llm_model must be a non-empty string")
- 81: def to_dict(self) -> dict[str, Any]:
- 86: def from_dict(cls, data: dict[str, Any]) -> "AgentConfig":
- 104: _DEFAULT_SWARM_CONCURRENCY = 4
- 105: _DEFAULT_HEARTBEAT_INTERVAL = 5.0
- 109: class SwarmConfig:
- 135: def __post_init__(self) -> None:
- 137: raise ValueError(f"max_concurrency must be positive, got {self.max_concurrency}")
- 139: raise ValueError(f"heartbeat_interval must be positive, got {self.heartbeat_interval}")
- 141: raise ValueError(f"log_level must be one of {sorted(self._VALID_LOG_LEVELS)}, got {self.log_level!r}")
- 144: def add_agent(self, config: AgentConfig) -> None:
- 148: def remove_agent(self, name: str) -> AgentConfig \| None:
- 152: def get_agent(self, name: str) -> AgentConfig \| None:
- 156: def enabled_agents(self) -> list[AgentConfig]:
- 160: def to_dict(self) -> dict[str, Any]:
- 172: def from_dict(cls, data: dict[str, Any]) -> "SwarmConfig":
- 185: def load_config(path: str \| os.PathLike[str]) -> SwarmConfig:
- 203: raise FileNotFoundError(f"Config file not found: {p}")
- 211: def save_config(config: SwarmConfig, path: str \| os.PathLike[str]) -> None:
- 229: def validate() -> bool:

## src/core/crdt_bridge.py

- 15: from __future__ import annotations
- 17: import json
- 18: import subprocess
- 19: import sys
- 20: import tempfile
- 21: from pathlib import Path
- 24: def _rust_crdt_binary() -> Path:
- 38: def merge(left: dict, right: dict) -> dict:
- 64: def validate() -> None:

## src/core/fuzzing/FuzzCase.py

- 17: from __future__ import annotations
- 19: import hashlib
- 20: from dataclasses import dataclass
- 22: from .exceptions import FuzzConfigurationError
- 26: class FuzzCase:
- 46: def __post_init__(self) -> None:
- 50: def validate(self) -> None:
- 59: raise FuzzConfigurationError(msg)
- 62: raise FuzzConfigurationError(msg)
- 65: raise FuzzConfigurationError(msg)
- 68: raise FuzzConfigurationError(msg)
- 71: raise FuzzConfigurationError(msg)
- 74: def replay_key(self) -> str:

## src/core/fuzzing/FuzzCorpus.py

- 17: from __future__ import annotations
- 19: from .exceptions import FuzzConfigurationError
- 22: class FuzzCorpus:
- 25: def __init__(self, *, entries: list[str \| bytes]) -> None:
- 41: def validate(self) -> None:
- 50: raise FuzzConfigurationError(msg)
- 53: def size(self) -> int:
- 57: def get(self, index: int) -> bytes:
- 70: def _normalize_entry(entry: str \| bytes) -> bytes:
- 88: raise FuzzConfigurationError(msg)

## src/core/fuzzing/FuzzEngineCore.py

- 17: from __future__ import annotations
- 19: import hashlib
- 21: from .FuzzCase import FuzzCase
- 22: from .FuzzCorpus import FuzzCorpus
- 23: from .FuzzMutator import FuzzMutator
- 24: from .FuzzSafetyPolicy import FuzzSafetyPolicy
- 27: class FuzzEngineCore:
- 30: def __init__(
- 44: def validate(self) -> None:
- 50: def schedule_cases(self, *, target: str, operator: str, requested_cases: int) -> tuple[FuzzCase, ...]:
- 103: def _deterministic_case_id(

## src/core/fuzzing/FuzzMutator.py

- 17: from __future__ import annotations
- 19: import random
- 21: from .exceptions import UnknownMutationOperatorError
- 24: class FuzzMutator:
- 29: def __init__(self, *, seed: int) -> None:
- 38: def validate(self) -> None:
- 42: raise TypeError(msg)
- 44: def available_operators(self) -> tuple[str, ...]:
- 48: def mutate(self, *, payload: bytes, operator: str, corpus_index: int) -> bytes:
- 65: raise UnknownMutationOperatorError(msg)

## src/core/fuzzing/FuzzResult.py

- 17: from __future__ import annotations
- 19: from dataclasses import dataclass
- 21: from .exceptions import FuzzConfigurationError
- 22: from .FuzzCase import FuzzCase
- 26: class FuzzCaseResult:
- 44: def __post_init__(self) -> None:
- 48: def validate(self) -> None:
- 57: raise FuzzConfigurationError(msg)
- 60: raise FuzzConfigurationError(msg)
- 63: raise FuzzConfigurationError(msg)
- 67: class FuzzCampaignResult:
- 73: def validate(self) -> None:
- 85: raise FuzzConfigurationError(msg)
- 88: def from_case_results(cls, results: list[FuzzCaseResult]) -> "FuzzCampaignResult":

## src/core/fuzzing/FuzzSafetyPolicy.py

- 17: from __future__ import annotations
- 19: from urllib.parse import urlparse
- 21: from .exceptions import FuzzConfigurationError, FuzzPolicyViolation
- 24: class FuzzSafetyPolicy:
- 27: def __init__(
- 46: def validate(self) -> None:
- 55: raise FuzzConfigurationError(msg)
- 58: raise FuzzConfigurationError(msg)
- 61: raise FuzzConfigurationError(msg)
- 64: raise FuzzConfigurationError(msg)
- 67: raise FuzzConfigurationError(msg)
- 70: raise FuzzConfigurationError(msg)
- 72: def validate_target(self, target: str) -> None:
- 86: raise FuzzPolicyViolation(msg)
- 89: raise FuzzPolicyViolation(msg)
- 91: def validate_operator(self, operator: str) -> None:
- 103: raise FuzzPolicyViolation(msg)
- 105: def validate_payload(self, payload: bytes) -> None:
- 117: raise FuzzPolicyViolation(msg)
- 120: raise FuzzPolicyViolation(msg)
- 122: def enforce_budget(
- 142: raise FuzzPolicyViolation(msg)
- 145: raise FuzzPolicyViolation(msg)
- 148: raise FuzzPolicyViolation(msg)

## src/core/fuzzing/__init__.py

- 17: from .exceptions import FuzzConfigurationError, FuzzExecutionError, FuzzingError, FuzzPolicyViolation
- 18: from .FuzzCase import FuzzCase
- 19: from .FuzzCorpus import FuzzCorpus
- 20: from .FuzzEngineCore import FuzzEngineCore
- 21: from .FuzzMutator import FuzzMutator
- 22: from .FuzzResult import FuzzCampaignResult, FuzzCaseResult
- 23: from .FuzzSafetyPolicy import FuzzSafetyPolicy
- 25: __all__ = [

## src/core/fuzzing/exceptions.py

- 18: class FuzzingError(Exception):
- 22: class FuzzConfigurationError(FuzzingError):
- 26: class FuzzExecutionError(FuzzingError):
- 30: class FuzzPolicyViolation(FuzzingError):  # noqa: N818
- 34: class UnknownMutationOperatorError(FuzzConfigurationError):

## src/core/memory.py

- 16: from __future__ import annotations
- 18: from dataclasses import dataclass
- 19: from typing import Any, Optional
- 23: class MemoryStore:
- 28: def __post_init__(self) -> None:
- 33: def set(self, key: str, value: Any) -> None:
- 38: def get(self, key: str, default: Any = None) -> Any:
- 43: def delete(self, key: str) -> bool:
- 51: def keys(self) -> list[str]:
- 56: def __len__(self) -> int:
- 61: def validate() -> None:

## src/core/memory/AutoMemCore.py

- 16: from __future__ import annotations
- 18: import asyncio
- 19: import math
- 20: import uuid
- 21: from dataclasses import dataclass, field
- 22: from datetime import datetime, timezone
- 23: from typing import Any, Optional
- 29: import asyncpg  # type: ignore[import]
- 36: from pgvector.asyncpg import register_vector  # type: ignore[import]
- 46: WEIGHT_VECTOR: float = 0.25  # pgvector cosine similarity
- 47: WEIGHT_GRAPH: float = 0.25  # Apache AGE graph neighbourhood depth
- 48: WEIGHT_TEMPORAL: float = 0.15  # exponential decay since last access
- 49: WEIGHT_KEYWORD: float = 0.15  # exact keyword intersection ratio
- 50: WEIGHT_LEXICAL: float = 0.10  # tsvector / tsquery rank
- 51: WEIGHT_IMPORTANCE: float = 0.05  # stored importance value 0?1
- 52: WEIGHT_CONFIDENCE: float = 0.05  # stored confidence value 0?1
- 69: DECAY_K: float = 0.01
- 78: class Memory:
- 100: class MemoryResult:
- 112: def breakdown(self) -> dict[str, float]:
- 130: def _temporal_score(last_accessed: Optional[datetime]) -> float:
- 145: def _keyword_score(query_keywords: list[str], memory_keywords: list[str]) -> float:
- 154: def _cosine_distance_to_score(distance: float) -> float:
- 159: def _graph_hops_to_score(hops: int) -> float:
- 171: class AutoMemCore:
- 186: def __init__(self, dsn: str, embedding_dim: int = 1536) -> None:
- 203: async def connect(self) -> None:
- 206: raise ImportError("asyncpg is required ? pip install asyncpg pgvector")
- 214: async def _init_conn(self, conn: Any) -> None:
- 217: await register_vector(conn)
- 220: async def close(self) -> None:
- 226: async def __aenter__(self) -> "AutoMemCore":
- 230: async def __aexit__(self, *_: Any) -> None:
- 237: async def store(
- 256: raise RuntimeError("Call connect() or use async-with first")
- 354: async def get(self, memory_id: uuid.UUID) -> Optional[Memory]:
- 357: raise RuntimeError("Call connect() first")
- 379: async def hybrid_search(
- 396: raise RuntimeError("Call connect() first")
- 406: FROM automem_hybrid_candidates($1, $2, $3, $4, $5)
- 488: async def _graph_depths(self, agent_id: str, mem_ids: list[str]) -> dict[str, int]:
- 518: async def get_subtree(self, root_id: uuid.UUID, max_depth: int = 3) -> list[Memory]:
- 521: raise RuntimeError("Call connect() first")
- 547: async def top_by_frecency(self, agent_id: str, n: int = 20) -> list[Memory]:
- 553: raise RuntimeError("Call connect() first")
- 576: async def delete(self, memory_id: uuid.UUID) -> bool:
- 579: raise RuntimeError("Call connect() first")
- 589: def _row_to_memory(row: Any) -> Memory:
- 609: def validate() -> bool:

## src/core/memory/BenchmarkRunner.py

- 25: from __future__ import annotations
- 27: import asyncio
- 28: import datetime as _dt
- 29: import json
- 30: import math
- 31: import random
- 32: import string
- 33: import time
- 34: import uuid
- 35: from dataclasses import asdict, dataclass, field
- 36: from typing import Any, Optional
- 38: asyncpg: Any = None
- 40: import asyncpg as _asyncpg  # type: ignore[import]
- 52: def _metadata_factory() -> dict[str, Any]:
- 57: def _operation_results_factory() -> list["OperationResult"]:
- 62: def _errors_factory() -> list[str]:
- 68: class OperationResult:
- 82: class BenchmarkReport:
- 91: def to_json(self, indent: int = 2) -> str:
- 100: WORD_POOL = [
- 124: def _random_content(length: int = 120) -> str:
- 136: def _random_embedding(dim: int = 1536) -> list[float]:
- 143: def _random_keywords(n: int = 4) -> list[str]:
- 148: def _random_importance() -> float:
- 158: class BenchmarkRunner:
- 168: def __init__(
- 177: raise ValueError(f"Unsupported benchmark backend: {backend}")
- 179: raise ImportError("asyncpg required ? pip install asyncpg pgvector")
- 190: async def __aenter__(self) -> "BenchmarkRunner":
- 203: SELECT format_type(a.atttypid, a.atttypmod)
- 214: SELECT format_type(a.atttypid, a.atttypmod)
- 228: async def __aexit__(self, *_: Any) -> None:
- 233: def _append_result(
- 269: def _append_unavailable(self, operation: str, method: str, reason: str) -> None:
- 293: async def _bench_writes(self, n: int) -> list[uuid.UUID]:
- 349: async def _bench_read_btree(self, sample_ids: list[uuid.UUID]) -> None:
- 370: async def _bench_read_hash(self) -> None:
- 392: async def _bench_sort(self) -> None:
- 422: async def _bench_search_hnsw(self) -> None:
- 445: SELECT SUM(POWER(a - b, 2))
- 446: FROM unnest(embedding, $1::double precision[]) AS t(a, b)
- 476: async def _bench_search_gin_tsv(self) -> None:
- 504: async def _bench_search_gin_keywords(self) -> None:
- 531: async def _bench_search_brin(self) -> None:
- 556: async def _bench_search_seqscan(self) -> None:
- 580: async def _bench_search_ltree(self) -> None:
- 613: async def _run_memory(self, cleanup_after: bool) -> BenchmarkReport:
- 790: async def _cleanup(self) -> None:
- 799: async def run(self, cleanup_after: bool = True) -> BenchmarkReport:
- 842: async def _main() -> None:
- 843: import sys
- 856: def validate() -> bool:

## src/core/memory/__init__.py

- 16: from __future__ import annotations
- 18: from typing import Any
- 21: class MemoryStore:
- 24: def __init__(self) -> None:
- 28: def set(self, key: str, value: Any) -> None:
- 32: def get(self, key: str, default: Any \| None = None) -> Any:
- 37: def validate() -> None:
- 44: __all__ = ["MemoryStore", "validate"]

## src/core/n8nbridge/N8nBridgeConfig.py

- 17: from __future__ import annotations
- 19: from dataclasses import dataclass
- 20: from typing import Mapping
- 21: from urllib.parse import urlparse
- 23: from .exceptions import N8nBridgeConfigError
- 27: class N8nBridgeConfig:
- 54: def from_env(cls, env: Mapping[str, str]) -> "N8nBridgeConfig":
- 81: def validate(self) -> None:
- 90: raise N8nBridgeConfigError("N8N_BRIDGE_BASE_URL must be an absolute http(s) URL")
- 92: raise N8nBridgeConfigError("N8N_BRIDGE_REQUEST_TIMEOUT_SECONDS must be > 0")
- 94: raise N8nBridgeConfigError("N8N_BRIDGE_MAX_RETRIES must be >= 0")
- 96: raise N8nBridgeConfigError("N8N_BRIDGE_BACKOFF_SECONDS must be >= 0")
- 98: raise N8nBridgeConfigError("N8N_BRIDGE_IDEMPOTENCY_TTL_SECONDS must be > 0")
- 101: def _parse_bool(value: str) -> bool:

## src/core/n8nbridge/N8nBridgeCore.py

- 17: from __future__ import annotations
- 19: import time as _stdlib_time
- 20: import uuid
- 21: from datetime import datetime, timezone
- 22: from typing import Any
- 24: from .N8nBridgeConfig import N8nBridgeConfig
- 25: from .N8nEventAdapter import N8nEventAdapter
- 26: from .N8nHttpClient import N8nHttpClient
- 29: class _TimeProxy:
- 33: def monotonic() -> float:
- 43: time = _TimeProxy()
- 46: class N8nBridgeCore:
- 49: def __init__(self, config: N8nBridgeConfig, adapter: N8nEventAdapter, http_client: N8nHttpClient) -> None:
- 63: async def handle_inbound_event(self, raw_payload: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:
- 105: async def trigger_workflow(
- 184: def _is_duplicate_event(self, event_id: str) -> bool:
- 203: def _evict_expired(self, now: float) -> None:

## src/core/n8nbridge/N8nBridgeMixin.py

- 17: from __future__ import annotations
- 19: from typing import Any
- 22: class N8nBridgeMixin:
- 27: async def n8n_trigger(
- 54: async def n8n_handle_callback(self, raw_payload: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:

## src/core/n8nbridge/N8nEventAdapter.py

- 17: from __future__ import annotations
- 19: from typing import Any
- 21: from .exceptions import N8nBridgeValidationError
- 24: class N8nEventAdapter:
- 27: def to_inbound_event(self, raw_payload: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:
- 53: raise N8nBridgeValidationError(f"Missing inbound fields: {', '.join(missing)}")
- 57: raise N8nBridgeValidationError("Unable to determine correlation_id")
- 72: def to_n8n_trigger_payload(self, outbound_event: dict[str, Any]) -> dict[str, Any]:
- 97: raise N8nBridgeValidationError(f"Missing outbound fields: {', '.join(missing)}")
- 111: def _get_header(headers: dict[str, str], name: str) -> str \| None:

## src/core/n8nbridge/N8nHttpClient.py

- 17: from __future__ import annotations
- 19: import asyncio
- 20: import json
- 21: import time
- 22: import urllib.request
- 23: from typing import Any
- 24: from urllib.error import HTTPError, URLError
- 26: from .exceptions import N8nHttpClientError
- 27: from .N8nBridgeConfig import N8nBridgeConfig
- 30: class N8nHttpClient:
- 33: def __init__(self, config: N8nBridgeConfig) -> None:
- 42: async def post_json(
- 103: await _sleep_backoff(self._config.backoff_seconds)
- 109: await _sleep_backoff(self._config.backoff_seconds)
- 111: raise N8nHttpClientError("n8n post_json exhausted retries")
- 114: def _parse_json_bytes(raw: bytes) -> dict[str, Any]:
- 132: async def _sleep_backoff(delay_seconds: float) -> None:
- 144: def validate() -> None:

## src/core/n8nbridge/__init__.py

- 17: __all__ = [

## src/core/n8nbridge/exceptions.py

- 18: class N8nBridgeError(Exception):
- 22: class N8nBridgeConfigError(N8nBridgeError):
- 26: class N8nBridgeValidationError(N8nBridgeError):
- 30: class N8nHttpClientError(N8nBridgeError):

## src/core/observability.py

- 16: from __future__ import annotations
- 18: import json
- 19: from typing import Any, Mapping
- 22: def emit_metric(name: str, value: Any, labels: Mapping[str, Any] \| None = None) -> None:
- 32: def validate() -> None:

## src/core/providers/FlmChatAdapter.py

- 20: from __future__ import annotations
- 22: from collections.abc import Callable
- 23: from dataclasses import dataclass
- 24: from typing import Any, Protocol, cast
- 26: from openai import OpenAI
- 28: from src.core.providers.FlmProviderConfig import FlmProviderConfig
- 31: class FlmRuntimeError(RuntimeError):
- 35: class _CompletionCreator(Protocol):
- 38: def create(self, **kwargs: Any) -> Any:
- 42: class _ChatClient(Protocol):
- 48: class _ClientProtocol(Protocol):
- 55: class _ClientFactory(Protocol):
- 61: def __call__(self, *, base_url: str, api_key: str) -> _ClientProtocol:  # type: ignore[return]
- 65: class _ToolFunctionProtocol(Protocol):
- 72: class _ToolCallProtocol(Protocol):
- 80: ToolExecutor = Callable[[_ToolCallProtocol], str]
- 84: class FlmChatAdapter:
- 92: def validate() -> None:
- 110: class _DummyModels:
- 111: def list(self) -> Any:
- 114: class _DummyCompletions:
- 115: def create(self, **kwargs: Any) -> Any:
- 118: class _DummyChat:
- 121: class _DummyClient:
- 125: def _factory(*, base_url: str, api_key: str) -> _ClientProtocol:
- 127: raise FlmRuntimeError("Invalid FLM client factory inputs")
- 133: def _create_client(self) -> _ClientProtocol:
- 145: def check_endpoint_available(self) -> None:
- 155: def ensure_model_available(self, model: str \| None = None) -> None:
- 174: def create_completion(
- 197: async def run_until_terminal(
- 231: raise FlmRuntimeError("FLM returned tool_calls but no tool_executor was provided")
- 276: raise FlmRuntimeError(f"Exceeded max tool iterations ({max_tool_iterations}) while processing FLM tool calls")
- 279: def validate() -> None:

## src/core/providers/FlmModelProbe.py

- 24: from __future__ import annotations
- 26: import asyncio
- 27: import time
- 28: from dataclasses import dataclass
- 29: from typing import Sequence
- 30: from urllib.parse import urljoin
- 34: class FlmModelProbeResult:
- 44: def reachable(self) -> bool:
- 48: def to_dict(self) -> dict:
- 59: def select_model(available: Sequence[str], preferred: str \| None = None) -> str \| None:
- 83: async def probe_models(
- 153: async def _http_get(url: str) -> str:
- 159: from urllib.parse import urlparse
- 185: raise ValueError("Malformed HTTP response: no header/body separator")
- 190: raise ValueError(f"Malformed HTTP status line: {status_line!r}")
- 193: raise ValueError(f"FLM /v1/models returned HTTP {status_code}")
- 197: def validate() -> bool:
- 203: def _parse_models_body(body: str) -> list[str]:
- 213: import json

## src/core/providers/FlmProviderConfig.py

- 20: from __future__ import annotations
- 22: import os
- 23: from dataclasses import dataclass
- 24: from typing import Any, Mapping
- 28: class FlmProviderConfig:
- 39: def from_mapping(cls, values: Mapping[str, Any]) -> "FlmProviderConfig":
- 63: def _required_text(values: Mapping[str, Any], key: str) -> str:
- 66: raise ValueError(f"FLM provider config requires non-empty '{key}'")
- 70: def _optional_int(
- 79: raise ValueError(f"FLM provider config '{key}' must be an integer")
- 81: raise ValueError(f"FLM provider config '{key}' must be >= {minimum}")
- 85: def _optional_path(values: Mapping[str, Any], key: str, *, default: str) -> str:
- 88: raise ValueError(f"FLM provider config '{key}' must be a non-empty path")
- 91: raise ValueError(f"FLM provider config '{key}' must start with '/'")
- 99: def from_env(cls, prefix: str = "DV_FLM") -> "FlmProviderConfig":
- 112: def _int_env(name: str, default: int) -> int:
- 133: def validate(cls) -> None:
- 154: def validate() -> None:

## src/core/providers/__init__.py

- 21: from .FlmChatAdapter import FlmChatAdapter  # noqa: F401
- 22: from .FlmProviderConfig import FlmProviderConfig  # noqa: F401
- 24: __all__ = [

## src/core/reasoning/CortAgent.py

- 26: from __future__ import annotations
- 28: from typing import Any
- 30: from src.agents.BaseAgent import AgentManifest, BaseAgent
- 31: from src.core.reasoning.CortCore import (
- 38: from src.core.reasoning.EvaluationEngine import EvaluationEngine
- 45: class CortMixin:
- 52: async def reason_with_cort(self, prompt: str, **kwargs: Any) -> CortResult:
- 73: class CortAgent(BaseAgent, CortMixin):
- 90: def __init__(
- 116: async def run(self, task: dict[str, Any]) -> dict[str, Any]:
- 133: async def run_task(self, task: str) -> CortResult:
- 149: def validate() -> bool:

## src/core/reasoning/CortCore.py

- 24: from __future__ import annotations
- 26: import asyncio
- 27: import time
- 28: from dataclasses import dataclass
- 29: from typing import Protocol, runtime_checkable
- 34: _CORT_PRODUCT_CAP: int = 15
- 42: class CortLimitExceeded(Exception):  # noqa: N818
- 46: class CortRecursionError(Exception):
- 50: class AlternativesGenerationError(Exception):
- 60: class LlmCallable(Protocol):
- 63: async def __call__(
- 84: class EvaluatorLike(Protocol):
- 87: def select_best(self, chains: list["ReasoningChain"]) -> "ReasoningChain":
- 91: def score_and_assign(
- 106: class CortConfig:
- 130: def __post_init__(self) -> None:
- 144: DEFAULT_CORT_CONFIG = CortConfig(
- 160: class ReasoningChain:
- 178: def __lt__(self, other: object) -> bool:
- 192: def __gt__(self, other: object) -> bool:
- 206: def __eq__(self, other: object) -> bool:
- 222: class CortRound:
- 240: class CortMetadata:
- 259: class CortResult:
- 279: class CortCore:
- 289: def __init__(
- 308: async def run(self, prompt: str, context: str = "") -> CortResult:
- 364: async def _run_round(
- 393: async def _generate_alternatives(
- 429: async def _call_one(idx: int, temp: float) -> ReasoningChain:
- 469: def validate() -> bool:

## src/core/reasoning/EvaluationEngine.py

- 28: from __future__ import annotations
- 30: import dataclasses
- 31: import re
- 32: from dataclasses import dataclass, field
- 33: from typing import Any
- 39: _CONTRADICTION_MARKERS: tuple[str, ...] = (
- 46: _LOGICAL_CONNECTIVES: tuple[str, ...] = (
- 57: _CONNECTIVES_FOR_FULL_SCORE: int = 4
- 58: _STRUCTURE_BONUS: float = 0.2
- 61: _NUMBERED_LIST_RE = re.compile(r"^\s*\d+\.", re.MULTILINE)
- 62: _CODE_BLOCK_RE = re.compile(r"```")
- 71: class RubricScore:
- 91: def __post_init__(self) -> None:
- 105: class EvaluationEngine:
- 115: def __init__(
- 131: def score(self, chain: str, prompt: str) -> RubricScore:
- 152: def _score_correctness(self, chain: str) -> float:
- 170: def _score_completeness(self, chain: str, prompt: str) -> float:
- 194: def _score_reasoning_depth(self, chain: str) -> float:
- 220: def select_best(self, chains: list[Any]) -> Any:
- 235: raise ValueError("select_best requires a non-empty list of chains.")
- 238: def score_and_assign(
- 257: def validate() -> bool:

## src/core/reasoning/__init__.py

- 29: from __future__ import annotations
- 31: from src.core.reasoning.CortAgent import CortAgent, CortMixin
- 32: from src.core.reasoning.CortCore import (
- 38: from src.core.reasoning.EvaluationEngine import EvaluationEngine
- 40: __all__ = [

## src/core/replay/ReplayEnvelope.py

- 17: from __future__ import annotations
- 19: import hashlib
- 20: import json
- 21: from dataclasses import dataclass
- 22: from typing import Any, ClassVar
- 24: from .exceptions import ReplaySchemaError
- 28: class ReplayEnvelope:
- 87: def create(
- 133: def from_dict(cls, payload: dict[str, Any]) -> ReplayEnvelope:
- 171: def compute_checksum(payload: dict[str, Any]) -> str:
- 187: def _validate_payload(cls, payload: dict[str, Any]) -> None:
- 199: raise ReplaySchemaError(f"Missing required envelope fields: {', '.join(sorted(missing))}")
- 202: raise ReplaySchemaError("Unsupported replay schema_version")
- 205: raise ReplaySchemaError("input_payload must be a dictionary")
- 208: raise ReplaySchemaError("output_payload must be a dictionary")
- 211: raise ReplaySchemaError("side_effect_intents must be a list")
- 213: def validate(self) -> None:
- 221: raise ReplaySchemaError("sequence_no must be positive")
- 224: raise ReplaySchemaError("logical_clock must be positive")
- 227: raise ReplaySchemaError("logical_clock must be monotonic with sequence_no")
- 232: raise ReplaySchemaError("Envelope checksum mismatch")
- 234: raise ReplaySchemaError("Envelope checksum mismatch")
- 236: def to_dict(self) -> dict[str, Any]:
- 263: def _is_sha256(value: str) -> bool:

## src/core/replay/ReplayMixin.py

- 17: from __future__ import annotations
- 19: from datetime import datetime, timezone
- 20: from typing import Any
- 21: from uuid import uuid4
- 23: from .exceptions import ReplayConfigurationError
- 24: from .ReplayEnvelope import ReplayEnvelope
- 27: class ReplayMixin:
- 30: def validate(self) -> None:
- 39: raise ReplayConfigurationError("Replay orchestrator must expose replay_session")
- 41: async def emit_replay_envelope(
- 98: async def replay_session(
- 122: raise ReplayConfigurationError("Replay orchestrator is not configured")

## src/core/replay/ReplayOrchestrator.py

- 17: from __future__ import annotations
- 19: from dataclasses import dataclass, field
- 20: from typing import Any
- 22: from .exceptions import ReplayConfigurationError, ReplaySequenceError
- 23: from .ReplayEnvelope import ReplayEnvelope
- 27: class ReplayDivergence:
- 41: class ReplaySessionSummary:
- 62: class ReplayOrchestrator:
- 65: def __init__(self, *, store: Any, shadow_core: Any) -> None:
- 76: def validate(self) -> None:
- 84: raise ReplayConfigurationError("Replay store must expose load_session")
- 87: raise ReplayConfigurationError("Shadow core must expose execute_envelope")
- 89: async def replay_session(
- 140: def _validate_contiguous_sequence(self, envelopes: list[ReplayEnvelope]) -> None:

## src/core/replay/ReplayStore.py

- 17: from __future__ import annotations
- 19: import json
- 20: from pathlib import Path
- 22: from .exceptions import ReplayCorruptionError, ReplaySequenceError
- 23: from .ReplayEnvelope import ReplayEnvelope
- 26: class ReplayStore:
- 34: def __init__(self, *, root_path: str \| Path) -> None:
- 44: def validate(self) -> None:
- 52: raise ReplayCorruptionError("Replay store root path is not a directory")
- 54: async def append_envelope(self, envelope: ReplayEnvelope) -> None:
- 77: async def load_session(self, session_id: str) -> list[ReplayEnvelope]:
- 114: raise ReplaySequenceError(f"Duplicate sequence_no {envelope.sequence_no} in session '{session_id}'")
- 118: async def load_range(self, session_id: str, start_sequence: int, end_sequence: int) -> list[ReplayEnvelope]:
- 136: async def delete_session(self, session_id: str) -> None:
- 147: async def session_exists(self, session_id: str) -> bool:
- 159: def _session_file(self, session_id: str) -> Path:

## src/core/replay/ShadowExecutionCore.py

- 17: from __future__ import annotations
- 19: from dataclasses import dataclass
- 20: from typing import Any, Callable
- 22: from .exceptions import ReplayConfigurationError, ShadowPolicyViolation
- 23: from .ReplayEnvelope import ReplayEnvelope
- 27: class ReplayStepResult:
- 42: class ShadowExecutionCore:
- 45: def __init__(
- 70: def validate(self) -> None:
- 84: raise ReplayConfigurationError(f"Invalid shadow core dependency: {name}")
- 86: async def execute_envelope(
- 127: async def _execute_tool_intent(self, envelope: ReplayEnvelope) -> dict[str, Any]:
- 139: def _assert_shadow_policy(self, envelope: ReplayEnvelope) -> None:
- 157: raise ShadowPolicyViolation(f"Blocked shadow side effect intent: kind={kind}, action={action}")
- 159: async def _rollback_all(self, transactions: list[Any]) -> None:
- 169: await rollback()

## src/core/replay/__init__.py

- 17: from .exceptions import (
- 25: from .ReplayEnvelope import ReplayEnvelope
- 26: from .ReplayMixin import ReplayMixin
- 27: from .ReplayOrchestrator import ReplayDivergence, ReplayOrchestrator, ReplaySessionSummary
- 28: from .ReplayStore import ReplayStore
- 29: from .ShadowExecutionCore import ReplayStepResult, ShadowExecutionCore
- 31: __all__ = [

## src/core/replay/exceptions.py

- 18: class ReplayError(Exception):
- 22: class ReplaySchemaError(ReplayError):
- 26: class ReplaySequenceError(ReplayError):
- 30: class ReplayCorruptionError(ReplayError):
- 34: class ShadowPolicyViolationError(ReplayError):
- 38: ShadowPolicyViolation = ShadowPolicyViolationError
- 41: class ReplayConfigurationError(ReplayError):

## src/core/resilience/CircuitBreakerConfig.py

- 17: from __future__ import annotations
- 19: from dataclasses import dataclass, field
- 23: class CircuitBreakerConfig:
- 42: def validate() -> bool:

## src/core/resilience/CircuitBreakerCore.py

- 17: from __future__ import annotations
- 19: import time
- 21: from src.core.resilience.CircuitBreakerConfig import CircuitBreakerConfig
- 22: from src.core.resilience.CircuitBreakerState import CircuitBreakerState, CircuitState
- 25: class CircuitBreakerCore:
- 30: def record_success(self, state: CircuitBreakerState) -> None:
- 43: def record_failure(self, state: CircuitBreakerState, config: CircuitBreakerConfig) -> None:
- 64: def should_allow(self, state: CircuitBreakerState, config: CircuitBreakerConfig) -> bool:
- 94: def reset(self, state: CircuitBreakerState) -> None:
- 105: def check_state(self, state: CircuitBreakerState, config: CircuitBreakerConfig) -> CircuitState:
- 123: def validate() -> bool:

## src/core/resilience/CircuitBreakerMixin.py

- 17: from __future__ import annotations
- 19: from collections.abc import Awaitable, Callable
- 20: from typing import TypeVar
- 22: from src.core.resilience.CircuitBreakerConfig import CircuitBreakerConfig
- 23: from src.core.resilience.CircuitBreakerRegistry import CircuitBreakerRegistry
- 24: from src.core.resilience.CircuitBreakerState import CircuitState
- 25: from src.core.resilience.exceptions import AllCircuitsOpenError, CircuitOpenError
- 27: T = TypeVar("T")
- 30: class CircuitBreakerMixin:
- 35: def _setup_circuit_breaker(self, registry: CircuitBreakerRegistry) -> None:
- 44: async def cb_call(
- 82: raise AllCircuitsOpenError(tried_keys)
- 85: raise CircuitOpenError(provider_key, state.state)
- 87: async def _execute(
- 116: def _validate_circuit(self, provider_key: str) -> None:
- 127: raise AttributeError(f"Circuit breaker registry is not configured for provider '{provider_key}'.")
- 130: def validate() -> bool:

## src/core/resilience/CircuitBreakerRegistry.py

- 17: from __future__ import annotations
- 19: import asyncio
- 21: from src.core.resilience.CircuitBreakerConfig import CircuitBreakerConfig
- 22: from src.core.resilience.CircuitBreakerCore import CircuitBreakerCore
- 23: from src.core.resilience.CircuitBreakerState import CircuitBreakerState, CircuitState
- 26: class CircuitBreakerRegistry:
- 29: def __init__(self) -> None:
- 36: async def get_or_create(self, key: str, config: CircuitBreakerConfig) -> CircuitBreakerState:
- 55: async def get_fallback(self, key: str, config: CircuitBreakerConfig \| None = None) -> str \| None:
- 78: async def record_success(self, key: str, config: CircuitBreakerConfig \| None = None) -> None:
- 95: async def record_failure(self, key: str, config: CircuitBreakerConfig \| None = None) -> None:
- 112: async def should_allow(self, key: str, config: CircuitBreakerConfig \| None = None) -> bool:
- 132: async def reset(self, key: str, config: CircuitBreakerConfig \| None = None) -> None:
- 149: def _resolve_config(self, key: str, config: CircuitBreakerConfig \| None) -> CircuitBreakerConfig:
- 170: def validate() -> bool:

## src/core/resilience/CircuitBreakerState.py

- 17: from __future__ import annotations
- 19: from dataclasses import dataclass
- 20: from enum import Enum
- 23: class CircuitState(Enum):
- 32: class CircuitBreakerState:
- 57: def validate() -> bool:

## src/core/resilience/__init__.py

- 17: from __future__ import annotations
- 19: from src.core.resilience.CircuitBreakerConfig import CircuitBreakerConfig
- 20: from src.core.resilience.CircuitBreakerCore import CircuitBreakerCore
- 21: from src.core.resilience.CircuitBreakerMixin import CircuitBreakerMixin
- 22: from src.core.resilience.CircuitBreakerRegistry import CircuitBreakerRegistry
- 23: from src.core.resilience.CircuitBreakerState import CircuitBreakerState, CircuitState
- 24: from src.core.resilience.exceptions import AllCircuitsOpenError, CircuitOpenError
- 26: __all__ = [
- 38: def validate() -> bool:

## src/core/resilience/exceptions.py

- 17: from __future__ import annotations
- 19: from src.core.resilience.CircuitBreakerState import CircuitState
- 22: class CircuitOpenError(Exception):
- 31: def __init__(self, provider_key: str, state: CircuitState) -> None:
- 44: class AllCircuitsOpenError(Exception):
- 52: def __init__(self, tried_keys: list[str]) -> None:
- 64: def validate() -> bool:

## src/core/runtime.py

- 23: from __future__ import annotations
- 25: import asyncio
- 26: import uuid
- 27: from dataclasses import dataclass, field
- 28: from typing import Any, Awaitable, Callable, Optional
- 35: async def spawn_task(
- 48: async def set_timeout(
- 57: async def _delayed() -> Any:
- 64: def create_queue(maxsize: int = 0) -> asyncio.Queue[Any]:
- 79: class Runtime:
- 85: async def start(self) -> None:
- 89: async def submit(self, coro: Awaitable[Any], task_id: Optional[str] = None) -> str:
- 96: def cancel(self, task_id: str) -> bool:
- 104: def pending(self) -> list[str]:
- 110: def validate() -> None:

## src/core/sandbox/SandboxConfig.py

- 17: from __future__ import annotations
- 19: import uuid
- 20: from dataclasses import dataclass, field
- 21: from pathlib import Path
- 25: class SandboxConfig:
- 42: def from_strings(
- 69: def validate() -> bool:

## src/core/sandbox/SandboxMixin.py

- 17: from __future__ import annotations
- 19: from src.core.sandbox.SandboxConfig import SandboxConfig
- 20: from src.core.sandbox.SandboxedStorageTransaction import SandboxedStorageTransaction
- 21: from src.core.sandbox.SandboxViolationError import SandboxViolationError
- 24: class SandboxMixin:
- 32: class MyAgent(SandboxMixin):
- 33: def __init__(self, allowed_dir: Path) -> None:
- 39: def sandbox_tx(self) -> SandboxedStorageTransaction:
- 48: def _validate_host(self, host: str) -> None:
- 63: raise SandboxViolationError(resource=host, reason="host not in allowed_hosts")
- 66: def validate() -> bool:

## src/core/sandbox/SandboxViolationError.py

- 17: from __future__ import annotations
- 20: class SandboxViolationError(RuntimeError):
- 32: def __init__(self, resource: str, reason: str) -> None:
- 45: def validate() -> bool:

## src/core/sandbox/SandboxedStorageTransaction.py

- 17: from __future__ import annotations
- 19: from pathlib import Path
- 20: from typing import Optional
- 22: from src.core.sandbox.SandboxConfig import SandboxConfig
- 23: from src.core.sandbox.SandboxViolationError import SandboxViolationError
- 24: from src.transactions.StorageTransactionManager import StorageTransaction
- 27: class SandboxedStorageTransaction(StorageTransaction):
- 40: def __init__(self, sandbox: SandboxConfig, target: Optional[Path] = None) -> None:
- 56: def _is_subpath(path: Path, allowed: Path) -> bool:
- 74: def _validate_path(self, path: Path) -> None:
- 98: async def write(self, path: Path, content: bytes, *, user_id: Optional[str] = None) -> None:
- 111: await super().write(path, content, user_id=user_id)
- 113: async def delete(self, path: Path) -> None:
- 124: await super().delete(path)
- 126: async def mkdir(self, path: Path) -> None:
- 137: await super().mkdir(path)
- 143: def commit(self) -> None:
- 158: def validate() -> bool:

## src/core/sandbox/__init__.py

- 17: from src.core.sandbox.SandboxConfig import SandboxConfig
- 18: from src.core.sandbox.SandboxedStorageTransaction import SandboxedStorageTransaction
- 19: from src.core.sandbox.SandboxMixin import SandboxMixin
- 20: from src.core.sandbox.SandboxViolationError import SandboxViolationError
- 22: __all__ = [

## src/core/scaffold/__init__.py

- 20: from dataclasses import dataclass
- 21: from typing import Protocol
- 24: class CoreAPI(Protocol):
- 27: def validate(self) -> None: ...
- 31: class ExampleCore:
- 36: def do_work(self, payload: dict[str, object]) -> dict[str, object]:
- 49: def validate() -> None:

## src/core/security_bridge.py

- 15: from __future__ import annotations
- 17: import subprocess
- 18: from pathlib import Path
- 21: def _rust_security_binary() -> Path:
- 34: def generate_key(path: Path) -> None:
- 40: def rotate_keys(path: Path) -> None:
- 46: def encrypt(key_file: Path, plaintext: str) -> str:
- 65: def decrypt(key_file: Path, ciphertext: str) -> str:
- 84: def validate() -> None:

## src/core/task_queue.py

- 16: from __future__ import annotations
- 18: import asyncio
- 19: from dataclasses import dataclass
- 20: from typing import Any, Optional
- 24: class TaskQueue:
- 35: def __post_init__(self) -> None:
- 40: async def put(self, item: Any) -> None:
- 45: async def get(self) -> Any:
- 50: def qsize(self) -> int:
- 55: def empty(self) -> bool:
- 60: def full(self) -> bool:
- 65: def task_done(self) -> None:
- 70: async def join(self) -> None:
- 76: def validate() -> None:
- 80: raise RuntimeError("TaskQueue missing core put/get methods")
- 82: raise RuntimeError("TaskQueue initial state is invalid")

## src/core/universal/UniversalAgentShell.py

- 17: from __future__ import annotations
- 19: import asyncio
- 20: from dataclasses import dataclass
- 21: from typing import Any, Awaitable, Callable, Literal, Protocol
- 23: from src.core.universal.exceptions import (
- 31: from src.core.universal.UniversalCoreRegistry import CoreHandlerProtocol
- 32: from src.core.universal.UniversalIntentRouter import RoutingDecision, TaskEnvelope
- 35: class IntentRouterProtocol(Protocol):
- 38: def classify(self, envelope: TaskEnvelope) -> RoutingDecision:
- 50: class CoreRegistryProtocol(Protocol):
- 53: def resolve(self, intent: str) -> CoreHandlerProtocol:
- 65: LegacyDispatcher = Callable[[TaskEnvelope], Awaitable[dict[str, Any]]]
- 69: class DispatchResult:
- 86: class UniversalAgentShell:
- 89: def __init__(
- 110: raise RoutingContractError("core_timeout_seconds must be > 0")
- 117: async def dispatch(self, envelope: Any) -> DispatchResult:
- 145: raise RoutingContractError(f"Unsupported preferred_route: {decision.preferred_route}")
- 149: def _validate_envelope(self, envelope: Any) -> TaskEnvelope:
- 163: raise EnvelopeValidationError("Envelope must be a TaskEnvelope instance")
- 166: def _validate_decision(self, decision: Any) -> RoutingDecision:
- 187: raise RoutingContractError("Router decision normalized_intent cannot be empty")
- 189: raise RoutingContractError("Router decision preferred_route must be 'core' or 'legacy'")
- 199: async def _dispatch_core_with_fallback(
- 247: async def _dispatch_legacy(self, envelope: TaskEnvelope) -> dict[str, Any]:
- 268: def validate() -> bool:
- 278: __all__ = ["DispatchResult", "LegacyDispatcher", "UniversalAgentShell", "validate"]

## src/core/universal/UniversalCoreRegistry.py

- 17: from __future__ import annotations
- 19: import inspect
- 20: from typing import Any, Callable, Protocol
- 22: from src.core.universal.exceptions import CoreNotRegisteredError, CoreRegistrationError
- 25: class CoreHandlerProtocol(Protocol):
- 28: async def execute(self, envelope: Any) -> dict[str, Any]:
- 40: CoreFactory = Callable[[], CoreHandlerProtocol]
- 43: class UniversalCoreRegistry:
- 46: def __init__(self) -> None:
- 50: def register(self, intent: str, factory: CoreFactory) -> None:
- 64: raise CoreRegistrationError(f"Core already registered for intent: {normalized_intent}")
- 69: def resolve(self, intent: str) -> CoreHandlerProtocol:
- 86: raise CoreNotRegisteredError(f"No core registered for intent: {normalized_intent}")
- 92: def has_intent(self, intent: str) -> bool:
- 104: def list_intents(self) -> tuple[str, ...]:
- 113: def unregister(self, intent: str) -> bool:
- 127: def _normalize_intent(self, intent: str) -> str:
- 142: raise CoreRegistrationError("Intent cannot be empty")
- 145: def _ensure_valid_factory(self, factory: CoreFactory) -> None:
- 156: raise CoreRegistrationError("Core factory must be callable")
- 161: def _ensure_valid_handler(self, handler: Any) -> None:
- 173: raise CoreRegistrationError("Core handler must expose execute()")
- 175: raise CoreRegistrationError("Core handler execute() must be async")
- 178: def validate() -> bool:
- 188: __all__ = ["CoreFactory", "CoreHandlerProtocol", "UniversalCoreRegistry", "validate"]

## src/core/universal/UniversalIntentRouter.py

- 17: from __future__ import annotations
- 19: from dataclasses import dataclass
- 20: from typing import Any, Literal
- 22: from src.core.universal.exceptions import EnvelopeValidationError
- 26: class TaskEnvelope:
- 44: class RoutingDecision:
- 59: class UniversalIntentRouter:
- 62: def __init__(self, core_allowlist: set[str] \| None = None) -> None:
- 72: def normalize_intent(self, intent: str \| None) -> str:
- 89: def classify(self, envelope: TaskEnvelope) -> RoutingDecision:
- 103: raise EnvelopeValidationError("Dispatch envelope must be a TaskEnvelope instance")
- 120: def validate() -> bool:
- 130: __all__ = ["TaskEnvelope", "RoutingDecision", "UniversalIntentRouter", "validate"]

## src/core/universal/__init__.py

- 17: from src.core.universal.exceptions import (
- 27: from src.core.universal.UniversalAgentShell import DispatchResult, UniversalAgentShell
- 28: from src.core.universal.UniversalCoreRegistry import UniversalCoreRegistry
- 29: from src.core.universal.UniversalIntentRouter import RoutingDecision, TaskEnvelope, UniversalIntentRouter
- 32: def validate() -> bool:
- 42: __all__ = [

## src/core/universal/exceptions.py

- 18: class UniversalShellError(Exception):
- 22: class EnvelopeValidationError(UniversalShellError):
- 26: class RoutingContractError(UniversalShellError):
- 30: class CoreRegistrationError(UniversalShellError):
- 34: class CoreNotRegisteredError(UniversalShellError):
- 38: class CoreExecutionError(UniversalShellError):
- 42: class CoreTimeoutError(UniversalShellError):
- 46: class LegacyDispatchError(UniversalShellError):
- 50: def validate() -> bool:
- 60: __all__ = [

## src/core/workflow/engine.py

- 4: from src.core.workflow.queue import TaskQueue
- 5: from src.core.workflow.task import Task, TaskState
- 8: class WorkflowEngine:
- 11: def __init__(self, queue: TaskQueue) -> None:
- 15: async def run_once(self) -> None:
- 22: def validate() -> None:

## src/core/workflow/queue.py

- 4: import asyncio
- 6: from src.core.workflow.task import Task
- 9: class TaskQueue:
- 12: def __init__(self) -> None:
- 16: async def enqueue(self, task: Task) -> None:
- 20: async def dequeue(self) -> Task:
- 25: def validate() -> None:
- 28: async def _run() -> None:

## src/core/workflow/task.py

- 4: from dataclasses import dataclass, field
- 5: from enum import Enum
- 6: from typing import Any
- 9: class TaskState(Enum):
- 20: class Task:
- 28: def transition(self, new_state: TaskState) -> None:
- 33: def validate() -> None:
- 37: raise AssertionError("initial state should be active")
- 40: raise AssertionError("state transition failed")

## src/cort/__init__.py

- 16: from __future__ import annotations
- 18: from typing import Optional
- 20: from context_manager import ContextManager
- 23: class ChainOfThought:
- 26: def __init__(self, context_mgr: ContextManager):
- 31: async def new_node(self, text: str) -> "ThoughtNode":
- 45: class ThoughtNode:
- 48: def __init__(self, text: str, cort: ChainOfThought):
- 60: async def fork(self, text: str) -> "ThoughtNode":
- 71: async def add(self, text: str) -> None:

## src/github_app.py

- 25: from __future__ import annotations
- 27: import hashlib
- 28: import hmac
- 29: import json
- 30: import logging
- 31: import os
- 32: from typing import Any, Optional
- 34: from fastapi import FastAPI, Header, HTTPException, Request, status
- 36: app = FastAPI(title="PyAgent GitHub App", version="1.0.0")
- 37: _log = logging.getLogger(__name__)
- 43: WEBHOOK_SECRET: str = os.getenv("GITHUB_WEBHOOK_SECRET", "")
- 51: def verify_github_signature(
- 76: def _handle_push(payload: dict[str, Any]) -> dict[str, Any]:
- 84: def _handle_pull_request(payload: dict[str, Any]) -> dict[str, Any]:
- 94: def _handle_issues(payload: dict[str, Any]) -> dict[str, Any]:
- 104: _HANDLERS = {
- 117: def health() -> dict[str, str]:
- 123: async def webhook(

## src/importer/__init__.py

- 4: from .compile import compile_architecture  # noqa: F401
- 5: from .config import parse_manifest  # noqa: F401
- 6: from .describe import describe_file  # noqa: F401
- 7: from .downloader import download_repo  # noqa: F401

## src/importer/compile.py

- 4: from pathlib import Path
- 7: async def compile_architecture(descriptors: list[dict[str, object]], out_path: Path) -> None:

## src/importer/config.py

- 14: from pathlib import Path
- 15: from typing import Tuple
- 18: async def parse_manifest(path: Path) -> list[Tuple[str, str]]:

## src/importer/describe.py

- 17: from pathlib import Path
- 20: def describe_file(path: Path) -> dict[str, object]:

## src/importer/downloader.py

- 16: from __future__ import annotations
- 18: import shutil
- 19: import subprocess
- 20: from pathlib import Path
- 23: def _git_binary() -> str:
- 27: raise FileNotFoundError("git executable not found on PATH")
- 31: def clone_repo(repo_url: str, dest: Path, *, depth: int \| None = 1) -> int:
- 60: def download_repo(repo: str, dest: Path) -> None:
- 101: def _normalize_repo_url(repo: str) -> str:
- 116: raise RuntimeError("Repository identifier must not be empty")
- 122: raise RuntimeError("Repository identifier must be owner/name or a full git URL")
- 128: raise RuntimeError("Repository identifier must be owner/name or a full git URL")

## src/mcp/McpClient.py

- 26: from __future__ import annotations
- 28: import asyncio
- 29: from dataclasses import dataclass, field
- 30: from typing import Any, Optional
- 32: from src.mcp.exceptions import McpCallTimeout, McpProtocolError, McpServerCrashed
- 33: from src.mcp.McpServerConfig import McpServerConfig
- 35: __all__ = ["McpClient", "McpToolDefinition", "McpToolResult"]
- 39: class McpToolDefinition:
- 55: class McpToolResult:
- 68: class McpClient:
- 86: def __init__(
- 107: async def initialize(self) -> dict[str, Any]:
- 143: async def list_tools(self) -> list[McpToolDefinition]:
- 167: async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> McpToolResult:
- 189: async def ping(self) -> bool:
- 202: async def close(self) -> None:
- 222: async def _rpc_call(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
- 238: import json
- 258: raise McpProtocolError(str(cached["error"]))
- 269: async def _read_loop(self) -> None:
- 275: import json

## src/mcp/McpRegistry.py

- 28: from __future__ import annotations
- 30: import asyncio
- 31: from enum import Enum
- 33: import yaml
- 35: from src.mcp.exceptions import (
- 40: from src.mcp.McpClient import McpClient
- 41: from src.mcp.McpSandbox import McpSandbox
- 42: from src.mcp.McpServerConfig import McpServerConfig
- 43: from src.mcp.McpToolAdapter import McpToolAdapter
- 45: __all__ = ["McpRegistry", "McpServerStatus"]
- 48: class McpServerStatus(Enum):
- 67: class McpRegistry:
- 83: def __init__(self) -> None:
- 100: async def load_config(self, path: str) -> None:
- 125: def list_servers(self) -> list[McpServerConfig]:
- 134: def get_client(self, name: str) -> McpClient:
- 156: async def enable(self, name: str) -> None:
- 173: raise McpServerNotFound(f"Server '{name}' is not configured")
- 178: raise McpServerAlreadyEnabled(f"Server '{name}' is already running")
- 201: async def disable(self, name: str) -> None:
- 216: raise McpServerNotEnabled(f"Server '{name}' is not running")
- 243: async def reload(self, name: str) -> None:

## src/mcp/McpSandbox.py

- 27: from __future__ import annotations
- 29: import asyncio
- 30: from pathlib import Path
- 32: from src.mcp.exceptions import (
- 38: from src.mcp.McpServerConfig import McpServerConfig
- 40: __all__ = ["McpSandbox"]
- 43: def _is_subpath(child: Path, parent: Path) -> bool:
- 52: class McpSandbox:
- 63: def build_env(self, config: McpServerConfig) -> tuple[dict[str, str], dict[str, str]]:
- 87: import os
- 113: async def spawn(self, config: McpServerConfig) -> asyncio.subprocess.Process:
- 133: import hashlib
- 162: async def terminate(self, process: asyncio.subprocess.Process) -> None:
- 184: def validate_path(self, path: str, config: McpServerConfig) -> Path:
- 205: raise McpPathForbidden(f"Path '{resolved}' is not under any allowed prefix: {config.allowed_paths!r}")

## src/mcp/McpServerConfig.py

- 28: from __future__ import annotations
- 30: from dataclasses import dataclass, field
- 31: from typing import Optional
- 33: from src.mcp.exceptions import McpConfigError
- 35: __all__ = ["McpServerConfig"]
- 37: _VALID_RESTART_POLICIES = {"on-failure", "always", "never"}
- 38: _VALID_TRANSPORTS = {"stdio", "http+sse"}
- 39: _VALID_STARTUP_MODES = {"eager", "lazy"}
- 43: class McpServerConfig:
- 88: def __post_init__(self) -> None:
- 98: raise McpConfigError("McpServerConfig.name must not be empty")
- 100: raise McpConfigError(f"McpServerConfig[{self.name!r}].command must not be empty")
- 117: def from_dict(cls, data: dict) -> "McpServerConfig":
- 137: raise McpConfigError("McpServerConfig.from_dict: 'name' is required")
- 139: raise McpConfigError(f"McpServerConfig.from_dict[{data.get('name')!r}]: 'command' is required")

## src/mcp/McpToolAdapter.py

- 22: use a plain in-memory dict and the registry can be wired at construction time.
- 25: from __future__ import annotations
- 27: from typing import Any, Callable
- 29: from src.mcp.exceptions import McpToolNameCollision
- 30: from src.mcp.McpClient import McpClient, McpToolDefinition, McpToolResult
- 31: from src.mcp.McpSandbox import McpSandbox
- 32: from src.mcp.McpServerConfig import McpServerConfig
- 33: from src.tools.tool_registry import Tool
- 35: __all__ = ["McpToolAdapter"]
- 38: class McpToolAdapter:
- 49: def __init__(self, registry_ref: dict[str, Any]) -> None:
- 65: async def register_server_tools(
- 102: raise McpToolNameCollision(f"Tool '{namespaced_name}' is already registered in the registry")
- 111: async def deregister_server_tools(self, server_name: str) -> int:
- 137: def tool_definition_to_spec(
- 167: async def async_main(args: list[str] \| None = None) -> int:  # noqa: ARG001
- 186: def _build_tool(
- 214: async def async_main(args: list[str] \| None = None) -> int:

## src/mcp/exceptions.py

- 39: from __future__ import annotations
- 41: __all__ = [
- 60: class McpError(Exception):
- 64: class McpConfigError(McpError):
- 68: class McpServerNotFound(McpError):
- 72: class McpServerNotEnabled(McpError):
- 76: class McpServerAlreadyEnabled(McpError):
- 80: class McpServerCrashed(McpError):
- 84: class McpCallTimeout(McpError):
- 88: class McpProtocolError(McpError):
- 92: class McpToolError(McpError):
- 96: class McpSandboxError(McpError):
- 100: class McpPinMismatch(McpSandboxError):
- 104: class McpPathForbidden(McpSandboxError):
- 108: class McpSecretNotFound(McpSandboxError):
- 112: class McpToolNameCollision(McpError):
- 116: class McpHealthError(McpError):

## src/memory/__init__.py

- 16: from __future__ import annotations
- 18: from typing import Any
- 21: class MemoryStore:
- 24: def __init__(self) -> None:
- 27: def set(self, key: str, value: Any) -> None:
- 30: def get(self, key: str, default: Any = None) -> Any:
- 33: def delete(self, key: str) -> None:
- 36: def clear(self) -> None:
- 39: def snapshot(self) -> dict[str, Any]:
- 43: def validate() -> bool:
- 53: __all__ = ["MemoryStore", "validate"]

## src/multimodal/__init__.py

- 27: from __future__ import annotations
- 29: from .models import Modality, MultiModalData, MultiModalInputs
- 30: from .processor import MultiModalProcessor
- 32: __all__ = [
- 41: def validate() -> bool:

## src/multimodal/models.py

- 21: from __future__ import annotations
- 23: from dataclasses import dataclass, field
- 24: from enum import Enum, auto
- 25: from typing import Any
- 28: class Modality(Enum):
- 39: class MultiModalData:
- 64: def is_text(self) -> bool:
- 69: def is_binary(self) -> bool:
- 73: def as_text(self) -> str:
- 91: class MultiModalInputs:
- 109: def add(self, item: MultiModalData) -> None:
- 113: def text_items(self) -> list[MultiModalData]:
- 117: def by_modality(self, modality: Modality) -> list[MultiModalData]:
- 121: def to_prompt_parts(self) -> list[str]:
- 134: def _item_to_text(item: MultiModalData) -> str:

## src/multimodal/processor.py

- 20: from __future__ import annotations
- 22: import base64
- 23: import logging
- 24: from typing import Any, Protocol
- 26: from .models import Modality, MultiModalData, MultiModalInputs
- 28: logger = logging.getLogger(__name__)
- 31: class ModalityProcessor(Protocol):
- 34: def process(self, data: MultiModalData) -> dict[str, Any]:
- 39: class TextProcessor:
- 42: def process(self, data: MultiModalData) -> dict[str, Any]:
- 46: class ImageProcessor:
- 49: def process(self, data: MultiModalData) -> dict[str, Any]:
- 58: class AudioProcessor:
- 61: def process(self, data: MultiModalData) -> dict[str, Any]:
- 68: class MultiModalProcessor:
- 88: def __init__(
- 96: def register(self, modality: Modality, processor: ModalityProcessor) -> None:
- 100: def process_item(self, data: MultiModalData) -> dict[str, Any]:
- 111: def process(self, inputs: MultiModalInputs) -> list[dict[str, Any]]:
- 123: def validate() -> bool:

## src/observability/stats/legacy_engine.py

- 17: from __future__ import annotations
- 19: from runtime_py import sleep, spawn
- 21: counter: int = 0
- 24: def start_loop() -> None:
- 31: async def _tick() -> None:
- 40: def get_count() -> int:

## src/observability/stats/metrics_engine.py

- 4: from __future__ import annotations
- 6: from runtime_py import sleep, spawn  # type: ignore[import-not-found]  # noqa: E402
- 40: counter: int = 0
- 43: def start_async_loop() -> None:
- 52: async def _tick_loop() -> None:

## src/plugins/PluginManager.py

- 21: from plugins import Plugin, PluginManager
- 23: class MyPlugin(Plugin):
- 25: def name(self) -> str:
- 28: def execute(self, **kwargs):
- 36: from __future__ import annotations
- 38: import logging
- 39: from abc import ABC, abstractmethod
- 40: from dataclasses import dataclass, field
- 41: from typing import Any
- 43: logger = logging.getLogger(__name__)
- 47: class PluginMetadata:
- 72: class Plugin(ABC):
- 89: def name(self) -> str:
- 93: def metadata(self) -> PluginMetadata:
- 97: def setup(self) -> None:  # noqa: B027
- 100: def teardown(self) -> None:  # noqa: B027
- 104: def execute(self, **kwargs: Any) -> Any:
- 120: class PluginManager:
- 134: def __init__(self) -> None:
- 141: def register(self, plugin: Plugin) -> None:
- 155: def unregister(self, name: str) -> None:
- 172: def get(self, name: str) -> Plugin:
- 186: def list_plugins(self) -> list[PluginMetadata]:
- 190: def has(self, name: str) -> bool:
- 194: def find_by_tag(self, tag: str) -> list[Plugin]:
- 202: def execute(self, name: str, **kwargs: Any) -> Any:
- 224: def _teardown_one(self, name: str, plugin: "Plugin") -> None:
- 231: def shutdown(self) -> None:
- 236: def __len__(self) -> int:
- 239: def __repr__(self) -> str:

## src/plugins/__init__.py

- 20: from __future__ import annotations
- 22: from .PluginManager import Plugin, PluginManager, PluginMetadata
- 24: __all__ = ["Plugin", "PluginManager", "PluginMetadata"]

## src/rl/__init__.py

- 17: from __future__ import annotations
- 19: import math
- 20: import warnings
- 23: def discounted_return(rewards: list[float], gamma: float = 0.99) -> float:
- 38: raise ValueError("gamma must be within [0.0, 1.0]")
- 40: raise ValueError("rewards must contain only finite values")
- 45: def validate() -> bool:
- 60: __all__ = ["discounted_return", "validate"]

## src/roadmap/__init__.py

- 15: from . import vision
- 17: __all__ = ["vision"]

## src/roadmap/cli.py

- 24: from __future__ import annotations
- 26: import argparse
- 27: import asyncio
- 28: import sys
- 29: from pathlib import Path
- 31: from . import milestones, vision
- 34: def generate(outdir: Path \| str) -> Path:
- 45: def _build_parser() -> argparse.ArgumentParser:
- 67: def main(argv: list[str] \| None = None) -> int:

## src/roadmap/innovation.py

- 15: import json
- 16: from pathlib import Path
- 17: from typing import Any
- 20: def record_experiment(name: str, db_path: str = "experiments.json") -> Path:

## src/roadmap/milestones.py

- 16: from pathlib import Path
- 17: from typing import Union
- 20: async def create(path: Union[str, Path], items: list[str]) -> None:

## src/roadmap/prioritization.py

- 17: def score_feature(attrs) -> float:

## src/roadmap/vision.py

- 17: def get_template() -> str:

## src/runtime/__init__.py

- 23: from __future__ import annotations
- 25: import asyncio
- 26: import inspect
- 27: from collections.abc import Awaitable, Callable
- 28: from typing import Any
- 31: def spawn_task(py_coro: Awaitable[Any]) -> None:
- 42: def set_timeout(ms: float, callback: Callable[[], None]) -> None:
- 48: def create_queue() -> tuple[asyncio.Queue[Any], Callable[[Any], Awaitable[None]]]:
- 54: def _shutdown_runtime() -> None:

## src/runtime_py/__init__.py

- 8: import path, which previously caused the local package to take precedence over
- 16: from __future__ import annotations
- 18: import asyncio
- 19: import importlib
- 20: import logging
- 21: import threading
- 22: from collections.abc import Awaitable, Callable
- 23: from typing import Any
- 25: _EXTENSION: object \| None = None
- 28: _background_loop: asyncio.AbstractEventLoop \| None = None
- 31: class _PythonRuntimeExtension:
- 34: def __init__(self) -> None:
- 38: def spawn_task(self, py_coro: Awaitable[object]) -> None:
- 42: def set_timeout(self, ms: float, callback: Callable[[], None]) -> None:
- 47: def create_queue(self) -> tuple[asyncio.Queue[object], Callable[[object], Awaitable[None]]]:
- 53: def _get_extension() -> object:
- 85: def _ensure_background_loop() -> asyncio.AbstractEventLoop:
- 95: def _run_loop() -> None:
- 110: def sleep(ms: float) -> asyncio.Future[None]:
- 115: def _done() -> None:
- 125: def create_queue() -> tuple[object, object]:
- 144: _event_subscribers: dict[str, list[Any]] = {}
- 147: def spawn(coro: Any) -> None:
- 173: async def _wrapper() -> None:
- 205: def on(event: str, handler: object) -> None:
- 210: def emit(event: str, *args: object, **kwargs: object) -> None:
- 223: def watch_file(path: str, callback: Callable[[str], Awaitable[None]]) -> None:
- 232: import os
- 242: async def _poll() -> None:
- 255: await callback(path)
- 260: def run_http_server(addr: str, handler: Callable[[str], Awaitable[tuple[int, str]]]) -> None:
- 274: async def _handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
- 291: async def _serve() -> None:

## src/security/__init__.py

- 17: from .rotation_checkpoint_service import RotationCheckpointService
- 18: from .secret_guardrail_policy import SecretGuardrailPolicy
- 19: from .secret_scan_service import SecretScanService
- 21: __all__ = [

## src/security/models/__init__.py

- 17: from .guardrail_decision import GuardrailDecision
- 18: from .rotation_models import RotationCheckpoint, RotationGateDecision
- 19: from .scan_report import ScanReport
- 21: __all__ = [

## src/security/models/guardrail_decision.py

- 17: from dataclasses import dataclass, field
- 21: class GuardrailDecision:

## src/security/models/rotation_models.py

- 17: from __future__ import annotations
- 19: from dataclasses import dataclass, field
- 23: class RotationCheckpoint:
- 41: class RotationGateDecision:

## src/security/models/scan_report.py

- 17: from __future__ import annotations
- 19: from dataclasses import dataclass, field
- 20: from typing import Any
- 22: _ALLOWED_STATUSES = {"PASS", "FAIL", "ERROR"}
- 23: _BLOCKING_SEVERITIES = {"HIGH", "CRITICAL"}
- 27: class ScanReport:
- 45: def __post_init__(self) -> None:
- 54: raise ValueError(msg)
- 57: raise ValueError(msg)

## src/security/rotation_checkpoint_service.py

- 17: from __future__ import annotations
- 19: from .models.rotation_models import RotationCheckpoint, RotationGateDecision
- 22: class RotationCheckpointService:
- 25: def __init__(self) -> None:
- 29: def begin_incident(
- 54: def record_rotation_step(self, incident_id: str, system: str, evidence_uri: str) -> None:
- 68: raise ValueError(msg)
- 72: raise ValueError(msg)
- 75: def evaluate_gate(self, incident_id: str) -> RotationGateDecision:
- 91: raise ValueError(msg)

## src/security/secret_guardrail_policy.py

- 17: from __future__ import annotations
- 19: from typing import Any
- 21: from .models.guardrail_decision import GuardrailDecision
- 23: _BLOCKING_SEVERITIES = {"HIGH", "CRITICAL"}
- 26: class SecretGuardrailPolicy:
- 29: def validate_pr(self, findings: list[dict[str, Any]]) -> GuardrailDecision:
- 41: def validate_push(self, findings: list[dict[str, Any]]) -> GuardrailDecision:
- 53: def _evaluate(self, findings: list[dict[str, Any]], gate_name: str) -> GuardrailDecision:

## src/security/secret_scan_service.py

- 17: from __future__ import annotations
- 19: from typing import Any
- 21: from .models.scan_report import ScanReport
- 24: class SecretScanService:
- 27: def normalize_finding_keys(self, findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
- 39: def scan_tree(self, findings: list[dict[str, Any]] \| None = None) -> ScanReport:
- 51: def scan_refs(self, findings: list[dict[str, Any]] \| None = None) -> ScanReport:
- 63: def scan_history(self, findings: list[dict[str, Any]] \| None = None) -> ScanReport:
- 75: def _scan_profile(self, profile: str, findings: list[dict[str, Any]]) -> ScanReport:
- 104: def _execute_profile(self, profile: str, findings: list[dict[str, Any]]) -> dict[str, Any]:

## src/skills_registry/__init__.py

- 16: from __future__ import annotations
- 18: from pathlib import Path
- 20: import yaml
- 23: class SkillsRegistry:
- 26: def __init__(self, skills_dir: Path):
- 30: async def list_skills(self) -> list[str]:

## src/speculation/__init__.py

- 17: from __future__ import annotations
- 19: import math
- 20: import warnings
- 23: def select_candidate(scores: dict[str, float], threshold: float = 0.0) -> str \| None:
- 38: raise ValueError("scores must contain only finite values")
- 49: def validate() -> bool:
- 64: __all__ = ["select_candidate", "validate"]

## src/swarm/__init__.py

- 16: from .agent_registry import AgentRegistry
- 17: from .memory_store import SwarmMemory
- 18: from .message_model import Message, validate_message
- 19: from .swarm_node import SwarmNode
- 20: from .task_scheduler import TaskScheduler
- 22: __all__ = [

## src/swarm/agent_registry.py

- 17: import time
- 18: from typing import Any
- 21: class AgentRegistry:
- 24: def __init__(self, heartbeat_interval: float = 30.0) -> None:
- 29: def register(self, agent_type: str, capabilities: list[str]) -> str:
- 39: def heartbeat(self, agent_id: str) -> None:
- 43: def get(self, agent_id: str) -> dict[str, Any]:
- 47: def is_healthy(self, agent_id: str) -> bool:
- 50: from typing import cast
- 55: def metrics(self) -> str:

## src/swarm/memory_store.py

- 16: from __future__ import annotations
- 18: import asyncio
- 19: from typing import Any
- 22: class SwarmMemory:
- 30: def __init__(self) -> None:
- 35: async def shared_set(self, key: str, value: Any) -> None:
- 40: async def shared_get(self, key: str, default: Any = None) -> Any:
- 45: async def local_set(self, node_id: str, key: str, value: Any) -> None:
- 50: async def local_get(self, node_id: str, key: str, default: Any = None) -> Any:
- 55: async def shared_keys(self) -> list[str]:
- 60: def metrics(self) -> str:

## src/swarm/message_model.py

- 4: from typing import Any
- 6: from pydantic import BaseModel
- 9: class Message(BaseModel):
- 22: def validate_message(data: dict[str, Any]) -> bool:

## src/swarm/swarm_node.py

- 16: from __future__ import annotations
- 18: import asyncio
- 19: import uuid
- 20: from typing import Any
- 22: from .message_model import Message, validate_message
- 25: class SwarmNode:
- 33: def __init__(self, node_id: str \| None = None) -> None:
- 42: def _make_message(self, msg_type: str, destination: str, payload: dict[str, Any]) -> dict[str, Any]:
- 43: import time
- 56: async def ping(self, destination: str) -> dict[str, Any]:
- 60: async def receive(self, raw: dict[str, Any]) -> dict[str, Any] \| None:
- 68: async def enqueue(self, raw: dict[str, Any]) -> None:
- 72: async def process_one(self) -> dict[str, Any] \| None:

## src/swarm/task_scheduler.py

- 4: import heapq
- 5: import time
- 6: import uuid
- 7: from typing import Any
- 10: class TaskScheduler:
- 13: def __init__(self) -> None:
- 19: def enqueue(self, payload: dict[str, Any], priority: int = 3) -> str:
- 28: async def dequeue(self) -> dict[str, Any]:
- 36: raise IndexError("no tasks")
- 38: def modify(self, task_id: str, priority: int) -> None:

## src/tools/FileWatcher.py

- 15: import asyncio
- 16: import json
- 17: import os
- 18: import time
- 19: from pathlib import Path
- 20: from typing import Optional
- 23: import rust_core as _rust_core
- 31: def _python_scan_sync(root: str, since_ms: float) -> list:
- 46: async def _python_scan(root: str, since_ms: float) -> list:
- 51: class FileWatcher:
- 64: def __init__(self, root: str, interval_s: float = 1.0) -> None:
- 71: async def start(self) -> None:
- 74: async def stop(self) -> None:
- 82: async def get_changes(self) -> list:
- 88: async def _poll(self) -> None:

## src/tools/__init__.py

- 22: from __future__ import annotations
- 24: import importlib
- 25: import logging
- 26: import pkgutil
- 28: _log = logging.getLogger(__name__)
- 31: _SKIP = frozenset({"tool_registry", "__main__", "common"})

## src/tools/__main__.py

- 22: from __future__ import annotations
- 24: import argparse
- 25: import sys
- 27: from src.tools.tool_registry import list_tools, run_tool
- 30: def _build_parser() -> argparse.ArgumentParser:
- 40: def main(argv: list[str] \| None = None) -> int:
- 57: raise SystemExit(main())

## src/tools/agent_plugins.py

- 4: from __future__ import annotations
- 6: import argparse
- 7: import importlib.util
- 8: import json
- 9: from pathlib import Path
- 12: from src.tools.tool_registry import register_tool
- 14: from tools.tool_registry import register_tool
- 16: PLUGIN_DIR = Path(__file__).parent / "plugins"
- 20: def _load_plugin(path: Path) -> str \| None:
- 31: def load_plugins() -> list[str]:
- 36: def main(args: list[str] \| None = None) -> int:

## src/tools/boot.py

- 17: from __future__ import annotations
- 19: import argparse
- 20: import sys
- 21: import textwrap
- 24: from src.tools.tool_registry import register_tool
- 26: from tools.tool_registry import register_tool
- 29: def _render_pyproject(name: str) -> str:
- 41: def main(args: list[str] \| None = None) -> int:

## src/tools/code_quality.py

- 11: from __future__ import annotations
- 13: import argparse
- 14: import shutil
- 15: import subprocess
- 16: import sys
- 17: import tempfile
- 18: from typing import Iterable, List
- 20: from .tool_registry import register_tool
- 23: def _run_cmd(cmd: list[str], capture: bool = False) -> int:
- 33: def _get_changed_files(base: str) -> List[str]:
- 48: def _select_python_files(files: Iterable[str]) -> List[str]:
- 53: def main(args: list[str] \| None = None) -> int:

## src/tools/common.py

- 16: import asyncio
- 17: import json
- 18: import logging
- 19: import os
- 20: from pathlib import Path
- 21: from typing import Any, Callable, TypeVar
- 24: import tomllib  # Python 3.11+
- 27: import tomli as tomllib  # type: ignore[no-redef]
- 31: T = TypeVar("T")
- 34: def load_config(path: str) -> Any:
- 39: raise RuntimeError("TOML support requires Python 3.11+ or the 'tomli' package.")
- 46: def get_logger(name: str, level: int = logging.WARNING) -> logging.Logger:
- 57: def ensure_dir(path: str \| os.PathLike) -> Path:
- 64: async def retry(
- 86: def format_table(rows: list[list[Any]], headers: list[str]) -> str:
- 91: >>> print(format_table([["alice", 30], ["bob", 25]], ["Name", "Age"]))
- 101: def _render_row(cells: list[str]) -> str:

## src/tools/dependency_audit.py

- 16: from __future__ import annotations
- 18: import argparse
- 19: import json
- 20: import os
- 23: import tomllib  # type: ignore
- 25: import tomli as tomllib  # type: ignore
- 28: from src.tools.tool_registry import register_tool
- 30: from tools.tool_registry import register_tool
- 33: def check_dependencies(project_root: str = ".") -> list[str]:
- 63: def main(args: list[str] \| None = None) -> int:

## src/tools/git_utils.py

- 22: from __future__ import annotations
- 24: import argparse
- 25: import datetime
- 26: import subprocess
- 27: import sys
- 28: from pathlib import Path
- 29: from typing import Iterable
- 32: from src.tools.tool_registry import register_tool
- 34: from tools.tool_registry import register_tool
- 42: def _run_git(
- 55: def _get_merge_base(base: str) -> str \| None:
- 63: def _current_branch() -> str:
- 74: def create_feature_branch(name: str, base: str = "main") -> bool:
- 96: def changed_files(base: str = "main") -> list[str]:
- 107: def update_changelog(entry: str, changelog_path: str = "CHANGELOG.md") -> None:
- 136: def main(args: list[str] \| None = None) -> int:

## src/tools/knock.py

- 17: from __future__ import annotations
- 19: import argparse
- 20: import socket
- 21: import sys
- 24: from src.tools.tool_registry import register_tool
- 26: from tools.tool_registry import register_tool
- 29: def main(args: list[str] \| None = None) -> int:
- 38: def _check_port(port: int) -> str:

## src/tools/metrics.py

- 19: from __future__ import annotations
- 21: import argparse
- 22: import ast
- 23: import pathlib
- 24: from typing import NamedTuple
- 27: from src.tools.tool_registry import register_tool
- 29: from tools.tool_registry import register_tool
- 32: class FileMetrics(NamedTuple):
- 44: def _estimate_complexity(tree: ast.AST) -> int:
- 58: def analyze_file(path: str) -> FileMetrics:
- 109: def analyze_directory(root: str) -> list[FileMetrics]:
- 127: def collect_metrics(root: str) -> dict[str, int]:
- 149: def main(args: list[str] \| None = None) -> int:
- 165: import json
- 178: import sys

## src/tools/netcalc.py

- 17: from __future__ import annotations
- 19: import argparse
- 20: import ipaddress
- 21: import sys
- 24: from src.tools.tool_registry import register_tool
- 26: from tools.tool_registry import register_tool
- 29: def main(args: list[str] \| None = None) -> int:

## src/tools/nettest.py

- 17: from __future__ import annotations
- 19: import argparse
- 20: import asyncio
- 21: import sys
- 24: from src.tools.tool_registry import register_tool
- 26: from tools.tool_registry import register_tool
- 29: async def _check_host(host: str, port: int, timeout: float) -> bool:
- 41: async def main(args: list[str] \| None = None) -> int:

## src/tools/nginx.py

- 17: from __future__ import annotations
- 19: import argparse
- 20: import shutil
- 21: import subprocess
- 22: import sys
- 25: from src.tools.tool_registry import register_tool
- 27: from tools.tool_registry import register_tool
- 30: def main(args: list[str] \| None = None) -> int:

## src/tools/plugin_loader.py

- 18: module injection.
- 22: from src.tools.plugin_loader import load_plugin, discover_plugins
- 32: from __future__ import annotations
- 34: import importlib
- 35: import importlib.util
- 36: import os
- 37: import sys
- 38: from types import ModuleType
- 39: from typing import Any
- 42: from src.tools.tool_registry import register_tool
- 44: from tools.tool_registry import register_tool
- 47: def discover_plugins(plugin_dir: str) -> list[str]:
- 75: def load_plugin(name: str, allowed: list[str], plugin_dir: str \| None = None) -> ModuleType:
- 106: raise ValueError(f"Invalid plugin name: {name!r}. Must be a plain identifier.")
- 108: raise ValueError(f"Plugin name {name!r} contains dots. Use a simple module name, not a package path.")
- 111: raise ValueError(f"Plugin {name!r} is not in the allowed list. Allowed plugins: {sorted(allowed)}")
- 116: raise ImportError(f"Plugin file not found: {plugin_path}")
- 120: raise ImportError(f"Cannot create spec for plugin: {plugin_path}")
- 131: def get_plugin_attr(name: str, allowed: list[str], attr: str, plugin_dir: str \| None = None) -> Any:
- 160: raise AttributeError(f"Plugin {name!r} has no attribute {attr!r}")
- 164: def main(args: list[str] \| None = None) -> int:
- 166: import argparse

## src/tools/pm/__init__.py

- 8: from . import email, kpi, risk  # noqa: F401

## src/tools/pm/email.py

- 17: async def render(template: str, context: dict[str, str]) -> str:

## src/tools/pm/kpi.py

- 16: from typing import Any, Sequence
- 19: def compute_throughput(completed: Sequence[Any], period: Sequence[Any]) -> int:
- 27: def velocity(completed_points: Sequence[float], sprints: int = 1) -> float:
- 30: raise ValueError("sprints must be >= 1")
- 34: def cycle_time(start_ts: float, end_ts: float) -> float:
- 37: raise ValueError("end_ts must be >= start_ts")
- 41: def defect_rate(bugs_found: int, total_items: int) -> float:
- 44: raise ValueError("total_items must be > 0")
- 48: def sprint_health(completed: int, planned: int) -> str:
- 51: raise ValueError("planned must be > 0")

## src/tools/pm/risk.py

- 16: from __future__ import annotations
- 18: _SCORE: dict[str, int] = {"low": 1, "medium": 3, "high": 5}
- 21: class Risk:
- 24: def __init__(self, title: str, probability: str, impact: str, mitigation: str = "") -> None:
- 31: def score(self) -> int:
- 36: def level(self) -> str:
- 45: def to_dict(self) -> dict[str, str]:
- 57: async def read_matrix(path: str) -> list[dict[str, str]]:
- 91: def top_risks(matrix: list[dict[str, str]], n: int = 5) -> list[dict[str, str]]:

## src/tools/port_forward.py

- 17: from __future__ import annotations
- 19: import argparse
- 20: import asyncio
- 21: import sys
- 24: from src.tools.tool_registry import register_tool
- 26: from tools.tool_registry import register_tool
- 29: async def _handle_client(
- 38: async def _pipe(src: asyncio.StreamReader, dst: asyncio.StreamWriter) -> None:
- 59: async def main(args: list[str] \| None = None) -> int:

## src/tools/proxy_test.py

- 17: from __future__ import annotations
- 19: import argparse
- 20: import sys
- 21: import urllib.request
- 24: from src.tools.tool_registry import register_tool
- 26: from tools.tool_registry import register_tool
- 29: def main(args: list[str] \| None = None) -> int:

## src/tools/ql.py

- 27: from __future__ import annotations
- 29: import argparse
- 30: import datetime
- 31: import shutil
- 32: import subprocess
- 33: import sys
- 34: import tempfile
- 35: from pathlib import Path
- 36: from typing import List, Optional, Tuple
- 38: from src.tools.tool_registry import register_tool
- 41: def _run_cmd(cmd: list[str], capture: bool = False) -> Tuple[int, str, str]:
- 54: def _get_merge_base(base: str) -> Optional[str]:
- 62: def _get_changed_files(base: str) -> List[str]:
- 77: def _guess_project_name(branch: str) -> str:
- 87: def _get_current_branch() -> str:
- 95: def _ensure_report_path(project: str) -> Path:
- 103: def _render_markdown_report(
- 174: def main(args: list[str] \| None = None) -> int:

## src/tools/remote.py

- 23: from __future__ import annotations
- 25: import argparse
- 26: import shutil
- 27: import subprocess
- 28: import sys
- 29: from pathlib import Path
- 32: from src.tools.tool_registry import register_tool
- 34: from tools.tool_registry import register_tool
- 37: def run_ssh_command(
- 68: raise FileNotFoundError("ssh binary not found on PATH")
- 81: def upload_file(host: str, local_path: str, remote_path: str, user: str \| None = None, port: int = 22) -> int:
- 110: raise FileNotFoundError("scp binary not found on PATH")
- 119: def upload_files(
- 129: def main(args: list[str] \| None = None) -> int:

## src/tools/self_heal.py

- 15: from __future__ import annotations
- 17: import argparse
- 18: import ast
- 19: import os
- 20: import sys
- 23: from src.tools.tool_registry import register_tool
- 25: from tools.tool_registry import register_tool
- 28: def _check_py_syntax(root: str) -> dict[str, str]:
- 31: def _check_file(path: str) -> tuple[str, str] \| None:
- 49: def detect_misconfig(root: str = ".") -> dict[str, str]:
- 54: def main(args: list[str] \| None = None) -> int:

## src/tools/ssl_utils.py

- 18: using Python's standard library ``ssl`` module. For advanced operations
- 23: from __future__ import annotations
- 25: import argparse
- 26: import datetime
- 27: import json
- 28: import socket
- 29: import ssl
- 30: import sys
- 31: from pathlib import Path
- 34: from src.tools.tool_registry import register_tool
- 36: from tools.tool_registry import register_tool
- 39: def check_expiry(host: str, port: int = 443, timeout: float = 5.0) -> dict[str, object]:
- 88: def verify_pem_file(path: str) -> dict[str, object]:
- 114: def main(args: list[str] \| None = None) -> int:

## src/tools/tool_registry.py

- 20: from src.tools.tool_registry import register_tool
- 22: def main(args: list[str] \| None = None) -> int:
- 29: from __future__ import annotations
- 31: import asyncio
- 32: import inspect
- 33: from dataclasses import dataclass
- 34: from typing import Any, Callable, Coroutine, Dict, List, Optional, Union
- 36: ToolMain = Callable[[list[str] \| None], Union[int, Coroutine[Any, Any, int]]]
- 40: class Tool:
- 48: _REGISTRY: Dict[str, Tool] = {}
- 51: def register_tool(name: str, main: ToolMain, description: str) -> None:
- 59: raise ValueError(f"Tool '{name}' is already registered")
- 63: def list_tools() -> List[Tool]:
- 68: def get_tool(name: str) -> Optional[Tool]:
- 73: def run_tool(name: str, args: list[str] \| None = None) -> int:
- 77: raise KeyError(f"Unknown tool: {name}")
- 85: def deregister_tool(name: str) -> None:
- 100: async def async_run_tool(name: str, args: list[str] \| None = None) -> int:
- 121: raise KeyError(f"Tool '{name}' not registered")

## src/transactions/BaseTransaction.py

- 17: from __future__ import annotations
- 19: import abc
- 22: class BaseTransaction(abc.ABC):  # noqa: B024

## src/transactions/ContextTransactionManager.py

- 21: from __future__ import annotations
- 23: import uuid
- 24: from contextvars import ContextVar, Token
- 25: from types import TracebackType
- 26: from typing import Any, List, Optional, Set
- 28: _active_var: ContextVar[Optional[Set[str]]] = ContextVar("_active_ctx", default=None)
- 29: _stack_var: ContextVar[Optional[List["ContextTransaction"]]] = ContextVar("_context_stack", default=None)
- 32: class RecursionGuardError(RuntimeError):
- 36: class ContextTransaction:
- 47: def __init__(
- 58: raise ValueError("context_id must be a non-empty string")
- 70: def _get_active() -> Set[str]:
- 76: def _get_stack() -> List["ContextTransaction"]:
- 85: def __enter__(self) -> "ContextTransaction":
- 91: raise RecursionGuardError(f"Context {self.context_id!r} is already active (recursion guard).")
- 103: def __exit__(
- 122: async def __aenter__(self) -> "ContextTransaction":
- 126: async def __aexit__(
- 140: def active_contexts(cls) -> Set[str]:
- 146: def current(cls) -> Optional["ContextTransaction"]:
- 157: async def commit(self) -> None:
- 160: async def rollback(self) -> None:
- 163: async def hand_to_llm(self, context_window: Any) -> None:
- 172: def validate() -> bool:

## src/transactions/MemoryTransactionManager.py

- 17: from __future__ import annotations
- 19: import asyncio
- 20: import base64
- 21: import json
- 22: import os
- 23: import threading
- 24: from pathlib import Path
- 25: from types import TracebackType
- 26: from typing import Any, Optional
- 27: from urllib.parse import urlparse
- 29: from src.core import security_bridge
- 32: class RemoteSyncError(RuntimeError):
- 35: def __init__(self, endpoint: str, cause: Exception) -> None:
- 41: class MemoryTransaction:
- 54: def __init__(self, tid: Optional[Any] = None) -> None:
- 62: def _memory_key_file(self) -> str:
- 72: def _pack_value(value: Any) -> str:
- 91: def _unpack_value(payload_text: str) -> Any:
- 100: raise ValueError(f"Unsupported encrypted payload type: {payload_type!r}")
- 106: def __enter__(self) -> "MemoryTransaction":
- 111: def __exit__(
- 124: async def __aenter__(self) -> "MemoryTransaction":
- 131: async def __aexit__(
- 145: async def set(self, key: str, value: Any, *, encrypt: bool = False) -> None:
- 154: async def get(self, key: str, *, decrypt: bool = False) -> Optional[Any]:
- 171: async def delete(self, key: str) -> None:
- 176: async def commit(self) -> None:
- 181: async def rollback(self) -> None:
- 189: async def sync_remote(  # noqa: D417
- 222: import httpx
- 224: import logging
- 240: def validate() -> bool:

## src/transactions/ProcessTransactionManager.py

- 17: from __future__ import annotations
- 19: import subprocess
- 20: from collections.abc import Coroutine
- 21: from types import TracebackType
- 22: from typing import TYPE_CHECKING, Any, List, Optional, Tuple
- 25: import asyncio
- 28: class ProcessTransaction:
- 45: def __init__(self, cmd: Optional[List[str]] = None) -> None:
- 57: def start(self) -> None:
- 65: def wait(self) -> int:
- 75: def rollback(self) -> Coroutine[None, None, None]:
- 90: async def _async_terminate(self) -> None:
- 95: import asyncio
- 109: def __enter__(self) -> "ProcessTransaction":
- 116: def __exit__(
- 137: async def __aenter__(self) -> "ProcessTransaction":
- 141: async def __aexit__(
- 158: import asyncio
- 172: async def start_async(self) -> None:
- 180: import asyncio
- 181: import sys
- 190: async def wait_async(self, timeout: float = 30.0) -> int:
- 192: import asyncio
- 198: raise RuntimeError("Async process did not produce a returncode after communicate().")
- 201: async def run(self, cmd: List[str], *, cwd: Any = None, timeout: float = 30.0) -> Tuple[int, str, str]:
- 203: import asyncio
- 215: raise RuntimeError("Process did not produce a returncode after communicate().")
- 219: def validate() -> bool:

## src/transactions/StorageTransactionManager.py

- 22: from __future__ import annotations
- 24: import asyncio
- 25: import base64
- 26: import os
- 27: import tempfile
- 28: from collections.abc import Coroutine
- 29: from pathlib import Path
- 30: from types import TracebackType
- 31: from typing import List, Optional, Tuple
- 34: class CommitError(RuntimeError):
- 38: class EncryptionConfigError(ValueError):
- 47: async def _noop_coro() -> None:  # pragma: no cover
- 62: class StorageTransaction:
- 65: Legacy mode (target supplied)
- 79: def __init__(self, target: Optional[Path] = None) -> None:
- 92: def stage(self, content: bytes) -> None:
- 96: def commit(self) -> None:
- 108: raise RuntimeError("commit() is only valid in legacy (single-file) mode.")
- 126: def rollback(self) -> Coroutine[None, None, None]:
- 146: def __enter__(self) -> "StorageTransaction":
- 150: def __exit__(
- 174: async def __aenter__(self) -> "StorageTransaction":
- 178: async def __aexit__(
- 207: async def write(self, path: Path, content: bytes, *, user_id: Optional[str] = None) -> None:
- 218: async def delete(self, path: Path) -> None:
- 222: async def mkdir(self, path: Path) -> None:
- 226: async def acommit(self) -> None:
- 256: def _encrypt(self, content: bytes, user_id: str) -> bytes:
- 268: from cryptography.fernet import Fernet
- 269: from cryptography.hazmat.primitives import hashes
- 270: from cryptography.hazmat.primitives.kdf.hkdf import HKDF
- 287: def validate() -> bool:

## src/transactions/__init__.py

- 17: from src.transactions.BaseTransaction import BaseTransaction
- 18: from src.transactions.ContextTransactionManager import ContextTransaction, RecursionGuardError
- 19: from src.transactions.MemoryTransactionManager import MemoryTransaction
- 20: from src.transactions.ProcessTransactionManager import ProcessTransaction
- 21: from src.transactions.StorageTransactionManager import StorageTransaction
- 23: __all__ = [

## src/transport/__init__.py

- 24: from __future__ import annotations
- 26: import os
- 27: import sys
- 28: from pathlib import Path
- 31: def _locate_local_rust_core() -> Path \| None:
- 44: def _apply_local_rust_core_path() -> None:
- 81: import rust_core  # type: ignore
- 86: def _ensure_rust_core() -> None:
- 88: raise ImportError("rust_core extension is not available. Ensure the Rust extension is built.")
- 91: def generate_node_identity() -> bytes:
- 97: def get_node_id() -> bytes:
- 103: def save_node_identity(path: str) -> None:
- 109: def load_node_identity(path: str) -> None:
- 115: def transport_loopback_pair() -> tuple[int, int]:
- 121: def transport_send(handle: int, payload: bytes) -> None:
- 127: def transport_recv(handle: int) -> bytes:
- 133: def transport_handshake_initiator(handle: int) -> None:
- 139: def transport_handshake_responder(handle: int) -> None:
- 145: def transport_handshake_finalize(a: int, b: int) -> None:
- 151: def validate() -> bool:
- 179: class NodeIdentity:
- 185: def __init__(self) -> None:
- 190: def public_key(self) -> bytes:
- 194: def sign(self, message: bytes) -> bytes:
- 200: def verify(public_key: bytes, message: bytes, signature: bytes) -> bool:
- 205: def __repr__(self) -> str:
- 209: class LoopbackChannel:
- 216: def __init__(self) -> None:
- 223: def send(self, payload: bytes) -> None:
- 228: def recv(self) -> bytes:
- 233: def send_b(self, payload: bytes) -> None:
- 238: def recv_a(self) -> bytes:
- 244: __all__ = [
