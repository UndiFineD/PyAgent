#!/usr/bin/env python3
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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Management logic for KV offloading eviction policies and tiers.
"""

from __future__ import annotations

import logging
from collections import OrderedDict
from typing import Any, Dict, Iterable, List, Optional

try:
    from ...core import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False

from .base import OffloadingBackend, OffloadingManager
from .models import (BlockHash, BlockStatus, LoadStoreSpec, OffloadingEvent,
                     PrepareStoreOutput)

logger = logging.getLogger(__name__)


class LRUOffloadingManager(OffloadingManager):
    """
    LRU-based offloading manager.

    vLLM Pattern: LRUOffloadingManager from lru_manager.py
    Evicts blocks by least recently used order.
    """

    def __init__(
        self,
        backend: OffloadingBackend,
        enable_events: bool = False,
    ):
        self.backend = backend
        self.blocks: OrderedDict[BlockHash, BlockStatus] = OrderedDict()
        self.events: Optional[List[OffloadingEvent]] = [] if enable_events else None

    def lookup(self, block_hashes: Iterable[BlockHash]) -> int:
        """Count consecutive cached blocks from start."""
        hit_count = 0
        for block_hash in block_hashes:
            block = self.blocks.get(block_hash)
            if block is None or not block.is_ready:
                break
            hit_count += 1
        return hit_count

    def prepare_load(self, block_hashes: Iterable[BlockHash]) -> LoadStoreSpec:
        """Prepare blocks for loading with refcount pinning."""
        blocks = []
        hashes = list(block_hashes)

        for block_hash in hashes:
            block = self.blocks[block_hash]
            assert block.is_ready, f"Block {block_hash} not ready"
            block.ref_cnt += 1
            blocks.append(block)

        return self.backend.get_load_store_spec(hashes, blocks)

    def touch(self, block_hashes: Iterable[BlockHash]) -> None:
        """Move blocks to end of LRU order."""
        for block_hash in reversed(list(block_hashes)):
            if block_hash in self.blocks:
                self.blocks.move_to_end(block_hash)

    def complete_load(self, block_hashes: Iterable[BlockHash]) -> None:
        """Decrement refcount after load."""
        for block_hash in block_hashes:
            block = self.blocks[block_hash]
            assert block.ref_cnt > 0
            block.ref_cnt -= 1

    def prepare_store(
        self,
        block_hashes: Iterable[BlockHash],
    ) -> Optional[PrepareStoreOutput]:
        """Prepare to store blocks, evicting as needed."""
        # Filter already stored
        block_hashes_to_store = [h for h in block_hashes if h not in self.blocks]

        num_to_evict = len(block_hashes_to_store) - self.backend.get_num_free_blocks()

        # Find blocks to evict
        to_evict: List[BlockHash] = []
        if num_to_evict > 0:
            for block_hash, block in self.blocks.items():
                if block.ref_cnt == 0:
                    to_evict.append(block_hash)
                    num_to_evict -= 1
                    if num_to_evict == 0:
                        break
            else:
                # Not enough evictable blocks
                return None

        # Evict blocks
        for block_hash in to_evict:
            self.backend.free(self.blocks.pop(block_hash))

        if to_evict and self.events is not None:
            self.events.append(
                OffloadingEvent(
                    block_hashes=to_evict,
                    block_size=self.backend.block_size,
                    medium=self.backend.medium,
                    removed=True,
                )
            )

        # Allocate new blocks
        blocks = self.backend.allocate_blocks(block_hashes_to_store)

        for block_hash, block in zip(block_hashes_to_store, blocks):
            self.blocks[block_hash] = block

        return PrepareStoreOutput(
            block_hashes_to_store=block_hashes_to_store,
            store_spec=self.backend.get_load_store_spec(block_hashes_to_store, blocks),
            block_hashes_evicted=to_evict,
        )

    def complete_store(
        self,
        block_hashes: Iterable[BlockHash],
        success: bool = True,
    ) -> None:
        """Complete store operation."""
        stored: List[BlockHash] = []

        for block_hash in block_hashes:
            block = self.blocks.get(block_hash)
            if block is None:
                continue

            if success:
                if not block.is_ready:
                    block.ref_cnt = 0
                    block.is_ready = True
                    stored.append(block_hash)
            else:
                if not block.is_ready:
                    self.backend.free(block)
                    del self.blocks[block_hash]

        if stored and self.events is not None:
            self.events.append(
                OffloadingEvent(
                    block_hashes=stored,
                    block_size=self.backend.block_size,
                    medium=self.backend.medium,
                    removed=False,
                )
            )

    def take_events(self) -> Iterable[OffloadingEvent]:
        """Yield and clear events."""
        if self.events is not None:
            yield from self.events
            self.events.clear()


class ARCOffloadingManager(OffloadingManager):
    """
    ARC (Adaptive Replacement Cache) offloading manager.

    vLLM Pattern: ARCOffloadingManager from arc_manager.py
    Dynamically balances recency vs frequency for eviction decisions.
    """

    def __init__(
        self,
        backend: OffloadingBackend,
        enable_events: bool = False,
    ):
        self.backend = backend
        self.target_t1_size: float = 0.0

        # Main caches
        self.t1: OrderedDict[BlockHash, BlockStatus] = OrderedDict()
        self.t2: OrderedDict[BlockHash, BlockStatus] = OrderedDict()

        # Ghost lists (just track presence)
        self.b1: OrderedDict[BlockHash, None] = OrderedDict()
        self.b2: OrderedDict[BlockHash, None] = OrderedDict()

        self.events: Optional[List[OffloadingEvent]] = [] if enable_events else None
        self.cache_capacity = backend.get_num_free_blocks()

    def lookup(self, block_hashes: Iterable[BlockHash]) -> int:
        """Count consecutive hits in T1 or T2."""
        hit_count = 0
        for block_hash in block_hashes:
            block = self.t1.get(block_hash) or self.t2.get(block_hash)
            if block is None or not block.is_ready:
                break
            hit_count += 1
        return hit_count

    def prepare_load(self, block_hashes: Iterable[BlockHash]) -> LoadStoreSpec:
        """Prepare blocks for loading."""
        blocks = []
        hashes = list(block_hashes)

        for block_hash in hashes:
            block = self.t1.get(block_hash) or self.t2.get(block_hash)
            assert block is not None, f"Block {block_hash} not found"
            assert block.is_ready, f"Block {block_hash} not ready"
            block.ref_cnt += 1
            blocks.append(block)

        return self.backend.get_load_store_spec(hashes, blocks)

    def touch(self, block_hashes: Iterable[BlockHash]) -> None:
        """Update LRU state with ARC adaptation."""
        for block_hash in reversed(list(block_hashes)):
            if block_hash in self.t1:
                block = self.t1.pop(block_hash)
                if block.is_ready:
                    self.t2[block_hash] = block
                else:
                    # Just stored, don't promote yet
                    self.t1[block_hash] = block

            elif block_hash in self.t2:
                self.t2.move_to_end(block_hash)

            elif block_hash in self.b1:
                # Hit in ghost list → increase recency preference
                delta = compute_arc_target_rust(
                    len(self.t1),
                    len(self.t2),
                    len(self.b1),
                    len(self.b2),
                    self.target_t1_size,
                    True,
                    self.cache_capacity,
                )
                self.target_t1_size = delta
                self.b1.move_to_end(block_hash)

            elif block_hash in self.b2:
                # Hit in ghost list → increase frequency preference
                delta = compute_arc_target_rust(
                    len(self.t1),
                    len(self.t2),
                    len(self.b1),
                    len(self.b2),
                    self.target_t1_size,
                    False,
                    self.cache_capacity,
                )
                self.target_t1_size = delta
                self.b2.move_to_end(block_hash)

    def complete_load(self, block_hashes: Iterable[BlockHash]) -> None:
        """Decrement refcount after load."""
        for block_hash in block_hashes:
            block = self.t1.get(block_hash) or self.t2.get(block_hash)
            if block is not None:
                assert block.ref_cnt > 0
                block.ref_cnt -= 1

    def _evict_one(self) -> Optional[BlockHash]:
        """Evict one block following ARC policy."""
        # Try T1 first if above target
        if len(self.t1) > self.target_t1_size:
            for block_hash, block in self.t1.items():
                if block.ref_cnt == 0:
                    self.backend.free(block)
                    del self.t1[block_hash]
                    self.b1[block_hash] = None
                    if len(self.b1) > self.cache_capacity:
                        self.b1.popitem(last=False)
                    return block_hash

        # Try T2
        for block_hash, block in self.t2.items():
            if block.ref_cnt == 0:
                self.backend.free(block)
                del self.t2[block_hash]
                self.b2[block_hash] = None
                if len(self.b2) > self.cache_capacity:
                    self.b2.popitem(last=False)
                return block_hash

        # Fallback to T1
        for block_hash, block in self.t1.items():
            if block.ref_cnt == 0:
                self.backend.free(block)
                del self.t1[block_hash]
                self.b1[block_hash] = None
                if len(self.b1) > self.cache_capacity:
                    self.b1.popitem(last=False)
                return block_hash

        return None

    def prepare_store(
        self,
        block_hashes: Iterable[BlockHash],
    ) -> Optional[PrepareStoreOutput]:
        """Prepare to store with ARC eviction."""
        block_hashes_to_store = [h for h in block_hashes if h not in self.t1 and h not in self.t2]

        num_to_evict = len(block_hashes_to_store) - self.backend.get_num_free_blocks()

        evicted: List[BlockHash] = []
        while num_to_evict > 0:
            victim = self._evict_one()
            if victim is None:
                return None
            evicted.append(victim)
            num_to_evict -= 1

        if evicted and self.events is not None:
            self.events.append(
                OffloadingEvent(
                    block_hashes=evicted,
                    block_size=self.backend.block_size,
                    medium=self.backend.medium,
                    removed=True,
                )
            )

        for block_hash in block_hashes_to_store:
            self.b1.pop(block_hash, None)
            self.b2.pop(block_hash, None)

        blocks = self.backend.allocate_blocks(block_hashes_to_store)
        for block_hash, block in zip(block_hashes_to_store, blocks):
            self.t1[block_hash] = block

        return PrepareStoreOutput(
            block_hashes_to_store=block_hashes_to_store,
            store_spec=self.backend.get_load_store_spec(block_hashes_to_store, blocks),
            block_hashes_evicted=evicted,
        )

    def complete_store(
        self,
        block_hashes: Iterable[BlockHash],
        success: bool = True,
    ) -> None:
        """Complete store operation."""
        stored: List[BlockHash] = []
        for block_hash in block_hashes:
            block = self.t1.get(block_hash) or self.t2.get(block_hash)
            if block is None:
                continue

            if success:
                if not block.is_ready:
                    block.ref_cnt = 0
                    block.is_ready = True
                    stored.append(block_hash)
            else:
                if not block.is_ready:
                    self.backend.free(block)
                    if block_hash in self.t1:
                        del self.t1[block_hash]
                    elif block_hash in self.t2:
                        del self.t2[block_hash]

        if stored and self.events is not None:
            self.events.append(
                OffloadingEvent(
                    block_hashes=stored,
                    block_size=self.backend.block_size,
                    medium=self.backend.medium,
                    removed=False,
                )
            )

    def take_events(self) -> Iterable[OffloadingEvent]:
        """Yield and clear events."""
        if self.events is not None:
            yield from self.events
            self.events.clear()

    @property
    def stats(self) -> Dict[str, Any]:
        """Get ARC statistics."""
        return {
            "t1_size": len(self.t1),
            "t2_size": len(self.t2),
            "b1_size": len(self.b1),
            "b2_size": len(self.b2),
            "target_t1_size": self.target_t1_size,
            "cache_capacity": self.cache_capacity,
        }


class TieredOffloadManager(OffloadingManager):
    """
    Tiered offloading with multiple backends (GPU→CPU→NVMe).
    """

    def __init__(
        self,
        backends: List[OffloadingBackend],
        enable_events: bool = False,
    ):
        self.backends = backends
        self.managers = [LRUOffloadingManager(backend, enable_events) for backend in backends]
        self.events: Optional[List[OffloadingEvent]] = [] if enable_events else None
        self._tier_map: Dict[BlockHash, int] = {}

    def _get_tier(self, block_hash: BlockHash) -> Optional[int]:
        return self._tier_map.get(block_hash)

    def lookup(self, block_hashes: Iterable[BlockHash]) -> int:
        hit_count = 0
        for block_hash in block_hashes:
            tier = self._get_tier(block_hash)
            if tier is None:
                break
            block = self.managers[tier].blocks.get(block_hash)
            if block is None or not block.is_ready:
                break
            hit_count += 1
        return hit_count

    def prepare_load(self, block_hashes: Iterable[BlockHash]) -> LoadStoreSpec:
        tier_groups: Dict[int, List[BlockHash]] = {}
        hashes = list(block_hashes)
        for block_hash in hashes:
            tier = self._get_tier(block_hash)
            if tier is not None:
                tier_groups.setdefault(tier, []).append(block_hash)

        if tier_groups:
            tier = min(tier_groups.keys())
            return self.managers[tier].prepare_load(tier_groups[tier])
        raise ValueError("No blocks found in any tier")

    def touch(self, block_hashes: Iterable[BlockHash]) -> None:
        tier_groups: Dict[int, List[BlockHash]] = {}
        for block_hash in block_hashes:
            tier = self._get_tier(block_hash)
            if tier is not None:
                tier_groups.setdefault(tier, []).append(block_hash)
        for tier, hashes in tier_groups.items():
            self.managers[tier].touch(hashes)

    def complete_load(self, block_hashes: Iterable[BlockHash]) -> None:
        tier_groups: Dict[int, List[BlockHash]] = {}
        for block_hash in block_hashes:
            tier = self._get_tier(block_hash)
            if tier is not None:
                tier_groups.setdefault(tier, []).append(block_hash)
        for tier, hashes in tier_groups.items():
            self.managers[tier].complete_load(hashes)

    def prepare_store(
        self,
        block_hashes: Iterable[BlockHash],
    ) -> Optional[PrepareStoreOutput]:
        hashes = [h for h in block_hashes if h not in self._tier_map]
        for tier, manager in enumerate(self.managers):
            result = manager.prepare_store(hashes)
            if result is not None:
                for block_hash in result.block_hashes_to_store:
                    self._tier_map[block_hash] = tier
                return result
        return None

    def complete_store(
        self,
        block_hashes: Iterable[BlockHash],
        success: bool = True,
    ) -> None:
        tier_groups: Dict[int, List[BlockHash]] = {}
        for block_hash in block_hashes:
            tier = self._get_tier(block_hash)
            if tier is not None:
                tier_groups.setdefault(tier, []).append(block_hash)
        for tier, hashes in tier_groups.items():
            self.managers[tier].complete_store(hashes, success)
            if not success:
                for h in hashes:
                    self._tier_map.pop(h, None)

    def promote(self, block_hash: BlockHash, target_tier: int = 0) -> bool:
        """Promote block to faster tier."""
        current_tier = self._get_tier(block_hash)
        if current_tier is None or current_tier <= target_tier:
            return False
        self._tier_map[block_hash] = target_tier
        return True


def compute_lru_eviction_rust(
    blocks: List[Dict[str, Any]],
    num_to_evict: int,
) -> List[int]:
    """Select blocks to evict using Rust LRU."""
    if HAS_RUST and hasattr(rust_core, "compute_lru_eviction_rust"):
        return rust_core.compute_lru_eviction_rust(blocks, num_to_evict)

    evictable = [(i, b) for i, b in enumerate(blocks) if b.get("ref_cnt", 0) == 0]
    return [i for i, _ in evictable[:num_to_evict]]


def compute_arc_target_rust(
    t1_size: int,
    t2_size: int,
    b1_size: int,
    b2_size: int,
    current_target: float,
    hit_in_b1: bool,
    capacity: int,
) -> float:
    """Compute new ARC target using Rust."""
    if HAS_RUST and hasattr(rust_core, "compute_arc_target_rust"):
        return rust_core.compute_arc_target_rust(
            t1_size, t2_size, b1_size, b2_size, current_target, hit_in_b1, capacity
        )

    if hit_in_b1:
        delta = max(1.0, b2_size / max(1, b1_size))
        return min(current_target + delta, float(capacity))
    else:
        delta = max(1.0, b1_size / max(1, b2_size))
        return max(current_target - delta, 0.0)
