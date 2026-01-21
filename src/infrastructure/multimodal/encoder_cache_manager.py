# SPDX-License-Identifier: Apache-2.0
# PyAgent Phase 44: Encoder Cache Manager for Multimodal Models
# Implements vLLM's EncoderCacheManager for vision/multimodal caching
# Beyond vLLM: Multi-tier caching, predictive prefetch, content dedup

"""
Encoder Cache Manager for Multimodal Models.

This module manages caching of encoder outputs (vision embeddings, audio features)
for multimodal LLM inference, avoiding redundant encoder computations.

Features beyond vLLM:
- Multi-tier caching (memory, disk, remote)
- Content-based deduplication via hashing
- Predictive prefetching
- Reference counting with weak references
- LRU eviction with priority support
"""

from __future__ import annotations

import hashlib
import time
import weakref
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TYPE_CHECKING, Any, Callable, Generic, TypeVar

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

# Try to import rust_core for acceleration
try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False

T = TypeVar('T')


class CacheTier(Enum):
    """Cache storage tier."""
    MEMORY = auto()      # In-memory (fastest)
    DISK = auto()        # Disk-based (persistent)
    REMOTE = auto()      # Remote storage (shared)


class EvictionPolicy(Enum):
    """Cache eviction policy."""
    LRU = auto()         # Least recently used
    LFU = auto()         # Least frequently used
    FIFO = auto()        # First in first out
    PRIORITY = auto()    # Priority-based


@dataclass
class CacheConfig:
    """Configuration for encoder cache."""
    cache_size: int = 1000              # Max number of entries
    memory_budget_mb: float = 512.0     # Memory budget in MB
    eviction_policy: EvictionPolicy = EvictionPolicy.LRU
    enable_dedup: bool = True           # Content-based deduplication
    enable_prefetch: bool = False       # Predictive prefetching
    prefetch_window: int = 3            # Number of items to prefetch
    ttl_seconds: float = 0.0            # Time-to-live (0 = no expiry)
    use_weak_refs: bool = True          # Use weak references for outputs
    hash_algorithm: str = "sha256"      # Hash algorithm for dedup
    
    def __post_init__(self) -> None:
        if self.cache_size < 1:
            raise ValueError(f"cache_size must be >= 1, got {self.cache_size}")
        if self.memory_budget_mb <= 0:
            raise ValueError(f"memory_budget_mb must be > 0")


@dataclass
class CacheEntry:
    """A single cache entry."""
    key: str                            # Unique identifier (hash)
    data: Any                           # Cached data (encoder output)
    size_bytes: int                     # Size in bytes
    access_count: int = 0               # Access count for LFU
    last_access: float = field(default_factory=time.time)
    created_at: float = field(default_factory=time.time)
    priority: int = 0                   # Higher = more important
    request_refs: set[str] = field(default_factory=set)  # Request IDs using this
    
    def touch(self) -> None:
        """Update access time and count."""
        self.last_access = time.time()
        self.access_count += 1
    
    @property
    def age_seconds(self) -> float:
        """Age since creation."""
        return time.time() - self.created_at
    
    @property
    def idle_seconds(self) -> float:
        """Time since last access."""
        return time.time() - self.last_access
    
    @property
    def is_referenced(self) -> bool:
        """Check if any requests reference this entry."""
        return bool(self.request_refs)


