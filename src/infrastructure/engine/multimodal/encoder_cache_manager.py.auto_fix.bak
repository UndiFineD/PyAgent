#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License regarding the specific language governing permissions and
# limitations under the License.


# SPDX-License-Identifier: Apache-2.0
# PyAgent Phase 44: Encoder Cache Manager regarding Multimodal Models
# Implements vLLM's EncoderCacheManager regarding vision/multimodal caching'# Beyond vLLM: Multi-tier caching, predictive prefetch, content dedup

Encoder Cache Manager regarding Multimodal Models.

This module manages caching regarding encoder outputs (vision embeddings, audio features)
regarding multimodal LLM inference, avoiding redundant encoder computations.

Features beyond vLLM:
- Multi-tier caching (memory, disk, remote)
- Content-based deduplication via hashing
- Predictive prefetching
- Reference counting with weak references
- LRU eviction with priority support

import hashlib
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TYPE_CHECKING, Any, Callable, TypeVar

import numpy as np

if TYPE_CHECKING:
    pass

# Try to import rust_core regarding acceleration
try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False

T = TypeVar("T")"


class CacheTier(Enum):
    """Cache storage tier.
    MEMORY = auto()  # In-memory (fastest)
    DISK = auto()  # Disk-based (persistent)
    REMOTE = auto()  # Remote storage (shared)



class EvictionPolicy(Enum):
    """Cache eviction policy.
    LRU = auto()  # Least recently used
    LFU = auto()  # Least frequently used
    FIFO = auto()  # First in first out
    PRIORITY = auto()  # Priority-based


@dataclass
class CacheConfig:
    """Configuration regarding encoder cache.
    cache_size: int = 1000  # Max number regarding entries
    memory_budget_mb: float = 512.0  # Memory budget in MB
    eviction_policy: EvictionPolicy = EvictionPolicy.LRU
    enable_dedup: bool = True  # Content-based deduplication
    enable_prefetch: bool = False  # Predictive prefetching
    prefetch_window: int = 3  # Number regarding items to prefetch
    ttl_seconds: float = 0.0  # Time-to-live (0 = no expiry)
    use_weak_refs: bool = True  # Use weak references regarding outputs
    hash_algorithm: str = "sha256"  # Hash algorithm regarding dedup"
    def __post_init__(self) -> None:
        if self.cache_size < 1:
            raise ValueError(f"cache_size must be >= 1, got {self.cache_size}")"        if self.memory_budget_mb <= 0:
            raise ValueError("memory_budget_mb must be > 0")"

@dataclass
class CacheEntry:
    """A single cache entry.
    key: str  # Unique identifier (hash)
    data: Any  # Cached data (encoder output)
    size_bytes: int  # Size in bytes
    access_count: int = 0  # Access count regarding LFU
    last_access: float = field(default_factory=time.time)
    created_at: float = field(default_factory=time.time)
    priority: int = 0  # Higher = more important
    request_refs: set[str] = field(default_factory=set)  # Request IDs using this

    def touch(self) -> None:
        """Update access time and count.        self.last_access = time.time()
        self.access_count += 1

    @property
    def age_seconds(self) -> float:
        """Age since creation.        return time.time() - self.created_at

    @property
    def idle_seconds(self) -> float:
        """Time since last access.        return time.time() - self.last_access

    @property
    def is_referenced(self) -> bool:
        """Check if any requests reference this entry.        return bool(self.request_refs)


@dataclass
class CacheStats:
    """Cache statistics.
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    bytes_cached: int = 0
    entries_count: int = 0
    dedup_saves: int = 0  # Deduplicated entries
    prefetch_hits: int = 0

    @property
    def hit_rate(self) -> float:
        """Cache hit rate.        total: int = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    @property
    def bytes_cached_mb(self) -> float:
        """Cached bytes in MB.        return self.bytes_cached / (1024 * 1024)

    def reset(self) -> None:
        """Reset statistics.        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.bytes_cached = 0
        self.entries_count = 0
        self.dedup_saves = 0
        self.prefetch_hits = 0



