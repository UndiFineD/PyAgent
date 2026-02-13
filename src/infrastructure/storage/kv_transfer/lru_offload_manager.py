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
# See the License for the specific language governing permissions and
# limitations under the License.

"""
LRUOffloadManager: LRU-based KV Cache Offloading

Implements simple LRU (Least Recently Used) eviction policy
for KV cache offloading with optimizations for batch operations.

Key Features Beyond vLLM:
- Weighted LRU with size and access frequency factors
- Batch eviction optimization
- Prefetch hints integration
- Multi-tier LRU (hot/warm/cold)
- Async batch operations

Based on vLLM v1 patterns with PyAgent innovations.
"""

from __future__ import annotations

import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any

from src.infrastructure.storage.kv_transfer.arc_offload_manager import (
    Backend,
    BlockHash,
    BlockState,
    BlockStatus,
    LoadStoreSpec,
    OffloadingEvent,
    OffloadingManager,
    OffloadMedium,
    PrepareStoreOutput,
    SimpleBackend,
)


@dataclass(slots=True)
class LRUEntry:
    """Entry in LRU cache with metadata."""

    block: BlockStatus
    access_count: int = 1
    access_time: float = field(default_factory=time.time)
    size_weight: float = 1.0

    @property
    def priority(self) -> float:
        """Calculate eviction priority (lower = evict first)."""
        # Combine recency and frequency
        age = time.time() - self.access_time
        return self.access_count / max(1.0, age) * self.size_weight


class LRUOffloadManager(OffloadingManager):
    """
    LRU-based offloading manager.

    Simple but effective LRU eviction policy for KV cache offloading.
    Evicts least recently used blocks when space is needed.
    """

    def __init__(self, backend: Backend, enable_events: bool = False):
        self.backend = backend
        # block_hash -> BlockStatus (ordered by access time)
        self.blocks: OrderedDict[BlockHash, BlockStatus] = OrderedDict()
        self.events: list[OffloadingEvent] | None = [] if enable_events else None

        # Statistics
        self._hits = 0
        self._misses = 0
        self._evictions = 0

        self._lock = threading.Lock()

    def lookup(self, block_hashes: list[BlockHash]) -> int:
        """
        Look up blocks in cache.

        Returns consecutive hit count until first miss.
        """
        with self._lock:
            hit_count = 0
            for block_hash in block_hashes:
                block = self.blocks.get(block_hash)
                if block is None or not block.is_ready:
                    self._misses += 1
                    break
                hit_count += 1
                self._hits += 1
            return hit_count

    def prepare_load(self, block_hashes: list[BlockHash]) -> LoadStoreSpec:
        """Prepare to load blocks."""
        with self._lock:
            blocks = []
            for block_hash in block_hashes:
                block = self.blocks[block_hash]
                assert block.is_ready, f"Block {block_hash!r} not ready"
                block.ref_cnt += 1
                blocks.append(block)

            return self.backend.get_load_store_spec(list(block_hashes), blocks)

    def touch(self, block_hashes: list[BlockHash]) -> None:
        """Update access recency by moving to end of OrderedDict."""
        with self._lock:
            for block_hash in reversed(list(block_hashes)):
                if self.blocks.get(block_hash):
                    self.blocks.move_to_end(block_hash)

    def complete_load(self, block_hashes: list[BlockHash]) -> None:
        """Complete load, decrement ref counts."""
        with self._lock:
            for block_hash in block_hashes:
                block = self.blocks[block_hash]
                assert block.ref_cnt > 0
                block.ref_cnt -= 1

    def prepare_store(self, block_hashes: list[BlockHash]) -> PrepareStoreOutput | None:
        """Prepare to store blocks with LRU eviction."""
        with self._lock:
            # Filter already stored
            to_store = [h for h in block_hashes if h not in self.blocks]

            if not to_store:
                return PrepareStoreOutput(
                    block_hashes_to_store=[],
                    store_spec=self.backend.get_load_store_spec([], []),
                    block_hashes_evicted=[],
                )

            num_to_evict = len(to_store) - self.backend.get_num_free_blocks()
            evicted = []

            if num_to_evict > 0:
                # Evict LRU blocks (from front of OrderedDict)
                for block_hash, block in list(self.blocks.items()):
                    if block.ref_cnt == 0:
                        evicted.append(block_hash)
                        self.backend.free(self.blocks.pop(block_hash))
                        self._evictions += 1
                        num_to_evict -= 1
                        if num_to_evict == 0:
                            break
                else:
                    # Could not evict enough
                    return None

            # Record event
            if self.events is not None and evicted:
                self.events.append(
                    OffloadingEvent(
                        block_hashes=evicted,
                        block_size=self.backend.block_size,
                        medium=self.backend.medium,
                        removed=True,
                    )
                )

            # Allocate new blocks
            new_blocks = self.backend.allocate_blocks(to_store)
            assert len(new_blocks) == len(to_store)

            for block_hash, block in zip(to_store, new_blocks):
                self.blocks[block_hash] = block

            return PrepareStoreOutput(
                block_hashes_to_store=to_store,
                store_spec=self.backend.get_load_store_spec(to_store, new_blocks),
                block_hashes_evicted=evicted,
            )

    def complete_store(self, block_hashes: list[BlockHash]) -> None:
        """Mark blocks as ready after store completes."""
        with self._lock:
            for block_hash in block_hashes:
                if block_hash in self.blocks:
                    self.blocks[block_hash].state = BlockState.READY

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            total = self._hits + self._misses
            return {
                "size": len(self.blocks),
                "hit_rate": self._hits / max(1, total),
                "evictions": self._evictions,
            }

    def clear(self) -> None:
        """Clear all cached blocks."""
        with self._lock:
            for block in self.blocks.values():
                self.backend.free(block)
            self.blocks.clear()
            self._hits = 0
            self._misses = 0
            self._evictions = 0


