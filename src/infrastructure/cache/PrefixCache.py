"""
Prefix Cache System.

Hash-based content-addressable caching for LLM inference:
- Block-level caching with reference counting
- LRU/LFU/ARC eviction policies
- Cache statistics and monitoring

Inspired by vLLM's v1/core/kv_cache_utils.py architecture.
"""

from __future__ import annotations

import hashlib
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Generic, TypeVar

try:
    import xxhash
    HAS_XXHASH = True
except ImportError:
    HAS_XXHASH = False


class EvictionPolicy(str, Enum):
    """Cache eviction policy."""
    LRU = "lru"    # Least Recently Used
    LFU = "lfu"    # Least Frequently Used
    ARC = "arc"    # Adaptive Replacement Cache
    FIFO = "fifo"  # First In First Out


@dataclass
class PrefixCacheConfig:
    """Configuration for prefix cache."""
    
    block_size: int = 16  # Tokens per block
    max_blocks: int = 10000
    eviction_policy: EvictionPolicy = EvictionPolicy.LRU
    enable_sharing: bool = True
    pin_common_prefixes: bool = True
    hash_algorithm: str = "xxhash"  # xxhash, sha256, md5


@dataclass
class CacheBlock:
    """A cached block of tokens."""
    
    block_id: int
    token_ids: tuple[int, ...]
    block_hash: str
    ref_count: int = 1
    is_pinned: bool = False
    access_count: int = 0
    last_access: float = field(default_factory=time.time)
    
    def touch(self) -> None:
        """Update access time and count."""
        self.last_access = time.time()
        self.access_count += 1
    
    def acquire(self) -> None:
        """Increment reference count."""
        self.ref_count += 1
        self.touch()
    
    def release(self) -> bool:
        """Decrement reference count. Returns True if block can be freed."""
        self.ref_count = max(0, self.ref_count - 1)
        return self.ref_count == 0 and not self.is_pinned
    
    @property
    def is_freeable(self) -> bool:
        return self.ref_count == 0 and not self.is_pinned


@dataclass
class PrefixCacheStats:
    """Statistics for prefix cache performance."""
    
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
        """Record cache access."""
        self.num_tokens += num_tokens
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
            "num_tokens": self.num_tokens,
            "num_hits": self.num_hits,
            "num_misses": self.num_misses,
            "num_evictions": self.num_evictions,
            "num_shared_blocks": self.num_shared_blocks,
            "hit_rate": self.hit_rate,
            "preempted": self.preempted,
        }


def compute_block_hash(token_ids: tuple[int, ...], algorithm: str = "xxhash") -> str:
    """Compute hash for a block of tokens."""
    # Convert to bytes
    data = b"".join(t.to_bytes(4, "little", signed=True) for t in token_ids)
    
    if algorithm == "xxhash" and HAS_XXHASH:
        return xxhash.xxh3_64(data).hexdigest()
    elif algorithm == "md5":
        return hashlib.md5(data).hexdigest()[:16]
    else:  # sha256 or fallback
        return hashlib.sha256(data).hexdigest()[:16]


