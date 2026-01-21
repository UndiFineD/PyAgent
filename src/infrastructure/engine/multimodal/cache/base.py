# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Base class for multimodal caching."""

import threading
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional
from .hasher import MultiModalHasher
from .data import MediaHash, CacheEntry, CacheStats


class MultiModalCache(ABC):
    """
    Abstract base for multimodal content caching.

    Features:
    - LRU eviction with configurable capacity
    - Content-aware hashing
    - Statistics tracking
    """

    def __init__(
        self,
        max_size_bytes: int = 1024 * 1024 * 1024,  # 1GB
        max_entries: int = 10000,
        hasher: Optional[MultiModalHasher] = None,
    ):
        self.max_size_bytes = max_size_bytes
        self.max_entries = max_entries
        self.hasher = hasher or MultiModalHasher()
        self._stats = CacheStats()
        self._lock = threading.RLock()

    @abstractmethod
    def get(self, key: MediaHash) -> Optional[CacheEntry]:
        """Get entry from cache."""
        pass

    @abstractmethod
    def put(self, key: MediaHash, data: Any, metadata: Optional[Dict] = None) -> CacheEntry:
        """Put entry into cache."""
        pass

    @abstractmethod
    def evict(self, count: int = 1) -> int:
        """Evict entries, return number evicted."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all entries."""
        pass

    @abstractmethod
    def contains(self, key: MediaHash) -> bool:
        """Check if key exists in cache."""
        pass

    def get_or_compute(
        self,
        key: MediaHash,
        compute_fn: Callable[[], Any],
        metadata: Optional[Dict] = None
    ) -> CacheEntry:
        """Get from cache or compute and cache."""
        entry = self.get(key)
        if entry is not None:
            return entry

        # Compute and cache
        data = compute_fn()
        return self.put(key, data, metadata)

    @property
    def stats(self) -> CacheStats:
        """Get cache statistics."""
        return self._stats
