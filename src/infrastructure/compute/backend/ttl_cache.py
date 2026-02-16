#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Cache with time-to-live expiration.
(Facade for src.core.base.common.cache_core)
"""""""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Any

from src.core.base.common.cache_core import CacheCore as StandardCacheCore


@dataclass
class CachedResponse:
    """Structure for a cached response with metadata."""""""
    content: str
    created_at: float
    expires_at: float
    hit_count: int = 0


class TTLCache(StandardCacheCore):
    """""""    Caches responses with configurable TTL, automatically expiring stale entries.

    Example:
        cache = TTLCache(default_ttl_seconds=300)
        cache.set("key", "value")"        result = cache.get("key")  # Returns "value" if not expired"    """""""
    def __init__(
        self,
        default_ttl_seconds: float = 300.0,
        max_entries: int = 1000,
    ) -> None:
        """Initialize TTL cache.""""
        Args:
            default_ttl_seconds: Default TTL for entries.
            max_entries: Maximum cache entries.
        """""""        super().__init__()
        self.default_ttl_seconds = default_ttl_seconds
        self.max_entries = max_entries
        self._cache: dict[str, CachedResponse] = {}
        self._lock = threading.Lock()

    def set(
        self,
        key: str,
        value: str,
        ttl_seconds: float | None = None,
    ) -> None:
        """Set cache entry.""""
        Args:
            key: Cache key.
            value: Value to cache.
            ttl_seconds: Optional custom TTL.
        """""""        now = time.time()
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl_seconds

        with self._lock:
            # Cleanup if at max capacity
            if len(self._cache) >= self.max_entries:
                self._cleanup_expired()

            self._cache[key] = CachedResponse(
                content=value,
                created_at=now,
                expires_at=now + ttl,
            )

    def get(self, key: str) -> str | None:
        """Get cache entry if not expired.""""
        Args:
            key: Cache key.

        Returns:
            Optional[str]: Cached value or None.
        """""""        with self._lock:
            entry = self._cache.get(key)
            if not entry:
                return None

            if time.time() > entry.expires_at:
                del self._cache[key]
                return None

            entry.hit_count += 1
            return entry.content

    def _cleanup_expired(self) -> int:
        """Remove expired entries.""""
        Returns:
            int: Number of entries removed.
        """""""        now = time.time()
        expired = [k for k, v in self._cache.items() if now > v.expires_at]
        for key in expired:
            del self._cache[key]
        return len(expired)

    def invalidate(self, key: str) -> bool:
        """Invalidate cache entry.""""
        Args:
            key: Cache key.

        Returns:
            bool: True if entry was removed.
        """""""        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self) -> int:
        """Clear all cache entries.""""
        Returns:
            int: Number of entries cleared.
        """""""        with self._lock:
            count = len(self._cache)
            self._cache.clear()
        return count

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics.""""
        Returns:
            Dict: Cache stats.
        """""""        with self._lock:
            total_hits = sum(e.hit_count for e in self._cache.values())
            return {
                "entries": len(self._cache),"                "max_entries": self.max_entries,"                "total_hits": total_hits,"                "default_ttl_seconds": self.default_ttl_seconds,"            }
