"""
Manager for result caching.
(Facade for src.core.base.common.cache_core)
"""

<<<<<<< HEAD
<<<<<<< HEAD
"""
Manager for result caching.
(Facade for src.core.base.common.cache_core)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.core.base.common.cache_core import CacheCore


class ResultCache:
    """Caches results of agent operations."""

    def __init__(self, core: CacheCore | None = None) -> None:
        self._core = core or CacheCore(Path("data/agent_cache"))
        self._memory_cache: dict[str, Any] = {}

    def get(
        self,
        file_path_or_key: str,
        agent_name: str | None = None,
        content_hash: str | None = None,
        default: Any = None
    ) -> Any:
        """Get a cached result. Supports legacy multi-arg calls."""
        key = file_path_or_key
        if agent_name and content_hash:
            key = f"{file_path_or_key}:{agent_name}:{content_hash}"

        if key in self._memory_cache:
            return self._memory_cache[key]

        res = self._core.get(key)
        if res is not None:
            self._memory_cache[key] = res
            return res
        return default

    def set(
        self,
        file_path_or_key: str,
        agent_name_or_value: Any,
        content_hash: str | None = None,
        data: Any = None
    ) -> None:
        """Cache a result. Supports legacy multi-arg calls."""
        key = file_path_or_key
        value = agent_name_or_value

        if content_hash and data is not None:
            # Called as set(file, agent, hash, data)
            key = f"{file_path_or_key}:{agent_name_or_value}:{content_hash}"
            value = data

        self._memory_cache[key] = value
        self._core.set(key, value)

    def clear(self) -> None:
        """Clears both memory and disk cache."""
        self._memory_cache.clear()
        self._core.clear()
=======
from src.core.base.common.cache_core import CacheCore as ResultCache
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
from src.core.base.common.cache_core import CacheCore as ResultCache
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
