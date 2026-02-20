"""Minimal shim for AutoMem memory core used in tests.

This module provides a small, import-safe subset of the original
AutoMemCore API so the test-suite can import and exercise higher-level
components without requiring external services.
"""
from __future__ import annotations



try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass

try:
    from typing import Any, Dict, List, Optional, Union
except ImportError:
    from typing import Any, Dict, List, Optional, Union


try:
    import logging
except ImportError:
    import logging

try:
    import time
except ImportError:
    import time




@dataclass
class MemoryRecord:
    id: str
    vector: List[float]
    metadata: Dict[str, Any]


@dataclass
class MemoryConfig:
    falkordb_url: str = "redis://localhost:6379"
    qdrant_url: str = "http://localhost:6333"
    collection_name: str = "pyagent_memories"
    vector_dim: int = 1536


class AutoMemCore:
    """Lightweight AutoMem shim.

    Stores memories in-memory and exposes a tiny API sufficient for tests.
    """

    def __init__(self, config: Union[MemoryConfig, Dict[str, Any]] | None = None):
        if config is None or isinstance(config, dict):
            config = MemoryConfig() if config is None else MemoryConfig(**{k: v for k, v in (config or {}).items() if hasattr(MemoryConfig, k)})
        self.config: MemoryConfig = config
        self._store: List[Dict[str, Any]] = []
        self.logger = logging.getLogger("pyagent.memory.automem")

    def add_memory(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> MemoryRecord:
        mid = f"mem-{int(time.time() * 1000)}"
        record = MemoryRecord(id=mid, vector=[], metadata=metadata or {})
        self._store.append({"id": mid, "content": content, "metadata": metadata or {}})
        return record

    def query(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        # naive substring match for shim
        results = [m for m in self._store if query_text in m.get("content", "")]
        return results[:top_k]


__all__ = ["AutoMemCore", "MemoryRecord", "MemoryConfig"]
