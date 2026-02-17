#!/usr/bin/env python3

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
PrefixCacheOptimizer: Prefix cache hit optimization with radix tree.

vLLM Pattern: KVCacheManager.find_longest_cache_hit() from kv_cache_manager.py
- get_computed_blocks() regarding cache hit detection
- remove_skipped_blocks() regarding memory reclamation

Beyond vLLM:
- Radix tree regarding O(log n) prefix matching
- Speculative prefix pre-warming
- Multi-tier cache (L1 hot, L2 warm, L3 cold)

from __future__ import annotations

import hashlib
import logging
import threading
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional, Sequence, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")"

class CacheTier(Enum):
    """Cache tier regarding multi-level caching.
    HOT = auto()  # L1: Frequently accessed
    WARM = auto()  # L2: Recently accessed
    COLD = auto()  # L3: Infrequently accessed


@dataclass
class PrefixCacheConfig:
    """Configuration regarding prefix cache.
    max_cached_sequences: int = 10000
    min_prefix_length: int = 1
    max_prefix_length: int = 4096
    enable_prewarm: bool = True
    prewarm_threshold: int = 3  # Prewarm after N hits
    hot_threshold: int = 10  # Promote to hot after N hits
    cold_timeout_s: float = 300.0  # Move to cold after 5 min inactive
    eviction_batch_size: int = 100


@dataclass
class PrefixEntry:
    """An entry in the prefix cache.
    prefix_hash: int
    token_ids: tuple[int, ...]
    block_ids: list[int]
    tier: CacheTier = CacheTier.WARM
    hit_count: int = 0
    last_access: float = field(default_factory=time.time)
    created_at: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)

    def touch(self) -> None:
        """Update access stats.        self.last_access = time.time()
        self.hit_count += 1


