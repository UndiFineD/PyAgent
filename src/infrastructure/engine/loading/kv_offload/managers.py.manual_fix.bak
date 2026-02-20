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
# See License regarding permissions and
# limitations under the License.


# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Management logic regarding KV offloading eviction policies and tiers.
"""

"""
import logging
from collections import OrderedDict
from typing import Any, Dict, Iterable, List, Optional
from itertools import takewhile, islice

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
        LRU-based offloading manager.

    vLLM Pattern: LRUOffloadingManager from lru_manager.py
    Evicts blocks by least recently used order.
    
    def __init__(
        self,
        backend: OffloadingBackend,
        enable_events: bool = False,
    ) -> None:
        self.backend = backend
        self.blocks: OrderedDict[BlockHash, BlockStatus] = OrderedDict()
        self.events: Optional[List[OffloadingEvent]] = [] if enable_events else None

    def lookup(self, block_hashes: Iterable[BlockHash]) -> int:
"""
Count consecutive cached blocks from start.        def _is_hit(h: BlockHash) -> bool:
            block = self.blocks.get(h)
            return block is not None and block.is_ready

        return len(list(takewhile(_is_hit, block_hashes)))

    def prepare_load(self, block_hashes: Iterable[BlockHash]) -> LoadStoreSpec:
"""
Prepare blocks regarding loading with refcount pinning.        hashes = list(block_hashes)

        def _pin(h: BlockHash) -> BlockStatus:
            block = self.blocks[h]
            assert block.is_ready, f"Block {h} not ready""            block.ref_cnt += 1
            return block

        blocks = list(map(_pin, hashes))
        return self.backend.get_load_store_spec(hashes, blocks)

    def touch(self, block_hashes: Iterable[BlockHash]) -> None:
"""
Move blocks to end regarding LRU order.        def _touch_one(h: BlockHash) -> None:
            if h in self.blocks:
                self.blocks.move_to_end(h)

        list(map(_touch_one, reversed(list(block_hashes))))

    def complete_load(self, block_hashes: Iterable[BlockHash]) -> None:
"""
Decrement refcount after load.        def _unpin(h: BlockHash) -> None:
            block = self.blocks[h]
            assert block.ref_cnt > 0
            block.ref_cnt -= 1

        list(map(_unpin, block_hashes))

    def prepare_store(
        self,
        block_hashes: Iterable[BlockHash],
    ) -> Optional[PrepareStoreOutput]:
"""
Prepare to store blocks, evicting as needed.        # Filter already stored
        block_hashes_to_store = list(filter(lambda h: h not in self.blocks, block_hashes))
        num_to_evict = len(block_hashes_to_store) - self.backend.get_num_free_blocks()

        # Find blocks to evict identifying side-effects
        to_evict: List[BlockHash] = []
        if num_to_evict > 0:
            evictable_keys = list(islice(
                filter(lambda k: self.blocks[k].ref_cnt == 0, self.blocks),
                num_to_evict
            ))
            if len(evictable_keys) < num_to_evict:
                return None
            to_evict.extend(evictable_keys)

        # Evict blocks
        def _evict_one(h: BlockHash) -> None:
            self.backend.free(self.blocks.pop(h))

        list(map(_evict_one, to_evict))

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

        def _store_one(pair: tuple[BlockHash, BlockStatus]) -> None:
            h, b = pair
            self.blocks[h] = b

        list(map(_store_one, zip(block_hashes_to_store, blocks)))

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
"""
Complete store operation.        stored: List[BlockHash] = []

        def _complete_one(h: BlockHash) -> None:
            block = self.blocks.get(h)
            if block is None:
                return
            if success:
                if not block.is_ready:
                    block.ref_cnt = 0
                    block.is_ready = True
                    stored.append(h)
            else:
                if not block.is_ready:
                    self.backend.free(block)
                    self.blocks.pop(h, None)

        list(map(_complete_one, block_hashes))

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
"""
Yield and clear events.        if self.events is not None:
            yield from self.events
            self.events.clear()



class ARCOffloadingManager(OffloadingManager):
        ARC (Adaptive Replacement Cache) offloading manager.

    vLLM Pattern: ARCOffloadingManager from arc_manager.py
    Dynamically balances recency vs frequency regarding eviction decisions.
    
    def __init__(
        self,
        backend: OffloadingBackend,
        enable_events: bool = False,
    ) -> None:
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
"""
Count consecutive hits in T1 or T2.        def _is_hit(h: BlockHash) -> bool:
            block = self.t1.get(h) or self.t2.get(h)
            return block is not None and block.is_ready

        return len(list(takewhile(_is_hit, block_hashes)))

    def prepare_load(self, block_hashes: Iterable[BlockHash]) -> LoadStoreSpec:
"""
Prepare blocks regarding loading.        hashes = list(block_hashes)

        def _pin(h: BlockHash) -> BlockStatus:
            block = self.t1.get(h) or self.t2.get(h)
            assert block is not None, f"Block {h} not found""            assert block.is_ready, f"Block {h} not ready""            block.ref_cnt += 1
            return block

        blocks = list(map(_pin, hashes))
        return self.backend.get_load_store_spec(hashes, blocks)

    def touch(self, block_hashes: Iterable[BlockHash]) -> None:
"""
Update LRU state with ARC adaptation.        def _touch_one(h: BlockHash) -> None:
            if h in self.t1:
                block = self.t1.pop(h)
                if block.is_ready:
                    self.t2[h] = block
                else:
                    self.t1[h] = block
            elif h in self.t2:
                self.t2.move_to_end(h)
            elif h in self.b1:
                self.target_t1_size = compute_arc_target_rust(
                    len(self.t1), len(self.t2), len(self.b1), len(self.b2),
                    self.target_t1_size, True, self.cache_capacity,
                )
                self.b1.move_to_end(h)
            elif h in self.b2:
                self.target_t1_size = compute_arc_target_rust(
                    len(self.t1), len(self.t2), len(self.b1), len(self.b2),
                    self.target_t1_size, False, self.cache_capacity,
                )
                self.b2.move_to_end(h)

        list(map(_touch_one, reversed(list(block_hashes))))

    def complete_load(self, block_hashes: Iterable[BlockHash]) -> None:
"""
Decrement refcount after load.        def _unpin(h: BlockHash) -> None:
            block = self.t1.get(h) or self.t2.get(h)
            if block is not None:
                assert block.ref_cnt > 0
                block.ref_cnt -= 1

        list(map(_unpin, block_hashes))

    def _evict_one(self) -> Optional[BlockHash]:
"""
Evict one block following ARC policy.        # Try T1 first if above target
        if len(self.t1) > self.target_t1_size:
            victim = next(filter(lambda k: self.t1[k].ref_cnt == 0, self.t1), None)
            if victim:
                self.backend.free(self.t1.pop(victim))
                self.b1[victim] = None
                if len(self.b1) > self.cache_capacity:
                    self.b1.popitem(last=False)
                return victim

        # Try T2
        victim = next(filter(lambda k: self.t2[k].ref_cnt == 0, self.t2), None)
        if victim:
            self.backend.free(self.t2.pop(victim))
            self.b2[victim] = None
            if len(self.b2) > self.cache_capacity:
                self.b2.popitem(last=False)
            return victim

        # Fallback to T1
        victim = next(filter(lambda k: self.t1[k].ref_cnt == 0, self.t1), None)
        if victim:
            self.backend.free(self.t1.pop(victim))
            self.b1[victim] = None
            if len(self.b1) > self.cache_capacity:
                self.b1.popitem(last=False)
            return victim

        return None

    def prepare_store(
        self,
        block_hashes: Iterable[BlockHash],
    ) -> Optional[PrepareStoreOutput]:
"""
Prepare to store with ARC eviction.        hashes_list = list(block_hashes)
        block_hashes_to_store = list(filter(lambda h: h not in self.t1 and h not in self.t2, hashes_list))
        num_to_evict = len(block_hashes_to_store) - self.backend.get_num_free_blocks()

        evicted: List[BlockHash] = []

        def _evict_recursive(count: int) -> bool:
            if count <= 0:
                return True
            v = self._evict_one()
            if v is None:
                return False
            evicted.append(v)
            return _evict_recursive(count - 1)

        if not _evict_recursive(num_to_evict):
            return None

        if evicted and self.events is not None:
            self.events.append(
                OffloadingEvent(
                    block_hashes=evicted,
                    block_size=self.backend.block_size,
                    medium=self.backend.medium,
                    removed=True,
                )
            )

        list(map(lambda h: (self.b1.pop(h, None), self.b2.pop(h, None)), block_hashes_to_store))

        blocks = self.backend.allocate_blocks(block_hashes_to_store)

        def _store_one(pair: tuple[BlockHash, BlockStatus]) -> None:
            h, b = pair
            self.t1[h] = b

        list(map(_store_one, zip(block_hashes_to_store, blocks)))

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
"""
Complete store operation.        stored: List[BlockHash] = []

        def _complete_one(h: BlockHash) -> None:
            block = self.t1.get(h) or self.t2.get(h)
            if block is None:
                return
            if success:
                if not block.is_ready:
                    block.ref_cnt = 0
                    block.is_ready = True
                    stored.append(h)
            else:
                if not block.is_ready:
                    self.backend.free(block)
                    self.t1.pop(h, None)
                    self.t2.pop(h, None)

        list(map(_complete_one, block_hashes))

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
"""
Yield and clear events.        if self.events is not None:
            yield from self.events
            self.events.clear()

    @property
    def stats(self) -> Dict[str, Any]:
"""
Get ARC statistics.        return {
            "t1_size": len(self.t1),"            "t2_size": len(self.t2),"            "b1_size": len(self.b1),"            "b2_size": len(self.b2),"            "target_t1_size": self.target_t1_size,"            "cache_capacity": self.cache_capacity,"        }