class WeightedLRUManager(LRUOffloadManager):
    """
    Weighted LRU with access frequency consideration.

    Combines recency with access frequency for smarter eviction.
    """

    def __init__(self, backend: Backend, enable_events: bool = False, frequency_weight: float = 0.3):
        super().__init__(backend, enable_events)
        self.frequency_weight = frequency_weight
        # Track access counts
        self._access_counts: dict[BlockHash, int] = {}

    def touch(self, block_hashes: list[BlockHash]) -> None:
        """Update recency and increment access count."""
        with self._lock:
            for block_hash in reversed(list(block_hashes)):
                if block_hash in self.blocks:
                    self.blocks.move_to_end(block_hash)
                    self._access_counts[block_hash] = self._access_counts.get(block_hash, 0) + 1

    def prepare_store(self, block_hashes: list[BlockHash]) -> PrepareStoreOutput | None:
        """Store with weighted eviction."""
        with self._lock:
            to_store = [h for h in block_hashes if h not in self.blocks]

            if not to_store:
                return PrepareStoreOutput(
                    block_hashes_to_store=[],
                    store_spec=self.backend.get_load_store_spec([], []),
                    block_hashes_evicted=[],
                )

            num_to_evict = len(to_store) - self.backend.get_num_free_blocks()
            evicted = []

            if num_to_evict > 0:
                # Build priority queue for eviction
                candidates = []
                for i, (block_hash, block) in enumerate(self.blocks.items()):
                    if block.ref_cnt == 0:
                        access_count = self._access_counts.get(block_hash, 1)
                        # Lower priority = evict first
                        # Position in OrderedDict gives recency (lower = older)
                        priority = i + access_count * self.frequency_weight * len(self.blocks)
                        candidates.append((priority, block_hash))

                # Sort by priority (lowest first)
                candidates.sort()

                for _, block_hash in candidates:
                    if num_to_evict <= 0:
                        break
                    block = self.blocks.get(block_hash)
                    if block and block.ref_cnt == 0:
                        self.backend.free(self.blocks.pop(block_hash))
                        self._access_counts.pop(block_hash, None)
                        evicted.append(block_hash)
                        self._evictions += 1
                        num_to_evict -= 1

                if num_to_evict > 0:
                    return None

            if self.events is not None and evicted:
                self.events.append(
                    OffloadingEvent(
                        block_hashes=evicted,
                        block_size=self.backend.block_size,
                        medium=self.backend.medium,
                        removed=True,
                    )
                )

            new_blocks = self.backend.allocate_blocks(to_store)
            for block_hash, block in zip(to_store, new_blocks):
                self.blocks[block_hash] = block
                self._access_counts[block_hash] = 1

            return PrepareStoreOutput(
                block_hashes_to_store=to_store,
                store_spec=self.backend.get_load_store_spec(to_store, new_blocks),
                block_hashes_evicted=evicted,
            )


