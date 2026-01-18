# SPDX-License-Identifier: Apache-2.0
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple
import time
from .Enums import CacheGroupType, AllocationStrategy, EvictionPolicy

@dataclass(frozen=True)
class BlockHash:
    """Immutable block hash for prefix caching."""
    hash_bytes: bytes
    
    def __hash__(self) -> int:
        return hash(self.hash_bytes)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BlockHash):
            return False
        return self.hash_bytes == other.hash_bytes
    
    @property
    def as_int(self) -> int:
        """Convert to integer for legacy compatibility."""
        return int.from_bytes(self.hash_bytes[:8], byteorder='big')


@dataclass(frozen=True)
class BlockHashWithGroupId:
    """Block hash combined with group ID for multi-group caching."""
    block_hash: BlockHash
    group_id: int
    
    def __hash__(self) -> int:
        return hash((self.block_hash, self.group_id))


@dataclass
class KVCacheBlock:
    """KV cache block metadata."""
    block_id: int
    ref_cnt: int = 0
    block_hash: Optional[BlockHashWithGroupId] = None
    is_null: bool = False
    
    # Doubly-linked list pointers for free block queue
    prev_free_block: Optional['KVCacheBlock'] = None
    next_free_block: Optional['KVCacheBlock'] = None
    
    # Timing for eviction decisions
    last_access_time: float = field(default_factory=time.time)
    access_count: int = 0
    
    def touch(self) -> None:
        """Mark block as accessed."""
        self.last_access_time = time.time()
        self.access_count += 1
    
    def reset(self) -> None:
        """Reset block state for reuse."""
        self.ref_cnt = 0
        self.block_hash = None
        self.is_null = False
        self.access_count = 0


@dataclass
class KVCacheBlocks:
    """Allocation result for multi-group KV cache."""
    blocks: Tuple[Sequence[KVCacheBlock], ...]
    
    def __add__(self, other: 'KVCacheBlocks') -> 'KVCacheBlocks':
        """Combine two KVCacheBlocks instances."""
        combined = tuple(
            list(b1) + list(b2)
            for b1, b2 in zip(self.blocks, other.blocks)
        )
        return KVCacheBlocks(combined)
    
    def get_block_ids(self) -> Tuple[List[int], ...]:
        """Get block IDs for all groups."""
        return tuple(
            [block.block_id for block in group]
            for group in self.blocks
        )
    
    def is_empty(self) -> bool:
        """Check if all groups are empty."""
        return all(len(group) == 0 for group in self.blocks)
    
    @classmethod
    def empty(cls, num_groups: int) -> 'KVCacheBlocks':
        """Create empty KVCacheBlocks."""
        return cls(tuple(() for _ in range(num_groups)))


@dataclass
class CacheGroupSpec:
    """Specification for a KV cache group."""
    group_id: int
    group_type: CacheGroupType
    block_size: int
    num_kv_heads: int
    head_dim: int
    sliding_window: Optional[int] = None
    chunk_size: Optional[int] = None
    
    @property
    def bytes_per_token(self) -> int:
        """Bytes per token in this group."""
        # 2 for K and V, 2 for FP16
        return 2 * self.num_kv_heads * self.head_dim * 2
    
    @property
    def bytes_per_block(self) -> int:
        """Bytes per block in this group."""
        return self.bytes_per_token * self.block_size


@dataclass
class CacheConfig:
    """Configuration for KV cache."""
    num_blocks: int
    block_size: int
    groups: List[CacheGroupSpec]
    enable_prefix_caching: bool = True
    eviction_policy: EvictionPolicy = EvictionPolicy.LRU
    allocation_strategy: AllocationStrategy = AllocationStrategy.GREEDY
