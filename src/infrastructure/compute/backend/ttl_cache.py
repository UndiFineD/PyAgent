"""
Cache with time-to-live expiration.
(Facade for src.core.base.common.cache_core)
"""

from src.core.base.common.cache_core import CacheCore as StandardCacheCore

<<<<<<< HEAD
<<<<<<< HEAD
"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .CachedResponse import CachedResponse
from typing import Any, Dict, Optional
import threading
import time

__version__ = VERSION

class TTLCache:
    """Cache with time-to-live expiration.
=======
class TTLCache(StandardCacheCore):
    """Facade for CacheCore."""
    pass
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
class TTLCache(StandardCacheCore):
    """Facade for CacheCore."""
    pass
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

    Caches responses with configurable TTL, automatically expiring stale entries.

    Example:
        cache=TTLCache(default_ttl_seconds=300)
        cache.set("key", "value")

        result=cache.get("key")  # Returns "value" if not expired
    """

    def __init__(
        self,
        default_ttl_seconds: float = 300.0,
        max_entries: int = 1000,
    ) -> None:
        """Initialize TTL cache.

        Args:
            default_ttl_seconds: Default TTL for entries.
            max_entries: Maximum cache entries.
        """
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
        """Set cache entry.

        Args:
            key: Cache key.
            value: Value to cache.
            ttl_seconds: Optional custom TTL.
        """
        now = time.time()
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
        """Get cache entry if not expired.

        Args:
            key: Cache key.

        Returns:
            Optional[str]: Cached value or None.
        """
        with self._lock:
            entry = self._cache.get(key)
            if not entry:
                return None

            if time.time() > entry.expires_at:
                del self._cache[key]
                return None

            entry.hit_count += 1
            return entry.content

    def _cleanup_expired(self) -> int:
        """Remove expired entries.

        Returns:
            int: Number of entries removed.
        """
        now = time.time()
        expired = [k for k, v in self._cache.items() if now > v.expires_at]
        for key in expired:
            del self._cache[key]
        return len(expired)

    def invalidate(self, key: str) -> bool:
        """Invalidate cache entry.

        Args:
            key: Cache key.

        Returns:
            bool: True if entry was removed.
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self) -> int:
        """Clear all cache entries.

        Returns:
            int: Number of entries cleared.
        """
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
        return count

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics.

        Returns:
            Dict: Cache stats.
        """
        with self._lock:
            total_hits = sum(e.hit_count for e in self._cache.values())
            return {
                "entries": len(self._cache),
                "max_entries": self.max_entries,
                "total_hits": total_hits,
                "default_ttl_seconds": self.default_ttl_seconds,
            }