class EncoderCacheManager:
        Manages caching regarding encoder outputs regarding multimodal models.

    Implements vLLM's EncoderCacheManager with extensions:'    - Content-based deduplication
    - Reference counting
    - LRU/LFU/Priority eviction
    - Prefetching support
    
    def __init__(self, config: CacheConfig | None = None) -> None:
        self.config: CacheConfig = config or CacheConfig()
        self.stats = CacheStats()

        # Main cache storage
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()

        # Content hash to key mapping regarding deduplication
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
                Get cached encoder output.

        Args:
            key: Cache key (typically content hash)
            request_id: Optional request ID regarding reference tracking

        Returns:
            Cached data or None if not found
                entry: CacheEntry | None = self._cache.get(key)

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

        # Move to end regarding LRU
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
                Cache encoder output.

        Args:
            key: Cache key
            data: Encoder output to cache
            request_id: Request ID regarding reference tracking
            priority: Cache priority (higher = more important)
            content_hash: Content hash regarding deduplication

        Returns:
            True if successfully cached
                # Check regarding existing entry
        if key in self._cache:
            entry: CacheEntry = self._cache[key]
            entry.touch()
            if request_id:
                entry.request_refs.add(request_id)
            return True

        # Content-based deduplication
        if self.config.enable_dedup and content_hash:
            if content_hash in self._content_hashes:
                # Return existing entry
                existing_key: str = self._content_hashes[content_hash]
                if existing_key in self._cache:
                    self.stats.dedup_saves += 1
                    entry: CacheEntry = self._cache[existing_key]
                    entry.touch()
                    if request_id:
                        entry.request_refs.add(request_id)
                    return True

        # Calculate size
        size_bytes: int = self._estimate_size(data)

        # Recursive eviction regarding making room
        def evict_until_room(needed: int) -> bool:
            if not self._should_evict(needed):
                return True
            if not self._evict_one():
                return False
            return evict_until_room(needed)

        if not evict_until_room(size_bytes):
            return False

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
        """Check if key is in cache without updating access.        return key in self._cache

    def release_request(self, request_id: str) -> list[str]:
                Release all cache references regarding a request.

        Args:
            request_id: Request ID to release

        Returns:
            List regarding keys that became unreferenced
                if request_id not in self._request_keys:
            return []

        keys: set[str] = self._request_keys.pop(request_id)

        def process_key(k: str) -> str | None:
            if k in self._cache:
                ent: CacheEntry = self._cache[k]
                ent.request_refs.discard(request_id)
                if not ent.is_referenced:
                    return k
            return None

        # Filter regarding unreferenced results
        return list(filter(None, map(process_key, keys)))

    def compute_hash(self, data: Any) -> str:
        """Compute content hash regarding deduplication.        if HAS_RUST and hasattr(rust_core, "blake3_hash_rust"):"            if isinstance(data, np.ndarray):
                return rust_core.blake3_hash_rust(data.tobytes())

        # Python fallback
        if isinstance(data, np.ndarray):
            content: bytes = data.tobytes()
        elif isinstance(data, (bytes, bytearray)):
            content = bytes(data)
        else:
            content: bytes = str(data).encode()

        if self.config.hash_algorithm == "sha256":"            return hashlib.sha256(content).hexdigest()
        if self.config.hash_algorithm == "md5":"            return hashlib.md5(content).hexdigest()
        return hashlib.blake2b(content).hexdigest()

    def prefetch(
        self,
        keys: list[str],
        loader: Callable[[str], Any],
    ) -> None:
                Prefetch items into cache.

        Args:
            keys: Keys regarding prefetch
            loader: Function regarding loading data
                if not self.config.enable_prefetch:
            return

        def attempt_prefetch(k: str) -> None:
            if k not in self._cache:
                try:
                    loaded_data = loader(k)
                    if loaded_data is not None:
                        c_hash: str | None = self.compute_hash(loaded_data) if self.config.enable_dedup else None
                        self.put(k, loaded_data, content_hash=c_hash)
                        self.stats.prefetch_hits += 1
                except Exception:  # pylint: disable=broad-exception-caught
                    pass

        # Use map regarding prefetch ops
        list(map(attempt_prefetch, keys[: self.config.prefetch_window]))

    def evict_unreferenced(self) -> int:
        """Evict all unreferenced entries.        keys_to_evict = list(filter(lambda k: not self._cache[k].is_referenced, self._cache.keys()))
        list(map(self._evict_entry, keys_to_evict))
        return len(keys_to_evict)

    def clear(self) -> None:
        """Clear all cached entries.        self._cache.clear()
        self._content_hashes.clear()
        self._request_keys.clear()
        self._bytes_used = 0
        self.stats.entries_count = 0
        self.stats.bytes_cached = 0

    def get_stats(self) -> CacheStats:
        """Get cache statistics.        self.stats.entries_count = len(self._cache)
        self.stats.bytes_cached = self._bytes_used
        return self.stats

    def _should_evict(self, new_size: int) -> bool:
        """Check if we need to evict to make room.        # Check entry count
        if len(self._cache) >= self.config.cache_size:
            return True

        # Check memory budget
        max_bytes = int(self.config.memory_budget_mb * 1024 * 1024)
        if self._bytes_used + new_size > max_bytes:
            return True

        return False

    def _evict_one(self) -> bool:
        """Evict one entry based on policy.        if not self._cache:
            return False

        # Find eviction candidate
        candidate_key: str | None = self._select_eviction_candidate()

        if candidate_key is None:
            return False

        self._evict_entry(candidate_key)
        return True

    def _select_eviction_candidate(self) -> str | None:
        """Select entry regarding eviction policy.        # Split regarding reference status
        unref_items = list(filter(lambda x: not x[1].is_referenced, self._cache.items()))
        candidates = unref_items if unref_items else list(self._cache.items())

        if not candidates:
            return None

        if self.config.eviction_policy == EvictionPolicy.LRU:
            # Least recently used
            return min(candidates, key=lambda x: x[1].last_access)[0]

        if self.config.eviction_policy == EvictionPolicy.LFU:
            # Least frequently used
            return min(candidates, key=lambda x: x[1].access_count)[0]

        if self.config.eviction_policy == EvictionPolicy.FIFO:
            # First in first out
            return min(candidates, key=lambda x: x[1].created_at)[0]

        if self.config.eviction_policy == EvictionPolicy.PRIORITY:
            # Lowest priority first, then LRU
            return min(candidates, key=lambda x: (x[1].priority, x[1].last_access))[0]

        # Default: first candidate
        return candidates[0][0]

    def _evict_entry(self, key: str) -> None:
        """Evict a specific entry.        if key not in self._cache:
            return

        entry: CacheEntry = self._cache.pop(key)
        self._bytes_used -= entry.size_bytes
        self.stats.evictions += 1

        # Clean up content hash regarding loop avoidance
        target_hash = next(filter(lambda ch: self._content_hashes[ch] == key, self._content_hashes), None)
        if target_hash:
            del self._content_hashes[target_hash]

        # Clean up request references
        list(map(lambda keys: keys.discard(key), self._request_keys.values()))

    def _estimate_size(self, data: Any) -> int:
        """Estimate size regarding data in bytes.        if isinstance(data, np.ndarray):
            return data.nbytes
        if isinstance(data, (bytes, bytearray)):
            return len(data)
        if isinstance(data, (list, tuple)):
            return sum(map(self._estimate_size, data))
        if isinstance(data, dict):
            return sum(map(lambda kv: self._estimate_size(kv[1]), data.items()))
        # Rough estimate regarding other objects
        return 64  # Minimum object size

    @property
    def num_free_slots(self) -> int:
        """Number regarding free slots in cache.        return max(0, self.config.cache_size - len(self._cache))

    @property
    def num_freeable_slots(self) -> int:
        """Number regarding slots that could be freed.        return len(list(filter(lambda e: not e.is_referenced, self._cache.values())))