class TieredLRUManager:
    """
    Multi-tier LRU manager with hot/warm/cold tiers.

    Blocks are promoted through tiers based on access patterns.
    """

    def __init__(
        self,
        hot_backend: Backend,
        warm_backend: Backend,
        cold_backend: Backend | None = None,
        hot_ratio: float = 0.2,
        warm_ratio: float = 0.3,
    ):
        self.hot_manager = LRUOffloadManager(hot_backend, enable_events=True)
        self.warm_manager = LRUOffloadManager(warm_backend, enable_events=True)
        self.cold_manager = LRUOffloadManager(cold_backend) if cold_backend else None

        self.hot_ratio = hot_ratio
        self.warm_ratio = warm_ratio

        # Access tracking for promotion
        self._access_counts: dict[BlockHash, int] = {}
        self._promote_threshold = 3
        self._lock = threading.Lock()

    def lookup(self, block_hashes: list[BlockHash]) -> int:
        """Look up across all tiers."""
        # Try hot first
        hit_count = self.hot_manager.lookup(block_hashes)
        if hit_count == len(block_hashes):
            return hit_count

        # Try remaining in warm
        remaining = block_hashes[hit_count:]
        warm_hits = self.warm_manager.lookup(remaining)
        hit_count += warm_hits

        if hit_count == len(block_hashes) or not self.cold_manager:
            return hit_count

        # Try cold
        remaining = block_hashes[hit_count:]
        cold_hits = self.cold_manager.lookup(remaining)
        return hit_count + cold_hits

    def touch(self, block_hashes: list[BlockHash]) -> None:
        """Touch and potentially promote blocks."""
        with self._lock:
            for block_hash in block_hashes:
                self._access_counts[block_hash] = self._access_counts.get(block_hash, 0) + 1

                count = self._access_counts[block_hash]

                # Promote from cold to warm
                if self.cold_manager and block_hash in self.cold_manager.blocks:
                    if count >= self._promote_threshold // 2:
                        self._promote(block_hash, self.cold_manager, self.warm_manager)

                # Promote from warm to hot
                elif block_hash in self.warm_manager.blocks:
                    if count >= self._promote_threshold:
                        self._promote(block_hash, self.warm_manager, self.hot_manager)

                # Touch in current tier
                else:
                    self.hot_manager.touch([block_hash])
                    self.warm_manager.touch([block_hash])
                    if self.cold_manager:
                        self.cold_manager.touch([block_hash])

    def _promote(self, block_hash: BlockHash, from_manager: LRUOffloadManager, to_manager: LRUOffloadManager) -> None:
        """Promote block between tiers."""
        # This is a simplified promotion - actual implementation
        # would handle data transfer between backends

    def prepare_store(self, block_hashes: list[BlockHash]) -> PrepareStoreOutput | None:
        """Store in appropriate tier."""
        # New blocks go to warm tier first
        result = self.warm_manager.prepare_store(block_hashes)

        if result is None and self.cold_manager:
            # Try cold tier if warm is full
            result = self.cold_manager.prepare_store(block_hashes)

        return result

    def get_stats(self) -> dict[str, Any]:
        """Get stats for all tiers."""
        stats = {
            "hot": self.hot_manager.get_stats(),
            "warm": self.warm_manager.get_stats(),
        }
        if self.cold_manager:
            stats["cold"] = self.cold_manager.get_stats()
        return stats