class PrefixCacheManager:
    """
    Manages prefix cache with hash-based content addressing.
    
    Supports block sharing across requests with same prefix.
    """
    
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
        return sum(1 for b in self._blocks.values() if b.is_freeable)
    
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
        """
        Allocate cache blocks for tokens.
        
        Returns list of block IDs (may include shared blocks).
        """
        block_size = self.config.block_size
        block_ids: list[int] = []
        num_hits = 0
        
        # Split into blocks
        for i in range(0, len(token_ids), block_size):
            block_tokens = tuple(token_ids[i:i + block_size])
            if len(block_tokens) < block_size:
                # Partial block - pad or skip
                continue
            
            block_hash = compute_block_hash(block_tokens, self.config.hash_algorithm)
            
            # Check if block exists
            if block_hash in self._hash_to_block:
                # Reuse existing block
                existing_id = self._hash_to_block[block_hash]
                existing_block = self._blocks[existing_id]
                existing_block.acquire()
                block_ids.append(existing_id)
                num_hits += 1
                self.stats.num_shared_blocks += 1
                self._update_access(existing_id)
            else:
                # Allocate new block
                new_id = self._allocate_block(block_tokens, block_hash)
                if new_id is not None:
                    block_ids.append(new_id)
        
        # Track request blocks
        self._request_blocks[request_id] = block_ids
        
        # Update stats
        total_blocks = len(token_ids) // block_size
        self.stats.record(total_blocks * block_size, num_hits * block_size)
        
        return block_ids
    
    def _allocate_block(
        self,
        token_ids: tuple[int, ...],
        block_hash: str,
    ) -> int | None:
        """Allocate a new cache block."""
        # Evict if needed
        while len(self._blocks) >= self.config.max_blocks:
            if not self._evict_one():
                return None  # Cannot evict
        
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
        """Update access tracking for eviction."""
        if block_id in self._access_order:
            self._access_order.move_to_end(block_id)
        else:
            self._access_order[block_id] = time.time()
        
        self._frequency[block_id] = self._frequency.get(block_id, 0) + 1
    
    def _evict_one(self) -> bool:
        """Evict one block based on policy. Returns True if successful."""
        policy = self.config.eviction_policy
        
        # Find eviction candidate
        candidate_id: int | None = None
        
        if policy == EvictionPolicy.LRU:
            for block_id in self._access_order:
                block = self._blocks.get(block_id)
                if block and block.is_freeable:
                    candidate_id = block_id
                    break
        
        elif policy == EvictionPolicy.LFU:
            min_freq = float('inf')
            for block_id, freq in self._frequency.items():
                block = self._blocks.get(block_id)
                if block and block.is_freeable and freq < min_freq:
                    min_freq = freq
                    candidate_id = block_id
        
        elif policy == EvictionPolicy.FIFO:
            for block_id in list(self._access_order.keys()):
                block = self._blocks.get(block_id)
                if block and block.is_freeable:
                    candidate_id = block_id
                    break
        
        else:  # ARC or default
            candidate_id = self._arc_evict()
        
        if candidate_id is None:
            return False
        
        self._free_block(candidate_id)
        self.stats.num_evictions += 1
        return True
    
    def _arc_evict(self) -> int | None:
        """ARC eviction - balance recency and frequency."""
        # Simplified ARC: prefer low-frequency among LRU candidates
        candidates = []
        for block_id in self._access_order:
            block = self._blocks.get(block_id)
            if block and block.is_freeable:
                freq = self._frequency.get(block_id, 0)
                candidates.append((block_id, freq))
                if len(candidates) >= 10:  # Check first 10 LRU candidates
                    break
        
        if not candidates:
            return None
        
        # Pick lowest frequency
        return min(candidates, key=lambda x: x[1])[0]
    
    def _free_block(self, block_id: int) -> None:
        """Free a block."""
        block = self._blocks.pop(block_id, None)
        if block:
            self._hash_to_block.pop(block.block_hash, None)
        self._access_order.pop(block_id, None)
        self._frequency.pop(block_id, None)
    
    def release_blocks(self, request_id: str) -> None:
        """Release blocks for a finished request."""
        block_ids = self._request_blocks.pop(request_id, [])
        for block_id in block_ids:
            block = self._blocks.get(block_id)
            if block:
                block.release()
    
    def get_block(self, block_id: int) -> CacheBlock | None:
        """Get a block by ID."""
        block = self._blocks.get(block_id)
        if block:
            block.touch()
            self._update_access(block_id)
        return block
    
    def pin_block(self, block_id: int) -> bool:
        """Pin a block to prevent eviction."""
        block = self._blocks.get(block_id)
        if block:
            block.is_pinned = True
            return True
        return False
    
    def unpin_block(self, block_id: int) -> bool:
        """Unpin a block to allow eviction."""
        block = self._blocks.get(block_id)
        if block:
            block.is_pinned = False
            return True
        return False
    
    def lookup_prefix(self, token_ids: list[int]) -> list[int]:
        """
        Look up cached blocks for a token prefix.
        
        Returns list of matching block IDs.
        """
        block_size = self.config.block_size
        matching_ids: list[int] = []
        
        for i in range(0, len(token_ids), block_size):
            block_tokens = tuple(token_ids[i:i + block_size])
            if len(block_tokens) < block_size:
                break
            
            block_hash = compute_block_hash(block_tokens, self.config.hash_algorithm)
            
            if block_hash in self._hash_to_block:
                block_id = self._hash_to_block[block_hash]
                matching_ids.append(block_id)
            else:
                break  # No more matches
        
        return matching_ids
    
    def reset(self) -> bool:
        """Reset the cache. Returns True if successful."""
        # Only reset if no pinned blocks
        pinned = [b for b in self._blocks.values() if b.is_pinned]
        if pinned:
            return False
        
        # Clear unpinned blocks
        to_remove = [bid for bid, b in self._blocks.items() if not b.is_pinned]
        for block_id in to_remove:
            self._free_block(block_id)
        
        self.stats.reset()
        return True
    
    def get_stats(self) -> PrefixCacheStats:
        """Get cache statistics."""
        return self.stats
    
    def make_stats_snapshot(self) -> PrefixCacheStats:
        """Make a snapshot of current stats and reset."""
        snapshot = PrefixCacheStats(
            num_tokens=self.stats.num_tokens,
            num_hits=self.stats.num_hits,
            num_misses=self.stats.num_misses,
            num_evictions=self.stats.num_evictions,
            num_shared_blocks=self.stats.num_shared_blocks,
        )
        self.stats.reset()
        return snapshot


class BlockHasher:
    """Configurable block hasher."""
    
    def __init__(self, algorithm: str = "xxhash"):
        self.algorithm = algorithm
    
    def hash(self, token_ids: tuple[int, ...]) -> str:
        return compute_block_hash(token_ids, self.algorithm)
    
    def hash_bytes(self, data: bytes) -> str:
        if self.algorithm == "xxhash" and HAS_XXHASH:
            return xxhash.xxh3_64(data).hexdigest()
        elif self.algorithm == "md5":
            return hashlib.md5(data).hexdigest()[:16]
        else:
            return hashlib.sha256(data).hexdigest()[:16]


# =============================================================================
# Convenience Functions
# =============================================================================

def create_prefix_cache(
    block_size: int = 16,
    max_blocks: int = 10000,
    eviction_policy: str = "lru",
) -> PrefixCacheManager:
    """Create a prefix cache manager."""
    config = PrefixCacheConfig(
        block_size=block_size,
        max_blocks=max_blocks,
        eviction_policy=EvictionPolicy(eviction_policy),
    )
    return PrefixCacheManager(config)


def get_request_block_hasher(algorithm: str = "xxhash") -> BlockHasher:
    """Get a block hasher instance."""
    return BlockHasher(algorithm)