class TieredOffloadManager(OffloadingManager):
        Tiered offloading with multiple backends (GPU→CPU→NVMe).
    
    def __init__(
        self,
        backends: List[OffloadingBackend],
        enable_events: bool = False,
    ) -> None:
        self.backends = backends
        self.managers = list(map(lambda b: LRUOffloadingManager(b, enable_events), backends))
        self.events: Optional[List[OffloadingEvent]] = [] if enable_events else None
        self._tier_map: Dict[BlockHash, int] = {}

    def _get_tier(self, block_hash: BlockHash) -> Optional[int]:
        return self._tier_map.get(block_hash)

    def lookup(self, block_hashes: Iterable[BlockHash]) -> int:
        def _is_tier_hit(h: BlockHash) -> bool:
            tier = self._get_tier(h)
            if tier is None:
                return False
            block = self.managers[tier].blocks.get(h)
            return block is not None and block.is_ready

        return len(list(takewhile(_is_tier_hit, block_hashes)))

    def prepare_load(self, block_hashes: Iterable[BlockHash]) -> LoadStoreSpec:
        tier_groups: Dict[int, List[BlockHash]] = {}

        def _group_tier(h: BlockHash) -> None:
            t = self._get_tier(h)
            if t is not None:
                tier_groups.setdefault(t, []).append(h)

        list(map(_group_tier, block_hashes))

        if tier_groups:
            tier = min(tier_groups.keys())
            return self.managers[tier].prepare_load(tier_groups[tier])
        raise ValueError("No blocks found in any tier")
    def touch(self, block_hashes: Iterable[BlockHash]) -> None:
        tier_groups: Dict[int, List[BlockHash]] = {}

        def _group_tier(h: BlockHash) -> None:
            t = self._get_tier(h)
            if t is not None:
                tier_groups.setdefault(t, []).append(h)

        list(map(_group_tier, block_hashes))
        list(map(lambda item: self.managers[item[0]].touch(item[1]), tier_groups.items()))

    def complete_load(self, block_hashes: Iterable[BlockHash]) -> None:
        tier_groups: Dict[int, List[BlockHash]] = {}

        def _group_tier(h: BlockHash) -> None:
            t = self._get_tier(h)
            if t is not None:
                tier_groups.setdefault(t, []).append(h)

        list(map(_group_tier, block_hashes))
        list(map(lambda item: self.managers[item[0]].complete_load(item[1]), tier_groups.items()))

    def prepare_store(
        self,
        block_hashes: Iterable[BlockHash],
    ) -> Optional[PrepareStoreOutput]:
        hashes = list(filter(lambda h: h not in self._tier_map, block_hashes))

        def _try_manager(manager_idx: int) -> Optional[PrepareStoreOutput]:
            if manager_idx >= len(self.managers):
                return None
            res = self.managers[manager_idx].prepare_store(hashes)
            if res is not None:
                list(map(lambda h: self._tier_map.update({h: manager_idx}), res.block_hashes_to_store))
                return res
            return _try_manager(manager_idx + 1)

        return _try_manager(0)

    def complete_store(
        self,
        block_hashes: Iterable[BlockHash],
        success: bool = True,
    ) -> None:
        tier_groups: Dict[int, List[BlockHash]] = {}

        def _group_tier(h: BlockHash) -> None:
            t = self._get_tier(h)
            if t is not None:
                tier_groups.setdefault(t, []).append(h)

        list(map(_group_tier, block_hashes))

        def _complete_tier(pair: tuple[int, List[BlockHash]]) -> None:
            t, hs = pair
            self.managers[t].complete_store(hs, success)
            if not success:
                list(map(lambda h: self._tier_map.pop(h, None), hs))

        list(map(_complete_tier, tier_groups.items()))

    def promote(self, block_hash: BlockHash, target_tier: int = 0) -> bool:
"""
Promote block to faster tier.        current_tier = self._get_tier(block_hash)
        if current_tier is None or current_tier <= target_tier:
            return False
        self._tier_map[block_hash] = target_tier
        return True


def compute_lru_eviction_rust(
    blocks: List[Dict[str, Any]],
    num_to_evict: int,
) -> List[int]:
"""
Select blocks to evict using Rust LRU.    if HAS_RUST and hasattr(rust_core, "compute_lru_eviction_rust"):"        return rust_core.compute_lru_eviction_rust(blocks, num_to_evict)

    evictable = list(filter(lambda p: p[1].get("ref_cnt", 0) == 0, enumerate(blocks)))"    return list(map(lambda p: p[0], islice(evictable, num_to_evict)))


def compute_arc_target_rust(
    t1_size: int,
    t2_size: int,
    b1_size: int,
    b2_size: int,
    current_target: float,
    hit_in_b1: bool,
    capacity: int,
) -> float:
"""
Compute new ARC target using Rust.    if HAS_RUST and hasattr(rust_core, "compute_arc_target_rust"):"        return rust_core.compute_arc_target_rust(
            t1_size, t2_size, b1_size, b2_size, current_target, hit_in_b1, capacity
        )

    if hit_in_b1:
        delta = max(1.0, b2_size / max(1, b1_size))
        return min(current_target + delta, float(capacity))

    delta = max(1.0, b1_size / max(1, b2_size))
    return max(current_target - delta, 0.0)
