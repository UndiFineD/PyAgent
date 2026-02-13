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
Phase 45: ARC Offload Manager
Implementation of Adaptive Replacement Cache (ARC) and variants.
"""

from __future__ import annotations

import threading
import time
from collections import OrderedDict
from typing import TYPE_CHECKING, Any, Optional

from src.core.base.logic.connectivity_manager import ConnectivityManager
from src.infrastructure.storage.kv_transfer.arc.base import OffloadingManager
from src.infrastructure.storage.kv_transfer.arc.types import (
    BlockHash, BlockState, BlockStatus, OffloadingEvent, PrepareStoreOutput)
from src.infrastructure.storage.kv_transfer.k_vzap import (KVzapConfig,
                                                           KVzapPruner)

if TYPE_CHECKING:
    import torch

    from src.infrastructure.storage.kv_transfer.arc.backend import Backend
    from src.infrastructure.storage.kv_transfer.arc.types import LoadStoreSpec


class ARCOffloadManager(OffloadingManager):
    """
    ARC (Adaptive Replacement Cache) offloading manager.

    Implements the ARC eviction policy which adaptively balances
    recency (T1) and frequency (T2) based on workload patterns.
    """

    def __init__(
        self,
        backend: Backend,
        enable_events: bool = False,
        adaptation_speed: float = 1.0,
        kvzap_config: Optional[KVzapConfig] = None,
    ):
        self.backend = backend
        self.adaptation_speed = adaptation_speed

        # KVzap Integration (arXiv:2601.07891)
        self.pruner: Optional[KVzapPruner] = None
        if kvzap_config:
            self.pruner = KVzapPruner(kvzap_config)

        # ARC data structures
        self.target_t1_size: float = 0.0
        self.t1: OrderedDict[BlockHash, BlockStatus] = OrderedDict()
        self.t2: OrderedDict[BlockHash, BlockStatus] = OrderedDict()
        # Ghost lists (hash -> None, only track presence)
        self.b1: OrderedDict[BlockHash, None] = OrderedDict()
        self.b2: OrderedDict[BlockHash, None] = OrderedDict()

        # Events for debugging/monitoring
        self.events: list[OffloadingEvent] | None = [] if enable_events else None

        # Cache capacity
        self.cache_capacity: int = self.backend.get_num_free_blocks()

        # Statistics
        self._hits = 0
        self._misses = 0
        self._t1_evictions = 0
        self._t2_evictions = 0

        self._lock = threading.Lock()

    def lookup(self, block_hashes: list[BlockHash]) -> int:
        """Look up blocks in cache."""
        with self._lock:
            hit_count = 0
            for block_hash in block_hashes:
                block = self.t1.get(block_hash) or self.t2.get(block_hash)
                if block is None or not block.is_ready:
                    self._misses += 1
                    break
                hit_count += 1
                self._hits += 1
            return hit_count

    def prepare_load(self, block_hashes: list[BlockHash]) -> LoadStoreSpec:
        """Prepare to load blocks from offload storage."""
        # Phase 336: Connectivity Check for Offload Backend
        # Using a generic ID 'kv_offload_backend' as backend identity isn't exposed yet
        if not ConnectivityManager().is_endpoint_available("kv_offload_backend"):
            # If backend is down, we can't load. Returning empty spec or raising might be appropriate.
            # For now, we'll log and return empty to avoid crashes, assuming fallback handling exists.
            return self.backend.get_load_store_spec([], [])

        with self._lock:
            blocks = []
            for block_hash in block_hashes:
                block = self.t1.get(block_hash) or self.t2.get(block_hash)
                assert block is not None, f"Block {block_hash!r} not found"
                assert block.is_ready, f"Block {block_hash!r} not ready"

                block.ref_cnt += 1
                block.last_access_time = time.time()
                blocks.append(block)

            return self.backend.get_load_store_spec(list(block_hashes), blocks)

    def touch(self, block_hashes: list[BlockHash]) -> None:
        """Update access recency - core of ARC adaptation."""
        with self._lock:
            for block_hash in reversed(list(block_hashes)):
                if block_hash in self.t1:
                    block = self.t1[block_hash]
                    if not block.is_ready:
                        self.t1.move_to_end(block_hash)
                    else:
                        del self.t1[block_hash]
                        self.t2[block_hash] = block
                        self.t2.move_to_end(block_hash)

                elif block_hash in self.t2:
                    self.t2.move_to_end(block_hash)

                elif block_hash in self.b1:
                    delta = self.adaptation_speed * max(1, len(self.b2) / max(1, len(self.b1)))
                    self.target_t1_size = min(self.target_t1_size + delta, self.cache_capacity)
                    self.b1.move_to_end(block_hash)

                elif block_hash in self.b2:
                    delta = self.adaptation_speed * max(1, len(self.b1) / max(1, len(self.b2)))
                    self.target_t1_size = max(self.target_t1_size - delta, 0)
                    self.b2.move_to_end(block_hash)

    def complete_load(self, block_hashes: list[BlockHash]) -> None:
        """Complete load operation, decrement ref counts."""
        with self._lock:
            for block_hash in block_hashes:
                block = self.t1.get(block_hash) or self.t2.get(block_hash)
                assert block is not None, f"Block {block_hash!r} not found"
                assert block.ref_cnt > 0, f"Block {block_hash!r} ref_cnt already 0"
                block.ref_cnt -= 1

    def prepare_store(self, block_hashes: list[BlockHash]) -> PrepareStoreOutput | None:
        """Prepare to store blocks with ARC eviction."""
        with self._lock:
            to_store = [h for h in block_hashes if h not in self.t1 and h not in self.t2]

            if not to_store:
                return PrepareStoreOutput(
                    block_hashes_to_store=[],
                    store_spec=self.backend.get_load_store_spec([], []),
                    block_hashes_evicted=[],
                )

            num_to_evict = len(to_store) - self.backend.get_num_free_blocks()
            evicted = []

            while num_to_evict > 0:
                block_to_evict = self._select_victim()
                if block_to_evict is None:
                    return None

                block_hash, block, from_t1 = block_to_evict

                if from_t1:
                    del self.t1[block_hash]
                    self.b1[block_hash] = None
                    self._t1_evictions += 1
                else:
                    del self.t2[block_hash]
                    self.b2[block_hash] = None
                    self._t2_evictions += 1

                self.backend.free(block)
                evicted.append(block_hash)
                num_to_evict -= 1

            self._trim_ghost_lists()
            new_blocks = self.backend.allocate_blocks(to_store)

            for block_hash, block in zip(to_store, new_blocks):
                self.t1[block_hash] = block
                self.b1.pop(block_hash, None)
                self.b2.pop(block_hash, None)

            if self.events is not None and evicted:
                self.events.append(
                    OffloadingEvent(
                        block_hashes=evicted,
                        block_size=self.backend.block_size,
                        medium=self.backend.medium,
                        removed=True,
                    )
                )

            return PrepareStoreOutput(
                block_hashes_to_store=to_store,
                store_spec=self.backend.get_load_store_spec(to_store, new_blocks),
                block_hashes_evicted=evicted,
            )

    def _select_victim(self) -> tuple[BlockHash, BlockStatus, bool] | None:
        """Select victim block for eviction."""
        if self.pruner:
            threshold = self.pruner.config.threshold
            for block_hash, block in self.t1.items():
                if block.can_evict and block.importance_score < threshold:
                    return (block_hash, block, True)
            for block_hash, block in self.t2.items():
                if block.can_evict and block.importance_score < threshold:
                    return (block_hash, block, False)

        if len(self.t1) >= int(self.target_t1_size):
            for block_hash, block in self.t1.items():
                if block.can_evict:
                    return (block_hash, block, True)

        for block_hash, block in self.t2.items():
            if block.can_evict:
                return (block_hash, block, False)

        for block_hash, block in self.t1.items():
            if block.can_evict:
                return (block_hash, block, True)

        return None

    def update_block_importance(self, block_hash: BlockHash, hidden_states: torch.Tensor) -> None:
        """Update a block's importance score using the KVzap pruner."""
        if not self.pruner:
            return

        block = self.t1.get(block_hash) or self.t2.get(block_hash)
        if block:
            scores = self.pruner.get_importance_scores(hidden_states)
            block.importance_score = scores.mean().item()

    def _trim_ghost_lists(self) -> None:
        """Trim ghost lists to bounded size."""
        max_ghost_size = self.cache_capacity

        while len(self.b1) > max_ghost_size:
            self.b1.popitem(last=False)

        while len(self.b2) > max_ghost_size:
            self.b2.popitem(last=False)

    def complete_store(self, block_hashes: list[BlockHash]) -> None:
        """Mark stored blocks as ready."""
        with self._lock:
            for block_hash in block_hashes:
                block = self.t1.get(block_hash) or self.t2.get(block_hash)
                if block:
                    block.state = BlockState.READY

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            total_requests = self._hits + self._misses
            return {
                "t1_size": len(self.t1),
                "t2_size": len(self.t2),
                "b1_size": len(self.b1),
                "b2_size": len(self.b2),
                "target_t1_size": self.target_t1_size,
                "cache_capacity": self.cache_capacity,
                "hit_rate": self._hits / max(1, total_requests),
                "t1_evictions": self._t1_evictions,
                "t2_evictions": self._t2_evictions,
            }

    def clear(self) -> None:
        """Clear all cached blocks."""
        with self._lock:
            for block in self.t1.values():
                self.backend.free(block)
            for block in self.t2.values():
                self.backend.free(block)

            self.t1.clear()
            self.t2.clear()
            self.b1.clear()
            self.b2.clear()
            self.target_t1_size = 0.0
            self._hits = 0
            self._misses = 0
            self._t1_evictions = 0
            self._t2_evictions = 0


