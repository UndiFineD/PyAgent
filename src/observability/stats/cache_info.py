"""
CacheInfo - LRU Cache with hit/miss statistics and pinned items.

Inspired by vLLM's cache.py patterns for production cache monitoring.

Phase 17: vLLM Pattern Integration
"""
from __future__ import annotations
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Hashable, Iterator

K = TypeVar('K', bound=Hashable)
V = TypeVar('V')


@dataclass
class CacheStats:
    """Statistics for cache performance monitoring."""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    pins: int = 0

    @property
    def total(self) -> int:
        """Total access attempts."""
        return self.hits + self.misses

    @property
    def hit_ratio(self) -> float:
        """Cache hit ratio (0.0 to 1.0)."""
        if self.total == 0:
            return 0.0
        return self.hits / self.total

    @property
    def miss_ratio(self) -> float:
        """Cache miss ratio (0.0 to 1.0)."""
        return 1.0 - self.hit_ratio

    def reset(self) -> 'CacheStats':
        """Reset stats and return a copy of the old stats."""
        old = CacheStats(
            hits=self.hits,
            misses=self.misses,
            evictions=self.evictions,
            pins=self.pins,
        )
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.pins = 0
        return old

    def to_dict(self) -> dict:
        return {
            'hits': self.hits,
            'misses': self.misses,
            'total': self.total,
            'hit_ratio': round(self.hit_ratio, 4),
            'evictions': self.evictions,
            'pins': self.pins,
        }


@dataclass
class CacheEntry(Generic[V]):
    """A cache entry with value, timestamp, and pin status."""
    value: V
    created_at: float = field(default_factory=time.time)
    last_access: float = field(default_factory=time.time)
    access_count: int = 0
    pinned: bool = False

    def touch(self) -> None:
        """Update access time and count."""
        self.last_access = time.time()
        self.access_count += 1