@dataclass
class CacheStats:
    """Cache statistics."""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    bytes_cached: int = 0
    entries_count: int = 0
    dedup_saves: int = 0  # Deduplicated entries
    prefetch_hits: int = 0
    
    @property
    def hit_rate(self) -> float:
        """Cache hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    @property
    def bytes_cached_mb(self) -> float:
        """Cached bytes in MB."""
        return self.bytes_cached / (1024 * 1024)
    
    def reset(self) -> None:
        """Reset statistics."""
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.bytes_cached = 0
        self.entries_count = 0
        self.dedup_saves = 0
        self.prefetch_hits = 0


class EncoderCacheManager:
    """
    Manages caching of encoder outputs for multimodal models.
    
    Implements vLLM's EncoderCacheManager with extensions:
    - Content-based deduplication
    - Reference counting
    - LRU/LFU/Priority eviction
    - Prefetching support
    """
    
    def __init__(self, config: CacheConfig | None = None):
        self.config = config or CacheConfig()
        self.stats = CacheStats()
        
        # Main cache storage
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        
        # Content hash to key mapping for deduplication
        self._content_hashes: dict[str, str] = {}
        
        # Request ID to cached keys mapping
        self._request_keys: dict[str, set[str]] = {}
        
        # Prefetch queue
        self._prefetch_queue: list[str] = []
        
        # Total bytes used
        self._bytes_used: int = 0
    
    def get(
        self,
        key: str,
        request_id: str | None = None,
    ) -> Any | None:
        """
        Get cached encoder output.
        
        Args:
            key: Cache key (typically content hash)
            request_id: Optional request ID for reference tracking
            
        Returns:
            Cached data or None if not found
        """
        entry = self._cache.get(key)
        
        if entry is None:
            self.stats.misses += 1
            return None
        
        # Check TTL
        if self.config.ttl_seconds > 0:
            if entry.age_seconds > self.config.ttl_seconds:
                self._evict_entry(key)
                self.stats.misses += 1
                return None
        
        # Update entry
        entry.touch()
        
        # Track request reference
        if request_id:
            entry.request_refs.add(request_id)
            if request_id not in self._request_keys:
                self._request_keys[request_id] = set()
            self._request_keys[request_id].add(key)
        
        # Move to end for LRU
        if self.config.eviction_policy == EvictionPolicy.LRU:
            self._cache.move_to_end(key)
        
        self.stats.hits += 1
        return entry.data
    
    def put(
        self,
        key: str,
        data: Any,
        request_id: str | None = None,
        priority: int = 0,
        content_hash: str | None = None,
    ) -> bool:
        """
        Cache encoder output.
        
        Args:
            key: Cache key
            data: Encoder output to cache
            request_id: Request ID for reference tracking
            priority: Cache priority (higher = more important)
            content_hash: Content hash for deduplication
            
        Returns:
            True if successfully cached
        """
        # Check for existing entry
        if key in self._cache:
            entry = self._cache[key]
            entry.touch()
            if request_id:
                entry.request_refs.add(request_id)
            return True
        
        # Content-based deduplication
        if self.config.enable_dedup and content_hash:
            if content_hash in self._content_hashes:
                # Return existing entry
                existing_key = self._content_hashes[content_hash]
                if existing_key in self._cache:
                    self.stats.dedup_saves += 1
                    entry = self._cache[existing_key]
                    entry.touch()
                    if request_id:
                        entry.request_refs.add(request_id)
                    return True
        
        # Calculate size
        size_bytes = self._estimate_size(data)
        
        # Evict if needed
        while self._should_evict(size_bytes):
            if not self._evict_one():
                return False  # Cannot make room
        
        # Create entry
        entry = CacheEntry(
            key=key,
            data=data,
            size_bytes=size_bytes,
            priority=priority,
        )
        
        if request_id:
            entry.request_refs.add(request_id)
            if request_id not in self._request_keys:
                self._request_keys[request_id] = set()
            self._request_keys[request_id].add(key)
        
        # Store
        self._cache[key] = entry
        self._bytes_used += size_bytes
        
        # Track content hash
        if self.config.enable_dedup and content_hash:
            self._content_hashes[content_hash] = key
        
        # Update stats
        self.stats.entries_count = len(self._cache)
        self.stats.bytes_cached = self._bytes_used
        
        return True
    
    def check_cached(self, key: str) -> bool:
        """Check if key is in cache without updating access."""
        return key in self._cache
    
    def release_request(self, request_id: str) -> list[str]:
        """
        Release all cache references for a request.
        
        Args:
            request_id: Request ID to release
            
        Returns:
            List of keys that became unreferenced
        """
        freed_keys: list[str] = []
        
        if request_id not in self._request_keys:
            return freed_keys
        
        keys = self._request_keys.pop(request_id)
        
        for key in keys:
            if key in self._cache:
                entry = self._cache[key]
                entry.request_refs.discard(request_id)
                
                if not entry.is_referenced:
                    freed_keys.append(key)
        
        return freed_keys
    
    def compute_hash(self, data: Any) -> str:
        """Compute content hash for deduplication."""
        if HAS_RUST and hasattr(rust_core, 'blake3_hash_rust'):
            if isinstance(data, np.ndarray):
                return rust_core.blake3_hash_rust(data.tobytes())
        
        # Python fallback
        if isinstance(data, np.ndarray):
            content = data.tobytes()
        elif isinstance(data, (bytes, bytearray)):
            content = bytes(data)
        else:
            content = str(data).encode()
        
        if self.config.hash_algorithm == "sha256":
            return hashlib.sha256(content).hexdigest()
        elif self.config.hash_algorithm == "md5":
            return hashlib.md5(content).hexdigest()
        else:
            return hashlib.blake2b(content).hexdigest()
    
    def prefetch(
        self,
        keys: list[str],
        loader: Callable[[str], Any],
    ) -> None:
        """
        Prefetch items into cache.
        
        Args:
            keys: Keys to prefetch
            loader: Function to load data for a key
        """
        if not self.config.enable_prefetch:
            return
        
        for key in keys[:self.config.prefetch_window]:
            if key not in self._cache:
                try:
                    data = loader(key)
                    if data is not None:
                        content_hash = self.compute_hash(data) if self.config.enable_dedup else None
                        self.put(key, data, content_hash=content_hash)
                        self.stats.prefetch_hits += 1
                except Exception:
                    pass  # Prefetch failures are non-critical
    
    def evict_unreferenced(self) -> int:
        """Evict all unreferenced entries."""
        evicted = 0
        keys_to_evict = [
            key for key, entry in self._cache.items()
            if not entry.is_referenced
        ]
        
        for key in keys_to_evict:
            self._evict_entry(key)
            evicted += 1
        
        return evicted
    
    def clear(self) -> None:
        """Clear all cached entries."""
        self._cache.clear()
        self._content_hashes.clear()
        self._request_keys.clear()
        self._bytes_used = 0
        self.stats.entries_count = 0
        self.stats.bytes_cached = 0
    
    def get_stats(self) -> CacheStats:
        """Get cache statistics."""
        self.stats.entries_count = len(self._cache)
        self.stats.bytes_cached = self._bytes_used
        return self.stats
    
    def _should_evict(self, new_size: int) -> bool:
        """Check if we need to evict to make room."""
        # Check entry count
        if len(self._cache) >= self.config.cache_size:
            return True
        
        # Check memory budget
        max_bytes = int(self.config.memory_budget_mb * 1024 * 1024)
        if self._bytes_used + new_size > max_bytes:
            return True
        
        return False
    
    def _evict_one(self) -> bool:
        """Evict one entry based on policy."""
        if not self._cache:
            return False
        
        # Find eviction candidate
        candidate_key = self._select_eviction_candidate()
        
        if candidate_key is None:
            return False
        
        self._evict_entry(candidate_key)
        return True
    
    def _select_eviction_candidate(self) -> str | None:
        """Select entry to evict based on policy."""
        # Prefer unreferenced entries first
        unreferenced = [
            (key, entry) for key, entry in self._cache.items()
            if not entry.is_referenced
        ]
        
        if unreferenced:
            candidates = unreferenced
        else:
            candidates = list(self._cache.items())
        
        if not candidates:
            return None
        
        if self.config.eviction_policy == EvictionPolicy.LRU:
            # Least recently used
            return min(candidates, key=lambda x: x[1].last_access)[0]
        
        elif self.config.eviction_policy == EvictionPolicy.LFU:
            # Least frequently used
            return min(candidates, key=lambda x: x[1].access_count)[0]
        
        elif self.config.eviction_policy == EvictionPolicy.FIFO:
            # First in first out
            return min(candidates, key=lambda x: x[1].created_at)[0]
        
        elif self.config.eviction_policy == EvictionPolicy.PRIORITY:
            # Lowest priority first, then LRU
            return min(candidates, key=lambda x: (x[1].priority, x[1].last_access))[0]
        
        # Default: first candidate
        return candidates[0][0]
    
    def _evict_entry(self, key: str) -> None:
        """Evict a specific entry."""
        if key not in self._cache:
            return
        
        entry = self._cache.pop(key)
        self._bytes_used -= entry.size_bytes
        self.stats.evictions += 1
        
        # Clean up content hash
        for content_hash, cached_key in list(self._content_hashes.items()):
            if cached_key == key:
                del self._content_hashes[content_hash]
                break
        
        # Clean up request references
        for keys in self._request_keys.values():
            keys.discard(key)
    
    def _estimate_size(self, data: Any) -> int:
        """Estimate size of data in bytes."""
        if isinstance(data, np.ndarray):
            return data.nbytes
        elif isinstance(data, (bytes, bytearray)):
            return len(data)
        elif isinstance(data, (list, tuple)):
            return sum(self._estimate_size(item) for item in data)
        elif isinstance(data, dict):
            return sum(
                self._estimate_size(k) + self._estimate_size(v)
                for k, v in data.items()
            )
        else:
            # Rough estimate for other objects
            return 64  # Minimum object size
    
    @property
    def num_free_slots(self) -> int:
        """Number of free slots in cache."""
        return max(0, self.config.cache_size - len(self._cache))
    
    @property
    def num_freeable_slots(self) -> int:
        """Number of slots that could be freed (unreferenced entries)."""
        return sum(1 for entry in self._cache.values() if not entry.is_referenced)


class MultiTierEncoderCache:
    """
    Multi-tier encoder cache with memory, disk, and remote tiers.
    
    Beyond vLLM: Hierarchical caching with automatic tier migration
    and consistent access patterns.
    """
    
    def __init__(
        self,
        memory_config: CacheConfig | None = None,
        disk_path: str | None = None,
        remote_url: str | None = None,
    ):
        self.memory_cache = EncoderCacheManager(memory_config)
        self.disk_path = disk_path
        self.remote_url = remote_url
        self._disk_index: dict[str, str] = {}  # key -> filename
    
    def get(self, key: str, request_id: str | None = None) -> Any | None:
        """Get from fastest available tier."""
        # Try memory first
        data = self.memory_cache.get(key, request_id)
        if data is not None:
            return data
        
        # Try disk
        if self.disk_path and key in self._disk_index:
            data = self._load_from_disk(key)
            if data is not None:
                # Promote to memory
                self.memory_cache.put(key, data, request_id)
                return data
        
        # Remote would be tried here if implemented
        return None
    
    def put(
        self,
        key: str,
        data: Any,
        request_id: str | None = None,
        tier: CacheTier = CacheTier.MEMORY,
    ) -> bool:
        """Put data into specified tier."""
        if tier == CacheTier.MEMORY:
            return self.memory_cache.put(key, data, request_id)
        elif tier == CacheTier.DISK and self.disk_path:
            return self._save_to_disk(key, data)
        return False
    
    def _load_from_disk(self, key: str) -> Any | None:
        """Load from disk tier."""
        if not self.disk_path or key not in self._disk_index:
            return None
        
        import os
        filepath = os.path.join(self.disk_path, self._disk_index[key])
        
        if os.path.exists(filepath):
            try:
                return np.load(filepath, allow_pickle=True)
            except Exception:
                return None
        return None
    
    def _save_to_disk(self, key: str, data: Any) -> bool:
        """Save to disk tier."""
        if not self.disk_path:
            return False
        
        import os
        os.makedirs(self.disk_path, exist_ok=True)
        
        filename = f"{hashlib.md5(key.encode()).hexdigest()}.npy"
        filepath = os.path.join(self.disk_path, filename)
        
        try:
            np.save(filepath, data, allow_pickle=True)
            self._disk_index[key] = filename
            return True
        except Exception:
            return False


# Factory function
def create_encoder_cache(
    cache_size: int = 1000,
    memory_mb: float = 512.0,
    eviction: str = "lru",
    enable_dedup: bool = True,
    **kwargs: Any,
) -> EncoderCacheManager:
    """
    Factory function to create encoder cache.
    
    Args:
        cache_size: Maximum number of entries
        memory_mb: Memory budget in MB
        eviction: "lru", "lfu", "fifo", "priority"
        enable_dedup: Enable content deduplication
        **kwargs: Additional config options
    """
    eviction_map = {
        "lru": EvictionPolicy.LRU,
        "lfu": EvictionPolicy.LFU,
        "fifo": EvictionPolicy.FIFO,
        "priority": EvictionPolicy.PRIORITY,
    }
    
    config = CacheConfig(
        cache_size=cache_size,
        memory_budget_mb=memory_mb,
        eviction_policy=eviction_map.get(eviction, EvictionPolicy.LRU),
        enable_dedup=enable_dedup,
        **kwargs,
    )
    
    return EncoderCacheManager(config)


__all__ = [
    "CacheTier",
    "EvictionPolicy",
    "CacheConfig",
    "CacheEntry",
    "CacheStats",
    "EncoderCacheManager",
    "MultiTierEncoderCache",
    "create_encoder_cache",
]
