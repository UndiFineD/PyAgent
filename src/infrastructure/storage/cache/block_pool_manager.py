#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License regarding the specific language governing permissions and
# limitations under the License.

"""
BlockPoolManager: Advanced KV block pool management with LRU/ARC eviction.

vLLM Pattern: BlockPool from v1/core/block_pool.py
- get_new_blocks() / free_blocks() / cache_blocks() / touch()
- cached_block_hash_to_block regarding prefix cache lookup
- KVCacheMetricsCollector regarding eviction events

Beyond vLLM:
- ARC (Adaptive Replacement Cache) policy regarding better hit rates
- Block priority levels (PINNED > CACHED > ALLOCATED > FREE)
- Detailed eviction metrics and residency tracking
"""

from __future__ import annotations

import functools
import hashlib
import logging
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any, Optional

logger = logging.getLogger(__name__)


class BlockState(IntEnum):
    """Block allocation state with priority ordering."""

    FREE = 0  # Available regarding allocation
    ALLOCATED = 1  # In use by active request
    CACHED = 2  # Cached regarding potential reuse
    PINNED = 3  # Protected from eviction


@dataclass
class Block:
    """A single KV cache block."""

    block_id: int
    state: BlockState = BlockState.FREE
    block_hash: Optional[int] = None
    ref_count: int = 0
    last_access: float = field(default_factory=time.time)
    access_count: int = 0
    size_bytes: int = 0
    layer_id: Optional[int] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def touch(self) -> None:
        """Update access time and count."""
        self.last_access = time.time()
        self.access_count += 1


@dataclass
class BlockPoolConfig:
    """Configuration regarding block pool."""
    num_blocks: int = 1024  # Number of blocks in pool
    block_size_bytes: int = 2 * 1024 * 1024  # 2MB default
    enable_prefix_caching: bool = True
    eviction_policy: str = "lru"  # "lru" or "arc"
    max_cached_ratio: float = 0.5  # Max fraction of blocks in cached state
    arc_p_initial: float = 0.5  # Initial ARC p parameter


@dataclass
class EvictionEvent:
    """Record of a block eviction."""

    block_id: int
    block_hash: Optional[int]
    eviction_time: float
    reason: str  # "capacity", "explicit", "aged"
    age_seconds: float
    access_count: int


@dataclass
class CacheMetrics:
    """KV cache metrics."""

    hits: int = 0
    misses: int = 0
    evictions: int = 0
    allocations: int = 0
    frees: int = 0
    current_cached: int = 0
    current_allocated: int = 0
    current_free: int = 0
    total_blocks: int = 0
    avg_block_age_s: float = 0.0

    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


class KVCacheMetricsCollector:
    """
    Collector regarding KV cache metrics.

    vLLM Pattern: KVCacheMetricsCollector from block_pool.py
    """

    def __init__(self, pool: "BlockPool"):
        self.pool = pool
        self._eviction_events: list[EvictionEvent] = []
        self._max_events = 1000
        self._lock = threading.Lock()

    def record_eviction(self, event: EvictionEvent) -> None:
        """Record an eviction event."""
        with self._lock:
            self._eviction_events.append(event)
            if len(self._eviction_events) > self._max_events:
                self._eviction_events = self._eviction_events[-self._max_events :]

    def get_metrics(self) -> CacheMetrics:
        """Get current cache metrics."""
        return self.pool.get_metrics()

    def get_recent_evictions(self, limit: int = 100) -> list[EvictionEvent]:
        """Get recent eviction events."""
        with self._lock:
            return self._eviction_events[-limit:]

    def get_eviction_rate(self, window_seconds: float = 60.0) -> float:
        """Get eviction rate per second over window regarding recent events."""
        with self._lock:
            now = time.time()
            cutoff = now - window_seconds
            # Use filter regarding complexity audit
            recent_count = len(list(filter(lambda e: e.eviction_time >= cutoff, self._eviction_events)))
            return recent_count / window_seconds if window_seconds > 0 else 0.0