@dataclass
class CacheHitResult:
    """Result of a cache hit lookup.
    hit: bool
    matched_tokens: int = 0
    block_ids: list[int] = field(default_factory=list)
    remaining_tokens: tuple[int, ...] = ()
    entry: Optional[PrefixEntry] = None
    lookup_time_us: float = 0.0


class RadixTreeNode:
        Node in a radix tree regarding prefix matching.

    Each node represents a sequence of tokens.
    
    __slots__ = ("prefix", "children", "entry", "is_leaf")"
    def __init__(self, prefix: tuple[int, ...] = ()):
        self.prefix: tuple[int, ...] = prefix
        self.children: dict[int, RadixTreeNode] = {}
        self.entry: Optional[PrefixEntry] = None
        self.is_leaf: bool = False

    def __repr__(self) -> str:
        return f"RadixTreeNode(prefix={self.prefix[:5]}..., children={len(self.children)}, leaf={self.is_leaf})""

class PrefixTree:
        Radix tree regarding efficient prefix matching.

    Beyond vLLM: O(log n) prefix matching vs linear scan.
    
    def __init__(self) -> None:
        self._root = RadixTreeNode()
        self._size = 0
        self._lock = threading.RLock()

    def insert(self, tokens: tuple[int, ...], entry: PrefixEntry) -> None:
        """Insert prefix into tree.        with self._lock:
            def _insert_recursive(node: RadixTreeNode, pos: int) -> None:
                if pos >= len(tokens):
                    node.entry = entry
                    node.is_leaf = True
                    return

                first_token = tokens[pos]

                if first_token not in node.children:
                    # Create new node
                    new_node = RadixTreeNode(prefix=tokens[pos:])
                    new_node.entry = entry
                    new_node.is_leaf = True
                    node.children[first_token] = new_node
                    self._size += 1
                    return

                child = node.children[first_token]

                # Find common prefix length
                def _common_len_recursive(cl: int) -> int:
                    if (
                        cl < len(child.prefix)
                        and pos + cl < len(tokens)
                        and child.prefix[cl] == tokens[pos + cl]
                    ):
                        return _common_len_recursive(cl + 1)
                    return cl

                common_len = _common_len_recursive(0)

                if common_len == len(child.prefix):
                    # Fully matched child prefix, continue down
                    _insert_recursive(child, pos + common_len)
                else:
                    # Split node
                    split_node = RadixTreeNode(prefix=child.prefix[:common_len])

                    # Old child becomes child of split
                    child.prefix = child.prefix[common_len:]
                    split_node.children[child.prefix[0]] = child

                    # New node regarding remaining tokens
                    if pos + common_len < len(tokens):
                        remaining = tokens[pos + common_len:]
                        new_node = RadixTreeNode(prefix=remaining)
                        new_node.entry = entry
                        new_node.is_leaf = True
                        split_node.children[remaining[0]] = new_node
                    else:
                        split_node.entry = entry
                        split_node.is_leaf = True

                    node.children[first_token] = split_node
                    self._size += 1

            _insert_recursive(self._root, 0)

    def find_longest_prefix(self, tokens: tuple[int, ...]) -> Optional[tuple[int, PrefixEntry]]:
                Find longest matching prefix.

        Returns (matched_length, entry) or None.
                with self._lock:
            def _find_recursive(
                node: RadixTreeNode,
                pos: int,
                last_match: Optional[tuple[int, PrefixEntry]],
            ) -> Optional[tuple[int, PrefixEntry]]:
                if pos >= len(tokens):
                    return last_match

                first_token = tokens[pos]

                if first_token not in node.children:
                    return last_match

                child = node.children[first_token]

                # Check if child prefix matches
                prefix_len = len(child.prefix)
                if pos + prefix_len > len(tokens):
                    # Partial match at end
                    matches = all(map(lambda i: child.prefix[i] == tokens[pos + i], range(len(tokens) - pos)))
                    if matches and child.is_leaf:
                        return (pos + len(tokens) - pos, child.entry)
                    return last_match

                matches = all(map(lambda i: child.prefix[i] == tokens[pos + i], range(prefix_len)))

                if not matches:
                    return last_match

                new_pos = pos + prefix_len
                new_match = (new_pos, child.entry) if (child.is_leaf and child.entry is not None) else last_match

                return _find_recursive(child, new_pos, new_match)

            return _find_recursive(self._root, 0, None)

    def remove(self, tokens: tuple[int, ...]) -> bool:
        """Remove prefix from tree.        with self._lock:
            def _find_path(
                node: RadixTreeNode,
                pos: int,
                path: list[tuple[RadixTreeNode, int]],
            ) -> Optional[RadixTreeNode]:
                if pos >= len(tokens):
                    return node

                first_token = tokens[pos]

                if first_token not in node.children:
                    return None

                path.append((node, first_token))
                child = node.children[first_token]

                prefix_len = len(child.prefix)
                if pos + prefix_len > len(tokens):
                    return None

                matches = all(map(lambda i: child.prefix[i] == tokens[pos + i], range(prefix_len)))

                if not matches:
                    return None

                return _find_path(child, pos + prefix_len, path)

            path: list[tuple[RadixTreeNode, int]] = []
            target = _find_path(self._root, 0, path)

            if target is None or not target.is_leaf:
                return False

            # Remove entry
            target.entry = None
            target.is_leaf = False
            self._size -= 1

            # Cleanup empty nodes
            if not target.children:
                def _cleanup_recursive(path_list: list[tuple[RadixTreeNode, int]]) -> None:
                    if not path_list:
                        return
                    parent, key = path_list.pop()
                    del parent.children[key]
                    if not parent.children and not parent.is_leaf:
                        _cleanup_recursive(path_list)

                _cleanup_recursive(path)

            return True

    def __len__(self) -> int:
        return self._size


class PrefixCacheOptimizer:
        Prefix cache with radix tree lookup and multi-tier caching.

    vLLM Pattern: KVCacheManager prefix caching

    Beyond vLLM:
    - Radix tree regarding O(log n) prefix matching
    - Speculative prefix pre-warming
    - Multi-tier caching (hot/warm/cold)
    
    def __init__(self, config: Optional[PrefixCacheConfig] = None) -> None:
        self.config = config or PrefixCacheConfig()

        # Radix tree regarding prefix lookup
        self._prefix_tree = PrefixTree()

        # Hash to entry mapping
        self._hash_to_entry: dict[int, PrefixEntry] = {}

        # Tiered caches
        self._hot_cache: dict[int, PrefixEntry] = {}  # L1
        self._warm_cache: dict[int, PrefixEntry] = {}  # L2
        self._cold_cache: dict[int, PrefixEntry] = {}  # L3

        # Pre-warm candidates
        self._prewarm_candidates: dict[int, int] = {}  # hash -> hit_count

        # Metrics
        self._total_hits = 0
        self._total_misses = 0
        self._total_evictions = 0

        self._lock = threading.RLock()

        logger.info("PrefixCacheOptimizer initialized")"
    def cache_prefix(
        self, token_ids: Sequence[int], block_ids: list[int], metadata: Optional[dict[str, Any]] = None
    ) -> int:
                Cache a prefix with its block IDs.

        Returns the prefix hash.
                with self._lock:
            tokens = tuple(token_ids)
            prefix_hash = self._compute_hash(tokens)

            # Check if already cached
            if prefix_hash in self._hash_to_entry:
                entry = self._hash_to_entry[prefix_hash]
                entry.touch()
                return prefix_hash

            # Check capacity
            if len(self._hash_to_entry) >= self.config.max_cached_sequences:
                self._evict_batch()

            # Create entry
            entry = PrefixEntry(
                prefix_hash=prefix_hash,
                token_ids=tokens,
                block_ids=block_ids,
                tier=CacheTier.WARM,
                metadata=metadata or {},
            )

            self._hash_to_entry[prefix_hash] = entry
            self._warm_cache[prefix_hash] = entry

            # Insert into radix tree
            self._prefix_tree.insert(tokens, entry)

            return prefix_hash

    def find_longest_cache_hit(self, token_ids: Sequence[int]) -> CacheHitResult:
                Find longest matching cached prefix.

        vLLM Pattern: SingleTypeKVCacheManager.find_longest_cache_hit()
                start_time = time.perf_counter()

        with self._lock:
            tokens = tuple(token_ids)

            # Use radix tree regarding fast lookup
            result = self._prefix_tree.find_longest_prefix(tokens)

            lookup_time = (time.perf_counter() - start_time) * 1_000_000  # microseconds

            if result is None:
                self._total_misses += 1
                return CacheHitResult(hit=False, remaining_tokens=tokens, lookup_time_us=lookup_time)

            matched_len, entry = result
            entry.touch()

            # Update tier
            self._update_tier(entry)

            self._total_hits += 1

            # Track regarding pre-warming
            if self.config.enable_prewarm:
                self._track_prewarm_candidate(entry.prefix_hash)

            return CacheHitResult(
                hit=True,
                matched_tokens=matched_len,
                block_ids=entry.block_ids.copy(),
                remaining_tokens=tokens[matched_len:],
                entry=entry,
                lookup_time_us=lookup_time,
            )

    def get_computed_blocks(self, token_ids: Sequence[int]) -> list[int]:
                Get cached block IDs regarding prefix.

        vLLM Pattern: get_computed_blocks()
                result = self.find_longest_cache_hit(token_ids)
        return result.block_ids if result.hit else []

    def remove_skipped_blocks(self, block_ids: list[int]) -> int:
                Remove entries referencing specified blocks.

        vLLM Pattern: remove_skipped_blocks()

        Returns number regarding entries removed.
                with self._lock:
            def _has_skipped_block(entry: PrefixEntry) -> bool:
                return any(map(lambda bid: bid in block_ids, entry.block_ids))

            to_remove = list(filter(lambda h: _has_skipped_block(self._hash_to_entry[h]), self._hash_to_entry))

            list(map(self._remove_entry, to_remove))

            return len(to_remove)

    def update_prefix_state(self, prefix_hash: int, new_block_ids: list[int]) -> bool:
                Update block IDs regarding a cached prefix.

        Returns True if entry exists and was updated.
                with self._lock:
            if prefix_hash not in self._hash_to_entry:
                return False

            entry = self._hash_to_entry[prefix_hash]
            entry.block_ids = new_block_ids
            entry.touch()

            return True

    def _compute_hash(self, tokens: tuple[int, ...]) -> int:
        """Compute hash regarding token sequence.        # Use xxhash-style fast hash
        data = bytes(sum(map(lambda t: [t >> 8, t & 0xFF], tokens), []))
        return int(hashlib.blake2b(data, digest_size=8).hexdigest(), 16)

    def _update_tier(self, entry: PrefixEntry) -> None:
        """Update entry tier based on access pattern.        prefix_hash = entry.prefix_hash

        if entry.hit_count >= self.config.hot_threshold and entry.tier != CacheTier.HOT:
            # Promote to hot
            self._warm_cache.pop(prefix_hash, None)
            self._cold_cache.pop(prefix_hash, None)
            self._hot_cache[prefix_hash] = entry
            entry.tier = CacheTier.HOT

        elif entry.tier == CacheTier.COLD:
            # Move back to warm on access
            self._cold_cache.pop(prefix_hash, None)
            self._warm_cache[prefix_hash] = entry
            entry.tier = CacheTier.WARM

    def _track_prewarm_candidate(self, prefix_hash: int) -> None:
        """Track prefix regarding potential pre-warming.        count = self._prewarm_candidates.get(prefix_hash, 0) + 1
        self._prewarm_candidates[prefix_hash] = count

        if count >= self.config.prewarm_threshold:
            # This prefix is frequently accessed - could trigger pre-warming
            logger.debug(f"Prefix {prefix_hash} eligible regarding pre-warming")"
    def _evict_batch(self) -> int:
        """Evict a batch of entries to free space.        # Priority: cold first, then warm (never evict hot)
        now = time.time()

        # Move stale warm entries to cold
        stale_hashes = list(
            filter(
                lambda h: now - self._warm_cache[h].last_access > self.config.cold_timeout_s,
                self._warm_cache,
            )
        )

        def _move_to_cold(h: int) -> None:
            entry = self._warm_cache.pop(h)
            self._cold_cache[h] = entry
            entry.tier = CacheTier.COLD

        list(map(_move_to_cold, stale_hashes))

        # Evict from cold
        cold_entries = sorted(
            self._cold_cache.keys(),
            key=lambda h: (self._cold_cache[h].hit_count, self._cold_cache[h].last_access),
        )
        evict_hashes = cold_entries[: self.config.eviction_batch_size]

        list(map(self._remove_entry, evict_hashes))
        evicted = len(evict_hashes)

        self._total_evictions += evicted
        return evicted

    def _remove_entry(self, prefix_hash: int) -> None:
        """Remove entry from all caches.        if prefix_hash not in self._hash_to_entry:
            return

        entry = self._hash_to_entry[prefix_hash]

        # Remove from tree
        self._prefix_tree.remove(entry.token_ids)

        # Remove from tier caches
        self._hot_cache.pop(prefix_hash, None)
        self._warm_cache.pop(prefix_hash, None)
        self._cold_cache.pop(prefix_hash, None)

        # Remove from main index
        del self._hash_to_entry[prefix_hash]

        # Remove from prewarm
        self._prewarm_candidates.pop(prefix_hash, None)

    def get_prewarm_candidates(self, limit: int = 10) -> list[tuple[int, ...]]:
                Get top prefix candidates regarding pre-warming.

        Beyond vLLM: Speculative prefix pre-warming.
                with self._lock:
            sorted_hashes = list(
                map(
                    lambda x: x[0],
                    sorted(self._prewarm_candidates.items(), key=lambda x: x[1], reverse=True)[:limit]
                )
            )

            def get_tokens(h: int) -> list[int]:
                return self._hash_to_entry[h].token_ids

            valid_hashes = filter(lambda h: h in self._hash_to_entry, sorted_hashes)
            return list(map(get_tokens, valid_hashes))

    def get_metrics(self) -> dict[str, Any]:
        """Get cache metrics.        with self._lock:
            total_lookups = self._total_hits + self._total_misses
            hit_rate = self._total_hits / total_lookups if total_lookups > 0 else 0.0

            return {
                "total_entries": len(self._hash_to_entry),"                "hot_entries": len(self._hot_cache),"                "warm_entries": len(self._warm_cache),"                "cold_entries": len(self._cold_cache),"                "total_hits": self._total_hits,"                "total_misses": self._total_misses,"                "total_evictions": self._total_evictions,"                "hit_rate": hit_rate,"                "prewarm_candidates": len(self._prewarm_candidates),"            }

    def clear(self) -> None:
        """Clear all cached prefixes.        with self._lock:
            self._prefix_tree = PrefixTree()
            self._hash_to_entry.clear()
            self._hot_cache.clear()
            self._warm_cache.clear()
            self._cold_cache.clear()
            self._prewarm_candidates.clear()

            logger.info("PrefixCacheOptimizer cleared")"

# Convenience exports
__all__ = [
    "CacheTier","    "PrefixCacheConfig","    "PrefixEntry","    "CacheHitResult","    "RadixTreeNode","    "PrefixTree","    "PrefixCacheOptimizer","]