class AdaptiveARCManager(ARCOffloadManager):
    """ARC manager with enhanced adaptation features."""

    def __init__(
        self,
        backend: Backend,
        enable_events: bool = False,
        min_adaptation_speed: float = 0.5,
        max_adaptation_speed: float = 2.0,
    ):
        super().__init__(backend, enable_events, adaptation_speed=1.0)
        self.min_adaptation_speed = min_adaptation_speed
        self.max_adaptation_speed = max_adaptation_speed

        self._request_blocks: dict[str, set[BlockHash]] = {}
        self._block_requests: dict[BlockHash, set[str]] = {}

        self._adaptation_history: list[float] = []
        self._window_size = 100

    def touch_for_request(self, block_hashes: list[BlockHash], request_id: str) -> None:
        """Touch blocks with request affinity tracking."""
        with self._lock:
            if request_id not in self._request_blocks:
                self._request_blocks[request_id] = set()

            for block_hash in block_hashes:
                self._request_blocks[request_id].add(block_hash)

                if block_hash not in self._block_requests:
                    self._block_requests[block_hash] = set()
                self._block_requests[block_hash].add(request_id)

        self.touch(block_hashes)

    def complete_request(self, request_id: str) -> None:
        """Mark request as complete, update affinity."""
        with self._lock:
            if request_id in self._request_blocks:
                blocks = self._request_blocks.pop(request_id)
                for block_hash in blocks:
                    if block_hash in self._block_requests:
                        self._block_requests[block_hash].discard(request_id)
                        if not self._block_requests[block_hash]:
                            del self._block_requests[block_hash]

    def get_block_affinity(self, block_hash: BlockHash) -> int:
        """Get number of active requests using block."""
        with self._lock:
            return len(self._block_requests.get(block_hash, set()))

    def _select_victim(self) -> tuple[BlockHash, BlockStatus, bool] | None:
        """Select victim considering request affinity."""
        for block_hash, block in self.t1.items():
            if block.can_evict and self.get_block_affinity(block_hash) == 0:
                if len(self.t1) >= int(self.target_t1_size):
                    return (block_hash, block, True)

        for block_hash, block in self.t2.items():
            if block.can_evict and self.get_block_affinity(block_hash) == 0:
                return (block_hash, block, False)

        return super()._select_victim()

    def adjust_adaptation_speed(self, hit_rate: float) -> None:
        """Dynamically adjust adaptation speed."""
        self._adaptation_history.append(hit_rate)
        if len(self._adaptation_history) > self._window_size:
            self._adaptation_history.pop(0)

        if len(self._adaptation_history) >= 10:
            recent_avg = sum(self._adaptation_history[-10:]) / 10
            overall_avg = sum(self._adaptation_history) / len(self._adaptation_history)

            if recent_avg < overall_avg * 0.9:
                self.adaptation_speed = min(self.adaptation_speed * 1.1, self.max_adaptation_speed)
            elif recent_avg > overall_avg * 1.1:
                self.adaptation_speed = max(self.adaptation_speed * 0.9, self.min_adaptation_speed)


class AsyncARCManager:
    """Async wrapper for ARC offloading manager."""

    def __init__(self, manager: ARCOffloadManager):
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
