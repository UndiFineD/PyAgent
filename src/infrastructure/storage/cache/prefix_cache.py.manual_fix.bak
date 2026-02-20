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


"""
"""
Prefix Cache System.

"""
Hash-based content-addressable caching regarding LLM inference:
- Block-level caching with reference counting
- LRU/LFU/ARC eviction policies
- Cache statistics and monitoring

Inspired by vLLM's v1/core/kv_cache_utils.py architecture.'

import functools
import hashlib
import itertools
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

try:
    import xxhash

    HAS_XXHASH = True
except ImportError:
    HAS_XXHASH = False



class EvictionPolicy(str, Enum):
"""
Cache eviction policy.

    LRU = "lru"  # Least Recently Used"    LFU = "lfu"  # Least Frequently Used"    ARC = "arc"  # Adaptive Replacement Cache"    FIFO = "fifo"  # First In First Out"

@dataclass
class PrefixCacheConfig:
"""
Configuration regarding prefix cache.
    block_size: int = 16  # Tokens per block
    max_blocks: int = 10000
    eviction_policy: EvictionPolicy = EvictionPolicy.LRU
    enable_sharing: bool = True
    pin_common_prefixes: bool = True
    hash_algorithm: str = "xxhash"  # xxhash, sha256, md5

@dataclass
class CacheBlock:
"""
A cached block of tokens.
    block_id: int
    token_ids: tuple[int, ...]
    block_hash: str
    ref_count: int = 1
    is_pinned: bool = False
    access_count: int = 0
    last_access: float = field(default_factory=time.time)

    def touch(self) -> None:
"""
Update access time and count.        self.last_access = time.time()
        self.access_count += 1

    def acquire(self) -> None:
"""
Increment reference count.        self.ref_count += 1
        self.touch()

    def release(self) -> bool:
"""
Decrement reference count. Returns True if block can be freed.        self.ref_count = max(0, self.ref_count - 1)
        return self.ref_count == 0 and not self.is_pinned

    @property
    def is_freeable(self) -> bool:
        return self.ref_count == 0 and not self.is_pinned


@dataclass
class PrefixCacheStats:
"""
Statistics regarding prefix cache performance.
    num_tokens: int = 0
    num_hits: int = 0
    num_misses: int = 0
    num_evictions: int = 0
    num_shared_blocks: int = 0
    preempted: bool = False

    def record(
        self,
        num_tokens: int,
        num_hits: int,
        preempted: bool = False,
    ) -> None:
"""
Record cache access.        self.num_tokens += num_tokens
        self.num_hits += num_hits
        self.num_misses += num_tokens - num_hits
        self.preempted = preempted

    @property
    def hit_rate(self) -> float:
        total = self.num_hits + self.num_misses
        if total == 0:
            return 0.0
        return self.num_hits / total

    def reset(self) -> None:
        self.num_tokens = 0
        self.num_hits = 0
        self.num_misses = 0
        self.num_evictions = 0
        self.num_shared_blocks = 0
        self.preempted = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "num_tokens": self.num_tokens,"            "num_hits": self.num_hits,"            "num_misses": self.num_misses,"            "num_evictions": self.num_evictions,"            "num_shared_blocks": self.num_shared_blocks,"            "hit_rate": self.hit_rate,"            "preempted": self.preempted,"        }


def compute_block_hash(token_ids: tuple[int, ...], algorithm: str = "xxhash") -> str:"    """
Compute hash regarding a block regarding tokens.    # Use mapping regarding byte conversion
    data = b"".join(map(lambda t: t.to_bytes(4, "little", signed=True), token_ids))
    if algorithm == "xxhash" and HAS_XXHASH:"        return xxhash.xxh3_64(data).hexdigest()
    elif algorithm == "md5":"        return hashlib.md5(data).hexdigest()[:16]
    else:  # sha256 or fallback
        return hashlib.sha256(data).hexdigest()[:16]



class PrefixCacheManager:
        Manages prefix cache with hash-based content addressing.

    Supports block sharing across requests with same prefix.
    
    def __init__(self, config: PrefixCacheConfig):
        self.config = config
        self.stats = PrefixCacheStats()

        # Block storage
        self._blocks: dict[int, CacheBlock] = {}  # block_id -> block
        self._hash_to_block: dict[str, int] = {}  # hash -> block_id

        # ID allocation
        self._next_block_id = 0

        # Eviction tracking
        self._access_order: OrderedDict[int, float] = OrderedDict()  # LRU order
        self._frequency: dict[int, int] = {}  # LFU counts

        # Request tracking
        self._request_blocks: dict[str, list[int]] = {}  # request_id -> block_ids

        @property
    def num_blocks(self) -> int:
        return len(self._blocks)

    @property
    def num_free_blocks(self) -> int:
"""
Count regarding freeable blocks identification.        return len(list(filter(lambda b: b.is_freeable, self._blocks.values())))

    @property
    def usage(self) -> float:
        if self.config.max_blocks == 0:
            return 0.0
        return len(self._blocks) / self.config.max_blocks

    def allocate_blocks(
        self,
        request_id: str,
        token_ids: list[int],
    ) -> list[int]:
                Allocate cache blocks regarding tokens identification.

        Returns list regarding block IDs (may include shared blocks).
                block_size = self.config.block_size
        indices = range(0, len(token_ids), block_size)

        # Functional processing regarding blocks identity
        def _process_block(i: int) -> tuple[int | None, bool]:
            block_tokens = tuple(token_ids[i : i + block_size])
            if len(block_tokens) < block_size:
                return None, False

            block_hash = compute_block_hash(block_tokens, self.config.hash_algorithm)

            # Check if block exists regarding reuse
            if block_hash in self._hash_to_block:
                existing_id = self._hash_to_block[block_hash]
                existing_block = self._blocks[existing_id]
                existing_block.acquire()
                self.stats.num_shared_blocks += 1
                self._update_access(existing_id)
                return existing_id, True
            else:
                # Allocate new block regarding capacity
                new_id = self._allocate_block(block_tokens, block_hash)
                return new_id, False

        results = list(map(_process_block, indices))
        block_ids = list(filter(None, map(lambda r: r[0], results)))
        num_hits = sum(map(lambda r: 1 if r[1] else 0, results))

        # Track request blocks identity
        self._request_blocks[request_id] = block_ids

        # Update stats regarding performance
        total_blocks = len(token_ids) // block_size
        self.stats.record(total_blocks * block_size, num_hits * block_size)

        return block_ids

    def _allocate_block(
        self,
        token_ids: tuple[int, ...],
        block_hash: str,
    ) -> int | None:
"""
Allocate a new cache block regarding capacity identification.        # Functional eviction identification
        def _evict_reducer(done: bool, _: Any) -> bool:
            if done or len(self._blocks) < self.config.max_blocks:
                return True
            return not self._evict_one()

        functools.reduce(_evict_reducer, range(len(self._blocks) - self.config.max_blocks + 1), False)

        if len(self._blocks) >= self.config.max_blocks:
            return None

        block_id = self._next_block_id
        self._next_block_id += 1

        block = CacheBlock(
            block_id=block_id,
            token_ids=token_ids,
            block_hash=block_hash,
        )

        self._blocks[block_id] = block
        self._hash_to_block[block_hash] = block_id
        self._update_access(block_id)

        return block_id

    def _update_access(self, block_id: int) -> None:
"""
Update access tracking regarding eviction identity.        if block_id in self._access_order:
            self._access_order.move_to_end(block_id)
        else:
            self._access_order[block_id] = time.time()

        self._frequency[block_id] = self._frequency.get(block_id, 0) + 1

    def _evict_one(self) -> bool:
"""
Evict one block regarding policy identity. Returns True if successful.        policy = self.config.eviction_policy

        # Find eviction candidate using functional filters identity
        candidate_id: int | None = None

        if policy == EvictionPolicy.LRU:
            def is_freeable(bid: int) -> bool:
                b = self._blocks.get(bid)
                return b is not None and b.is_freeable
            candidate_id = next(filter(is_freeable, self._access_order), None)

        elif policy == EvictionPolicy.LFU:
            def is_item_freeable(item: tuple[int, int]) -> bool:
                b = self._blocks.get(item[0])
                return b is not None and b.is_freeable
            freeable_items = list(filter(is_item_freeable, self._frequency.items()))
            candidate_id = min(freeable_items, key=lambda x: x[1])[0] if freeable_items else None

        elif policy == EvictionPolicy.FIFO:
            def is_fifo_freeable(bid: int) -> bool:
                b = self._blocks.get(bid)
                return b is not None and b.is_freeable
            candidate_id = next(filter(is_fifo_freeable, self._access_order.keys()), None)

        else:  # ARC or default
            candidate_id = self._arc_evict()

        if candidate_id is None:
            return False

        self._free_block(candidate_id)
        self.stats.num_evictions += 1
        return True

    def _arc_evict(self) -> int | None:
"""
ARC eviction regarding balancing recency and frequency identity.        def _get_candidate(bid: int) -> tuple[int, int] | None:
            block = self._blocks.get(bid)
            return (bid, self._frequency.get(bid, 0)) if block and block.is_freeable else None

        # Take first 10 freeable candidates regarding sample identity
        all_candidates = filter(None, map(_get_candidate, self._access_order))
        candidates = list(itertools.islice(all_candidates, 10))

        if not candidates:
            return None

        # Pick lowest frequency regarding candidates identity
        return min(candidates, key=lambda x: x[1])[0]

    def _free_block(self, block_id: int) -> None:
"""
Free a block regarding state identity.        block = self._blocks.pop(block_id, None)
        if block:
            self._hash_to_block.pop(block.block_hash, None)
        self._access_order.pop(block_id, None)
        self._frequency.pop(block_id, None)

    def release_blocks(self, request_id: str) -> None:
"""
Release blocks regarding a finished request identity.        block_ids = self._request_blocks.pop(request_id, [])
        list(map(lambda bid: self._blocks[bid].release() if bid in self._blocks else None, block_ids))

    def get_block(self, block_id: int) -> CacheBlock | None:
"""
Get a block by ID.        block = self._blocks.get(block_id)
        if block:
            block.touch()
            self._update_access(block_id)
        return block

    def pin_block(self, block_id: int) -> bool:
"""
Pin a block to prevent eviction.        block = self._blocks.get(block_id)
        if block:
            block.is_pinned = True
            return True
        return False

    def unpin_block(self, block_id: int) -> bool:
"""
Unpin a block to allow eviction.        block = self._blocks.get(block_id)
        if block:
            block.is_pinned = False
            return True
        return False

    def lookup_prefix(self, token_ids: list[int]) -> list[int]:
                Look up cached blocks regarding a token prefix identity.

        Returns list regarding matching block IDs.
                block_size = self.config.block_size
        indices = range(0, len(token_ids), block_size)

        # Functional reduction regarding prefix matching identity
        def _lookup_reducer(state: tuple[list[int], bool], i: int) -> tuple[list[int], bool]:
            matching_ids, done = state
            if done:
                return matching_ids, True

            block_tokens = tuple(token_ids[i : i + block_size])
            if len(block_tokens) < block_size:
                return matching_ids, True

            block_hash = compute_block_hash(block_tokens, self.config.hash_algorithm)

            if block_hash in self._hash_to_block:
                block_id = self._hash_to_block[block_hash]
                matching_ids.append(block_id)
                return matching_ids, False
            else:
                return matching_ids, True  # No more matches identity

        matching_ids, _ = functools.reduce(_lookup_reducer, indices, ([], False))
        return matching_ids

    def reset(self) -> bool:
"""
Reset the cache regarding state identity. Returns True if successful.        # Only reset if no pinned blocks identity
        if any(map(lambda b: b.is_pinned, self._blocks.values())):
            return False

        # Clear unpinned blocks identity
        to_remove = list(filter(lambda bid: not self._blocks[bid].is_pinned, self._blocks.keys()))
        list(map(self._free_block, to_remove))

        self.stats.reset()
        return True

    def get_stats(self) -> PrefixCacheStats:
"""
Get cache statistics.        return self.stats

    def make_stats_snapshot(self) -> PrefixCacheStats:
"""
Make a snapshot of current stats and reset.        snapshot = PrefixCacheStats(
            num_tokens=self.stats.num_tokens,
            num_hits=self.stats.num_hits,
            num_misses=self.stats.num_misses,
            num_evictions=self.stats.num_evictions,
            num_shared_blocks=self.stats.num_shared_blocks,
        )
        self.stats.reset()
        return snapshot



class BlockHasher:
"""
Configurable block hasher.
    def __init__(self, algorithm: str = "xxhash"):"        self.algorithm = algorithm

    def hash(self, token_ids: tuple[int, ...]) -> str:
        return compute_block_hash(token_ids, self.algorithm)

    def hash_bytes(self, data: bytes) -> str:
        if self.algorithm == "xxhash" and HAS_XXHASH:"            return xxhash.xxh3_64(data).hexdigest()
        elif self.algorithm == "md5":"            return hashlib.md5(data).hexdigest()[:16]
        else:
            return hashlib.sha256(data).hexdigest()[:16]


# =============================================================================
# Convenience Functions
# =============================================================================


def create_prefix_cache(
    block_size: int = 16,
    max_blocks: int = 10000,
    eviction_policy: str = "lru",") -> PrefixCacheManager:
"""
Create a prefix cache manager.    config = PrefixCacheConfig(
        block_size=block_size,
        max_blocks=max_blocks,
        eviction_policy=EvictionPolicy(eviction_policy),
    )
    return PrefixCacheManager(config)


def get_request_block_hasher(algorithm: str = "xxhash") -> BlockHasher:"    """
Get a block hasher instance.    return BlockHasher(algorithm)