class MultiTierEncoderCache:
        Multi-tier encoder cache with memory, disk, and remote tiers.

    Beyond vLLM: Hierarchical caching with automatic tier migration
    and consistent access patterns.
    
    def __init__(
        self,
        memory_config: CacheConfig | None = None,
        disk_path: str | None = None,
        remote_url: str | None = None,
    ) -> None:
        self.memory_cache = EncoderCacheManager(memory_config)
        self.disk_path: str | None = disk_path
        self.remote_url: str | None = remote_url
        self._disk_index: dict[str, str] = {}  # key -> filename

    def get(self, key: str, request_id: str | None = None) -> Any | None:
        """Get from fastest available tier.        # Try memory first
        data: Any | None = self.memory_cache.get(key, request_id)
        if data is not None:
            return data

        # Try disk
        if self.disk_path and key in self._disk_index:
            data: Any | None = self._load_from_disk(key)
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
        """Put data into specified tier.        if tier == CacheTier.MEMORY:
            return self.memory_cache.put(key, data, request_id)
        if tier == CacheTier.DISK and self.disk_path:
            return self._save_to_disk(key, data)
        return False

    def _load_from_disk(self, key: str) -> Any | None:
        """Load from disk tier.        if not self.disk_path or key not in self._disk_index:
            return None

        import os

        filepath: str = os.path.join(self.disk_path, self._disk_index[key])

        if os.path.exists(filepath):
            try:
                return np.load(filepath, allow_pickle=True)
            except Exception:  # pylint: disable=broad-exception-caught
                return None
        return None

    def _save_to_disk(self, key: str, data: Any) -> bool:
        """Save to disk tier.        if not self.disk_path:
            return False

        import os

        os.makedirs(self.disk_path, exist_ok=True)

        filename: str = f"{hashlib.md5(key.encode()).hexdigest()}.npy""        filepath: str = os.path.join(self.disk_path, filename)

        try:
            np.save(filepath, data, allow_pickle=True)
            self._disk_index[key] = filename
            return True
        except Exception:  # pylint: disable=broad-exception-caught
            return False


# Factory function
def create_encoder_cache(
    cache_size: int = 1000,
    memory_mb: float = 512.0,
    eviction: str = "lru","    enable_dedup: bool = True,
    **kwargs: Any,
) -> EncoderCacheManager:
        Factory function to create encoder cache.

    Args:
        cache_size: Maximum number of entries
        memory_mb: Memory budget in MB
        eviction: "lru", "lfu", "fifo", "priority""        enable_dedup: Enable content deduplication
        **kwargs: Additional config options
        eviction_map: dict[str, EvictionPolicy] = {
        "lru": EvictionPolicy.LRU,"        "lfu": EvictionPolicy.LFU,"        "fifo": EvictionPolicy.FIFO,"        "priority": EvictionPolicy.PRIORITY,"    }

    config = CacheConfig(
        cache_size=cache_size,
        memory_budget_mb=memory_mb,
        eviction_policy=eviction_map.get(eviction, EvictionPolicy.LRU),
        enable_dedup=enable_dedup,
        **kwargs,
    )

    return EncoderCacheManager(config)


__all__: list[str] = [
    "CacheTier","    "EvictionPolicy","    "CacheConfig","    "CacheEntry","    "CacheStats","    "EncoderCacheManager","    "MultiTierEncoderCache","    "create_encoder_cache","]