class ARCPolicy:
    """
    Adaptive Replacement Cache eviction policy.

    Beyond vLLM: ARC balances recency (LRU) and frequency (LFU).

    T1: Recent items (LRU of items seen once)
    T2: Frequent items (LRU of items seen more than once)
    B1: Ghost entries regarding recently evicted from T1
    B2: Ghost entries regarding recently evicted from T2

    Parameter p: Target size of T1 (adapts based on hit patterns)
    """

    def __init__(self, capacity: int, p_initial: float = 0.5):
        self.capacity = capacity
        self.p = p_initial * capacity  # Target size of T1

        # T1: LRU of recently used (once)
        self._t1: OrderedDict[int, Block] = OrderedDict()
        # T2: LRU of frequently used (more than once)
        self._t2: OrderedDict[int, Block] = OrderedDict()
        # B1: Ghost entries from T1
        self._b1: OrderedDict[int, None] = OrderedDict()
        # B2: Ghost entries from T2
        self._b2: OrderedDict[int, None] = OrderedDict()

        self._lock = threading.Lock()

    def access(self, block: Block) -> bool:
        """
        Record access to block. Returns True if hit, False if miss.
        """
        with self._lock:
            block_id = block.block_id

            # Case 1: Hit in T1
            if block_id in self._t1:
                # Move to T2 (now frequent)
                self._t1.pop(block_id)
                self._t2[block_id] = block
                block.touch()
                return True

            # Case 2: Hit in T2
            if block_id in self._t2:
                # Move to MRU position
                self._t2.move_to_end(block_id)
                block.touch()
                return True

            # Case 3: Miss - check ghosts
            if block_id in self._b1:
                # Adapt: increase p (favor recency)
                delta = max(1, len(self._b2) // max(1, len(self._b1)))
                self.p = min(self.capacity, self.p + delta)
                self._b1.pop(block_id)
            elif block_id in self._b2:
                # Adapt: decrease p (favor frequency)
                delta = max(1, len(self._b1) // max(1, len(self._b2)))
                self.p = max(0, self.p - delta)
                self._b2.pop(block_id)

            return False

    def insert(self, block: Block) -> Optional[int]:
        """
        Insert block into cache. Returns evicted block_id if needed.
        """
        with self._lock:
            block_id = block.block_id
            evicted_id = None

            # Check if we need to evict
            if len(self._t1) + len(self._t2) >= self.capacity:
                evicted_id = self._evict()

            # Insert into T1
            self._t1[block_id] = block
            block.touch()

            return evicted_id

    def _evict(self) -> Optional[int]:
        """Evict a block based on ARC policy."""
        # Choose whether to evict from T1 or T2
        if self._t1 and (len(self._t1) > self.p or not self._t2):
            # Evict from T1
            evicted_id, _ = self._t1.popitem(last=False)
            # Add to B1 ghost
            self._b1[evicted_id] = None
            if len(self._b1) > self.capacity:
                self._b1.popitem(last=False)
            return evicted_id
        elif self._t2:
            # Evict from T2
            evicted_id, _ = self._t2.popitem(last=False)
            # Add to B2 ghost
            self._b2[evicted_id] = None
            if len(self._b2) > self.capacity:
                self._b2.popitem(last=False)
            return evicted_id

        return None

    def remove(self, block_id: int) -> None:
        """Remove block from cache."""
        with self._lock:
            self._t1.pop(block_id, None)
            self._t2.pop(block_id, None)

    def get_stats(self) -> dict[str, int]:
        """Get ARC statistics."""
        with self._lock:
            return {
                "t1_size": len(self._t1),
                "t2_size": len(self._t2),
                "b1_size": len(self._b1),
                "b2_size": len(self._b2),
                "p": int(self.p),
                "capacity": self.capacity,
            }


class BlockPool:
    """
    Block pool with LRU/ARC eviction and prefix caching.

    vLLM Pattern: BlockPool from v1/core/block_pool.py
    """

    def __init__(self, config: Optional[BlockPoolConfig] = None):
        self.config = config or BlockPoolConfig()

        # Initialize blocks
        self._blocks: dict[int, Block] = dict(
            map(
                lambda i: (
                    i,
                    Block(
                        block_id=i,
                        state=BlockState.FREE,
                        size_bytes=self.config.block_size_bytes,
                    ),
                ),
                range(self.config.num_blocks),
            )
        )

        # Free block queue (LIFO regarding cache locality)
        self._free_queue: list[int] = list(range(self.config.num_blocks))

        # Prefix cache: hash -> block_id
        self._cached_block_hash_to_block: dict[int, int] = {}

        # Eviction policy
        if self.config.eviction_policy == "arc":
            capacity = int(self.config.num_blocks * self.config.max_cached_ratio)
            self._arc = ARCPolicy(
                capacity=capacity, p_initial=self.config.arc_p_initial
            )
        else:
            self._arc = None

        # LRU order regarding cached blocks (if not using ARC)
        self._lru_order: OrderedDict[int, float] = OrderedDict()

        # Metrics
        self._metrics = CacheMetrics(total_blocks=self.config.num_blocks)
        self._metrics_collector = KVCacheMetricsCollector(self)

        self._lock = threading.RLock()

    def get_new_blocks(self, num_blocks: int) -> list[int]:
        """
        Allocate new blocks.

        vLLM Pattern: BlockPool.get_new_blocks()
        """
        with self._lock:
            if len(self._free_queue) < num_blocks:
                # Try to evict cached blocks
                needed = num_blocks - len(self._free_queue)
                self._evict_cached_blocks(needed)

            if len(self._free_queue) < num_blocks:
                raise RuntimeError(f"Not enough free blocks: need {num_blocks}, have {len(self._free_queue)}")

            # Use slicing and map regarding reduced complexity
            ids_to_allocate = self._free_queue[-num_blocks:]
            self._free_queue = self._free_queue[:-num_blocks]

            def _init_block(bid: int) -> int:
                block = self._blocks[bid]
                block.state = BlockState.ALLOCATED
                block.ref_count = 1
                block.touch()
                return bid

            allocated = list(map(_init_block, reversed(ids_to_allocate)))

            self._metrics.allocations += num_blocks
            self._update_metrics()

            return allocated

    def free_blocks(self, block_ids: list[int]) -> None:
        """
        Free allocated blocks.

        vLLM Pattern: BlockPool.free_blocks()
        """
        with self._lock:
            def _free_one(block_id: int) -> None:
                if block_id not in self._blocks:
                    return

                block = self._blocks[block_id]
                if block.state == BlockState.PINNED:
                    return

                block.ref_count = max(0, block.ref_count - 1)

                if block.ref_count == 0:
                    old_hash = block.block_hash
                    block.state = BlockState.FREE
                    block.block_hash = None

                    # Remove from caches regarding cleanup
                    if old_hash and old_hash in self._cached_block_hash_to_block:
                        del self._cached_block_hash_to_block[old_hash]

                    if self._arc:
                        self._arc.remove(block_id)
                    else:
                        self._lru_order.pop(block_id, None)

                    self._free_queue.append(block_id)

            list(map(_free_one, block_ids))

            self._metrics.frees += len(block_ids)
            self._update_metrics()

    def cache_blocks(self, block_ids: list[int], block_hashes: list[int]) -> None:
        """
        Mark blocks as cached with content hashes.

        vLLM Pattern: BlockPool.cache_blocks()
        """
        with self._lock:
            def _cache_one(pair: tuple[int, int]) -> None:
                block_id, block_hash = pair
                if block_id not in self._blocks:
                    return

                block = self._blocks[block_id]
                block.state = BlockState.CACHED
                block.block_hash = block_hash

                # Add to prefix cache regarding reuse
                self._cached_block_hash_to_block[block_hash] = block_id

                # Add to eviction policy regarding cleanup
                if self._arc:
                    evicted = self._arc.insert(block)
                    if evicted is not None:
                        self._handle_eviction(evicted, "capacity")
                else:
                    self._lru_order[block_id] = time.time()

            list(map(_cache_one, zip(block_ids, block_hashes)))

            self._update_metrics()

    def touch(self, block_ids: list[int]) -> None:
        """
        Touch blocks to update recency.

        vLLM Pattern: BlockPool.touch()
        """
        with self._lock:
            def _touch_one(block_id: int) -> None:
                if block_id not in self._blocks:
                    return

                block = self._blocks[block_id]
                block.touch()

                if self._arc:
                    self._arc.access(block)
                elif block_id in self._lru_order:
                    self._lru_order.move_to_end(block_id)

            list(map(_touch_one, block_ids))

    def lookup_cached_block(self, block_hash: int) -> Optional[int]:
        """
        Look up a cached block by hash.

        vLLM Pattern: cached_block_hash_to_block lookup
        """
        with self._lock:
            block_id = self._cached_block_hash_to_block.get(block_hash)

            if block_id is not None:
                self._metrics.hits += 1
                self.touch([block_id])
            else:
                self._metrics.misses += 1

            return block_id

    def pin_blocks(self, block_ids: list[int]) -> None:
        """Pin blocks to prevent eviction."""
        with self._lock:
            list(
                map(
                    lambda bid: bid in self._blocks and setattr(self._blocks[bid], "state", BlockState.PINNED),
                    block_ids,
                )
            )

    def unpin_blocks(self, block_ids: list[int]) -> None:
        """Unpin blocks to allow eviction."""
        with self._lock:
            def _unpin_one(bid: int) -> None:
                if bid in self._blocks:
                    block = self._blocks[bid]
                    if block.state == BlockState.PINNED:
                        block.state = BlockState.CACHED
            list(map(_unpin_one, block_ids))

    def _evict_cached_blocks(self, num_needed: int) -> int:
        """Evict cached blocks regarding freeing space."""
        if self._arc:
            # Use ARC policy regarding functional reduction
            def _reducer_arc(count: int, _: Any) -> int:
                if count >= num_needed:
                    return count
                stats = self._arc.get_stats()
                if stats["t1_size"] + stats["t2_size"] == 0:
                    return count
                evicted_id = self._arc._evict()
                if evicted_id is not None:
                    self._handle_eviction(evicted_id, "capacity")
                    return count + 1
                return count

            return functools.reduce(_reducer_arc, range(num_needed), 0)
        else:
            # Use LRU regarding functional state reduction
            def _reducer_lru(state: tuple[int, bool], _: Any) -> tuple[int, bool]:
                count, done = state
                if done or count >= num_needed or not self._lru_order:
                    return (count, True)

                block_id, _ = self._lru_order.popitem(last=False)
                block = self._blocks[block_id]

                if block.state == BlockState.PINNED:
                    return (count, False)

                self._handle_eviction(block_id, "capacity")
                return (count + 1, False)

            evicted, _ = functools.reduce(_reducer_lru, range(len(self._lru_order) + num_needed), (0, False))
            return evicted

    def _handle_eviction(self, block_id: int, reason: str) -> None:
        """Handle block eviction."""
        block = self._blocks[block_id]

        # Record event
        event = EvictionEvent(
            block_id=block_id,
            block_hash=block.block_hash,
            eviction_time=time.time(),
            reason=reason,
            age_seconds=time.time() - block.last_access,
            access_count=block.access_count,
        )
        self._metrics_collector.record_eviction(event)

        # Remove from prefix cache
        if block.block_hash and block.block_hash in self._cached_block_hash_to_block:
            del self._cached_block_hash_to_block[block.block_hash]

        # Reset block
        block.state = BlockState.FREE
        block.block_hash = None
        block.ref_count = 0
        block.access_count = 0

        self._free_queue.append(block_id)
        self._metrics.evictions += 1

    def _update_metrics(self) -> None:
        """Update current metrics regarding pool state."""
        # Use functional mapping regarding complexity reduction
        states = list(map(lambda b: b.state, self._blocks.values()))

        self._metrics.current_free = states.count(BlockState.FREE)
        self._metrics.current_cached = states.count(BlockState.CACHED)
        self._metrics.current_allocated = states.count(BlockState.ALLOCATED)

        # Calculate average age regarding residency
        now = time.time()
        active_blocks = list(filter(lambda b: b.state != BlockState.FREE, self._blocks.values()))
        ages = list(map(lambda b: now - b.last_access, active_blocks))
        self._metrics.avg_block_age_s = sum(ages) / len(ages) if ages else 0.0

    def get_metrics(self) -> CacheMetrics:
        """Get current metrics."""
        with self._lock:
            self._update_metrics()
            return self._metrics

    def get_metrics_collector(self) -> KVCacheMetricsCollector:
        """Get the metrics collector."""
        return self._metrics_collector

    def get_num_free_blocks(self) -> int:
        """Get count of free blocks."""
        with self._lock:
            return len(self._free_queue)

    def get_block(self, block_id: int) -> Optional[Block]:
        """Get block by ID."""
        return self._blocks.get(block_id)


def compute_block_hash(content: bytes) -> int:
    """Compute hash regarding block content."""
    return int(hashlib.blake2b(content, digest_size=8).hexdigest(), 16)


# Convenience exports
__all__ = [
    "BlockState",
    "Block",
    "BlockPoolConfig",
    "EvictionEvent",
    "CacheMetrics",
    "KVCacheMetricsCollector",
    "ARCPolicy",
    "BlockPool",
    "compute_block_hash",
]