class LRUCache(Generic[K, V]):
    """
    Thread-safe LRU cache with hit statistics and pinned items.

    Features:
    - Hit/miss tracking with statistics
    - Pinned items that won't be evicted
    - Delta statistics (changes since last check)
    - Touch operation for manual LRU updates
    - Capacity tracking

    Example:
        >>> cache = LRUCache[str, int](max_size=100)
        >>> cache.put("key1", 42)
        >>> value = cache.get("key1")  # Returns 42, records hit
        >>> value = cache.get("key2")  # Returns None, records miss
        >>> print(cache.stats.hit_ratio)  # 0.5
    """

    def __init__(
        self,
        max_size: int = 1000,
        ttl_seconds: Optional[float] = None,
        name: str = "cache",
    ) -> None:
        """
        Initialize LRU cache.

        Args:
            max_size: Maximum number of items (excluding pinned)
            ttl_seconds: Optional TTL for entries (None = no expiration)
            name: Name for logging/debugging
        """
        self._max_size = max_size
        self._ttl_seconds = ttl_seconds
        self._name = name

        self._cache: OrderedDict[K, CacheEntry[V]] = OrderedDict()
        self._pinned: dict[K, CacheEntry[V]] = {}
        self._stats = CacheStats()
        self._delta_stats = CacheStats()
        self._lock = threading.RLock()

    @property
    def stats(self) -> CacheStats:
        """Get cache statistics."""
        return self._stats

    @property
    def size(self) -> int:
        """Current number of items (including pinned)."""
        with self._lock:
            return len(self._cache) + len(self._pinned)

    @property
    def capacity(self) -> int:
        """Maximum capacity."""
        return self._max_size

    @property
    def usage(self) -> float:
        """Current usage ratio (0.0 to 1.0)."""
        if self._max_size == 0:
            return 1.0
        return min(1.0, len(self._cache) / self._max_size)

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """
        Get a value from the cache.

        Updates LRU order and records hit/miss.

        Args:
            key: Cache key
            default: Default value if key not found

        Returns:
            Cached value or default
        """
        with self._lock:
            # Check pinned first
            if key in self._pinned:
                entry = self._pinned[key]
                if not self._is_expired(entry):
                    entry.touch()
                    self._record_hit()
                    return entry.value
                else:
                    # Remove expired pinned item
                    del self._pinned[key]

            # Check regular cache
            if key in self._cache:
                entry = self._cache[key]
                if not self._is_expired(entry):
                    entry.touch()
                    # Move to end (most recently used)
                    self._cache.move_to_end(key)
                    self._record_hit()
                    return entry.value
                else:
                    # Remove expired item
                    del self._cache[key]

            self._record_miss()
            return default

    def put(self, key: K, value: V, pinned: bool = False) -> None:
        """
        Put a value in the cache.

        Args:
            key: Cache key
            value: Value to cache
            pinned: If True, item won't be evicted
        """
        with self._lock:
            entry = CacheEntry(value=value, pinned=pinned)

            # Remove from other dict if exists
            if key in self._cache:
                del self._cache[key]
            if key in self._pinned:
                del self._pinned[key]

            if pinned:
                self._pinned[key] = entry
                self._stats.pins += 1
            else:
                self._cache[key] = entry
                self._cache.move_to_end(key)
                self._evict_if_needed()

    def touch(self, key: K) -> bool:
        """
        Update access time without retrieving value.

        Args:
            key: Cache key

        Returns:
            True if key exists and was touched
        """
        with self._lock:
            if key in self._pinned:
                self._pinned[key].touch()
                return True
            if key in self._cache:
                self._cache[key].touch()
                self._cache.move_to_end(key)
                return True
            return False

    def pin(self, key: K) -> bool:
        """
        Pin an existing item so it won't be evicted.

        Args:
            key: Cache key

        Returns:
            True if item was found and pinned
        """
        with self._lock:
            if key in self._pinned:
                return True  # Already pinned

            if key in self._cache:
                entry = self._cache.pop(key)
                entry.pinned = True
                self._pinned[key] = entry
                self._stats.pins += 1
                return True

            return False

    def unpin(self, key: K) -> bool:
        """
        Unpin an item so it can be evicted.

        Args:
            key: Cache key

        Returns:
            True if item was found and unpinned
        """
        with self._lock:
            if key not in self._pinned:
                return False

            entry = self._pinned.pop(key)
            entry.pinned = False
            self._cache[key] = entry
            self._cache.move_to_end(key)
            self._evict_if_needed()
            return True

    def delete(self, key: K) -> bool:
        """
        Delete an item from the cache.

        Args:
            key: Cache key

        Returns:
            True if item was deleted
        """
        with self._lock:
            if key in self._pinned:
                del self._pinned[key]
                return True
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def contains(self, key: K) -> bool:
        """Check if key exists (without updating LRU)."""
        with self._lock:
            return key in self._cache or key in self._pinned

    def clear(self, include_pinned: bool = False) -> int:
        """
        Clear the cache.

        Args:
            include_pinned: If True, also clear pinned items

        Returns:
            Number of items cleared
        """
        with self._lock:
            count = len(self._cache)
            self._cache.clear()

            if include_pinned:
                count += len(self._pinned)
                self._pinned.clear()

            return count

    def keys(self) -> list[K]:
        """Get all keys (including pinned)."""
        with self._lock:
            return list(self._cache.keys()) + list(self._pinned.keys())

    def get_delta_stats(self) -> CacheStats:
        """
        Get statistics since last delta check and reset delta.

        Useful for periodic monitoring.
        """
        with self._lock:
            delta = CacheStats(
                hits=self._stats.hits - self._delta_stats.hits,
                misses=self._stats.misses - self._delta_stats.misses,
                evictions=self._stats.evictions - self._delta_stats.evictions,
                pins=self._stats.pins - self._delta_stats.pins,
            )
            # Update delta baseline
            self._delta_stats = CacheStats(
                hits=self._stats.hits,
                misses=self._stats.misses,
                evictions=self._stats.evictions,
                pins=self._stats.pins,
            )
            return delta

    def info(self) -> dict:
        """Get comprehensive cache information."""
        with self._lock:
            return {
                'name': self._name,
                'size': self.size,
                'capacity': self._max_size,
                'usage': round(self.usage, 4),
                'pinned_count': len(self._pinned),
                'ttl_seconds': self._ttl_seconds,
                'stats': self._stats.to_dict(),
            }

    def _record_hit(self) -> None:
        """Record a cache hit."""
        self._stats.hits += 1

    def _record_miss(self) -> None:
        """Record a cache miss."""
        self._stats.misses += 1

    def _is_expired(self, entry: CacheEntry[V]) -> bool:
        """Check if an entry has expired."""
        if self._ttl_seconds is None:
            return False
        return (time.time() - entry.created_at) > self._ttl_seconds

    def _evict_if_needed(self) -> None:
        """Evict oldest items if over capacity."""
        while len(self._cache) > self._max_size:
            # Pop from the front (oldest)
            self._cache.popitem(last=False)
            self._stats.evictions += 1

    def __len__(self) -> int:
        return self.size

    def __contains__(self, key: K) -> bool:
        return self.contains(key)

    def __repr__(self) -> str:
        return f"LRUCache(name={self._name}, size={self.size}/{self._max_size}, hit_ratio={self._stats.hit_ratio:.2%})"


class TTLLRUCache(LRUCache[K, V]):
    """
    LRU Cache with mandatory TTL.

    Convenience class for caches that always need TTL.
    """

    def __init__(
        self,
        max_size: int = 1000,
        ttl_seconds: float = 300.0,  # 5 minutes default
        name: str = "ttl_cache",
    ) -> None:
        super().__init__(max_size=max_size, ttl_seconds=ttl_seconds, name=name)


__all__ = [
    'LRUCache',
    'TTLLRUCache',
    'CacheStats',
    'CacheEntry',
]