class PrefetchingLRUManager(LRUOffloadManager):
    """
    LRU manager with prefetching support.

    Maintains prefetch hints to proactively load blocks.
    """

    def __init__(self, backend: Backend, enable_events: bool = False, prefetch_lookahead: int = 4):
        super().__init__(backend, enable_events)
        self.prefetch_lookahead = prefetch_lookahead

        # Prefetch queue
        self._prefetch_queue: list[BlockHash] = []
        self._prefetch_in_progress: set[BlockHash] = set()

    def hint_prefetch(self, block_hashes: list[BlockHash]) -> None:
        """Hint blocks that may be needed soon."""
        with self._lock:
            for block_hash in block_hashes[: self.prefetch_lookahead]:
                if block_hash not in self.blocks and block_hash not in self._prefetch_in_progress:
                    self._prefetch_queue.append(block_hash)

    def process_prefetch(self) -> list[BlockHash]:
        """Process pending prefetch requests."""
        with self._lock:
            to_prefetch = []
            while self._prefetch_queue and len(to_prefetch) < self.prefetch_lookahead:
                block_hash = self._prefetch_queue.pop(0)
                if block_hash not in self.blocks and block_hash not in self._prefetch_in_progress:
                    to_prefetch.append(block_hash)
                    self._prefetch_in_progress.add(block_hash)

            return to_prefetch

    def complete_prefetch(self, block_hashes: list[BlockHash]) -> None:
        """Mark prefetch as complete."""
        with self._lock:
            for block_hash in block_hashes:
                self._prefetch_in_progress.discard(block_hash)


class AsyncLRUManager:
    """Async wrapper for LRU offloading manager."""

    def __init__(self, manager: LRUOffloadManager):
        self.manager = manager

    async def lookup_async(self, block_hashes: list[BlockHash]) -> int:
        """Async lookup."""
        import asyncio

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.manager.lookup, block_hashes)

    async def prepare_load_async(self, block_hashes: list[BlockHash]) -> LoadStoreSpec:
        """Async prepare load."""
        import asyncio

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.manager.prepare_load, block_hashes)

    async def prepare_store_async(self, block_hashes: list[BlockHash]) -> PrepareStoreOutput | None:
        """Async prepare store."""
        import asyncio

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.manager.prepare_store, block_hashes)

    async def touch_async(self, block_hashes: list[BlockHash]) -> None:
        """Async touch."""
        import asyncio

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.manager.touch, block_hashes)


class LRUManagerFactory:
    """Factory for creating LRU managers."""

    @staticmethod
    def create_simple(num_blocks: int = 1000, block_size: int = 16) -> LRUOffloadManager:
        """Create simple LRU manager."""
        backend = SimpleBackend(num_blocks=num_blocks, block_size=block_size)
        return LRUOffloadManager(backend)

    @staticmethod
    def create_weighted(
        num_blocks: int = 1000, block_size: int = 16, frequency_weight: float = 0.3
    ) -> WeightedLRUManager:
        """Create weighted LRU manager."""
        backend = SimpleBackend(num_blocks=num_blocks, block_size=block_size)
        return WeightedLRUManager(backend, frequency_weight=frequency_weight)

    @staticmethod
    def create_tiered(
        hot_blocks: int = 200, warm_blocks: int = 500, cold_blocks: int = 1000, block_size: int = 16
    ) -> TieredLRUManager:
        """Create tiered LRU manager."""
        hot = SimpleBackend(hot_blocks, block_size, OffloadMedium.GPU)
        warm = SimpleBackend(warm_blocks, block_size, OffloadMedium.CPU)
        cold = SimpleBackend(cold_blocks, block_size, OffloadMedium.DISK)
        return TieredLRUManager(hot, warm, cold)

    @staticmethod
    def create_prefetching(
        num_blocks: int = 1000, block_size: int = 16, prefetch_lookahead: int = 4
    ) -> PrefetchingLRUManager:
        """Create prefetching LRU manager."""
        backend = SimpleBackend(num_blocks=num_blocks, block_size=block_size)
        return PrefetchingLRUManager(backend, prefetch_lookahead=prefetch_lookahead)
