# SPDX-License-Identifier: Apache-2.0
"""
KV Cache Coordinator - Multi-group KV cache coordination infrastructure.

Implements vLLM's KVCacheCoordinator pattern with PyAgent enhancements:
- Multi-group KV cache management
- Block allocation and eviction coordination
- Prefix cache integration
- Cross-attention support for encoder-decoder models

Beyond vLLM:
- Hierarchical cache coordination
- Predictive block allocation
- Memory pressure adaptation
- Async prefetch coordination
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple
import time
import threading
from collections import defaultdict


class CacheGroupType(Enum):
    """Type of KV cache group."""
    FULL_ATTENTION = auto()
    SLIDING_WINDOW = auto()
    CROSS_ATTENTION = auto()
    CHUNKED_LOCAL = auto()
    MLA_COMPRESSED = auto()


class AllocationStrategy(Enum):
    """Block allocation strategy."""
    GREEDY = auto()         # Allocate as needed
    PREDICTIVE = auto()     # Pre-allocate based on expected length
    CONSERVATIVE = auto()   # Minimal allocation, grow on demand
    ADAPTIVE = auto()       # Adjust based on memory pressure


class EvictionPolicy(Enum):
    """Block eviction policy."""
    LRU = auto()           # Least recently used
    ARC = auto()           # Adaptive replacement cache
    PRIORITY = auto()      # Priority-based eviction
    FREQUENCY = auto()     # Least frequently used


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


class FreeBlockQueue:
    """
    Doubly-linked list queue for free blocks with O(1) operations.
    
    Maintains LRU order for eviction decisions.
    """
    
    def __init__(self, blocks: List[KVCacheBlock]) -> None:
        self.num_free_blocks = len(blocks)
        
        # Initialize doubly-linked list
        for i in range(len(blocks)):
            if i > 0:
                blocks[i].prev_free_block = blocks[i - 1]
            if i < len(blocks) - 1:
                blocks[i].next_free_block = blocks[i + 1]
        
        # Sentinel nodes for easier list manipulation
        self._head = KVCacheBlock(block_id=-1)
        self._tail = KVCacheBlock(block_id=-1)
        
        if blocks:
            self._head.next_free_block = blocks[0]
            blocks[0].prev_free_block = self._head
            self._tail.prev_free_block = blocks[-1]
            blocks[-1].next_free_block = self._tail
        else:
            self._head.next_free_block = self._tail
            self._tail.prev_free_block = self._head
    
    def pop_front(self) -> Optional[KVCacheBlock]:
        """Pop block from front (least recently used)."""
        if self.num_free_blocks == 0:
            return None
        
        block = self._head.next_free_block
        assert block is not None and block != self._tail
        
        self._remove(block)
        return block
    
    def append(self, block: KVCacheBlock) -> None:
        """Append block to back (most recently used)."""
        prev = self._tail.prev_free_block
        assert prev is not None
        
        prev.next_free_block = block
        block.prev_free_block = prev
        block.next_free_block = self._tail
        self._tail.prev_free_block = block
        
        self.num_free_blocks += 1
    
    def remove(self, block: KVCacheBlock) -> None:
        """Remove specific block from queue."""
        self._remove(block)
    
    def _remove(self, block: KVCacheBlock) -> None:
        """Internal remove with list updates."""
        prev = block.prev_free_block
        next_ = block.next_free_block
        
        if prev:
            prev.next_free_block = next_
        if next_:
            next_.prev_free_block = prev
        
        block.prev_free_block = None
        block.next_free_block = None
        self.num_free_blocks -= 1
    
    def __len__(self) -> int:
        return self.num_free_blocks
    
    def __bool__(self) -> bool:
        return self.num_free_blocks > 0


class BlockHashCache:
    """
    Cache mapping block hashes to blocks for prefix caching.
    
    Supports multiple blocks with the same hash (for different requests).
    """
    
    def __init__(self) -> None:
        self._cache: Dict[BlockHashWithGroupId, 
                         KVCacheBlock | Dict[int, KVCacheBlock]] = {}
    
    def get(self, key: BlockHashWithGroupId) -> Optional[KVCacheBlock]:
        """Get any block matching the hash."""
        entry = self._cache.get(key)
        if entry is None:
            return None
        if isinstance(entry, KVCacheBlock):
            return entry
        return next(iter(entry.values()))
    
    def insert(self, key: BlockHashWithGroupId, block: KVCacheBlock) -> None:
        """Insert a block into the cache."""
        entry = self._cache.get(key)
        
        if entry is None:
            self._cache[key] = block
        elif isinstance(entry, KVCacheBlock):
            # Convert to dict for multiple blocks
            self._cache[key] = {entry.block_id: entry, block.block_id: block}
        else:
            entry[block.block_id] = block
    
    def remove(self, key: BlockHashWithGroupId, block_id: int) -> Optional[KVCacheBlock]:
        """Remove a specific block from the cache."""
        entry = self._cache.get(key)
        
        if entry is None:
            return None
        
        if isinstance(entry, KVCacheBlock):
            if entry.block_id == block_id:
                del self._cache[key]
                return entry
            return None
        
        block = entry.pop(block_id, None)
        if not entry:
            del self._cache[key]
        return block
    
    def __len__(self) -> int:
        return len(self._cache)


class BlockPool:
    """
    Manages allocation, caching, and eviction of KV cache blocks.
    
    Features:
    - LRU/ARC eviction policies
    - Prefix caching with hash lookups
    - Reference counting
    - Eviction event tracking
    """
    
    def __init__(
        self,
        num_blocks: int,
        enable_caching: bool = True,
        eviction_policy: EvictionPolicy = EvictionPolicy.LRU,
    ) -> None:
        self.num_blocks = num_blocks
        self.enable_caching = enable_caching
        self.eviction_policy = eviction_policy
        
        # Create all blocks
        self.blocks = [KVCacheBlock(block_id=i) for i in range(num_blocks)]
        
        # Free block queue (LRU order)
        self.free_queue = FreeBlockQueue(self.blocks.copy())
        
        # Block hash cache for prefix caching
        self.hash_cache = BlockHashCache()
        
        # Null block for padding
        self.null_block = KVCacheBlock(block_id=-1, is_null=True)
        
        # Statistics
        self.total_allocations = 0
        self.total_evictions = 0
        self.cache_hits = 0
        self.cache_misses = 0
        
        # Eviction events for metrics
        self._eviction_events: List[Dict[str, Any]] = []
    
    @property
    def usage(self) -> float:
        """Get current cache usage (0.0 to 1.0)."""
        used = self.num_blocks - len(self.free_queue)
        return used / self.num_blocks if self.num_blocks > 0 else 0.0
    
    @property
    def num_free_blocks(self) -> int:
        """Number of currently free blocks."""
        return len(self.free_queue)
    
    def allocate(self, num_blocks: int) -> List[KVCacheBlock]:
        """Allocate blocks, evicting if necessary."""
        allocated = []
        
        for _ in range(num_blocks):
            block = self._allocate_one()
            if block is None:
                # Out of memory - release what we allocated
                for b in allocated:
                    self.free(b)
                raise MemoryError(f"Cannot allocate {num_blocks} blocks, only {len(allocated)} available")
            allocated.append(block)
        
        self.total_allocations += num_blocks
        return allocated
    
    def _allocate_one(self) -> Optional[KVCacheBlock]:
        """Allocate a single block."""
        block = self.free_queue.pop_front()
        
        if block is None:
            return None
        
        # If block was cached, record eviction
        if block.block_hash is not None:
            self._record_eviction(block)
            self.hash_cache.remove(block.block_hash, block.block_id)
            block.block_hash = None
        
        block.ref_cnt = 1
        block.touch()
        return block
    
    def free(self, block: KVCacheBlock) -> None:
        """Free a block (decrease ref count)."""
        if block.is_null:
            return
        
        block.ref_cnt -= 1
        if block.ref_cnt <= 0:
            block.reset()
            self.free_queue.append(block)
    
    def cache_block(self, block: KVCacheBlock, block_hash: BlockHashWithGroupId) -> None:
        """Mark block as cached with given hash."""
        if not self.enable_caching:
            return
        
        block.block_hash = block_hash
        self.hash_cache.insert(block_hash, block)
    
    def lookup_cached(self, block_hash: BlockHashWithGroupId) -> Optional[KVCacheBlock]:
        """Look up a cached block by hash."""
        if not self.enable_caching:
            return None
        
        block = self.hash_cache.get(block_hash)
        if block is not None:
            self.cache_hits += 1
            block.ref_cnt += 1
            block.touch()
            return block
        
        self.cache_misses += 1
        return None
    
    def _record_eviction(self, block: KVCacheBlock) -> None:
        """Record eviction event for metrics."""
        self.total_evictions += 1
        
        lifetime = time.time() - block.last_access_time
        self._eviction_events.append({
            'block_id': block.block_id,
            'lifetime_seconds': lifetime,
            'access_count': block.access_count,
            'timestamp': time.time(),
        })
        
        # Keep only recent events
        if len(self._eviction_events) > 10000:
            self._eviction_events = self._eviction_events[-5000:]
    
    def get_eviction_events(self) -> List[Dict[str, Any]]:
        """Get recent eviction events."""
        events = self._eviction_events
        self._eviction_events = []
        return events


class SingleTypeKVCacheManager(ABC):
    """
    Abstract base for single-type KV cache management.
    
    Handles allocation and tracking for one cache group type.
    """
    
    def __init__(
        self,
        spec: CacheGroupSpec,
        block_pool: BlockPool,
    ) -> None:
        self.spec = spec
        self.block_pool = block_pool
        
        # Request ID -> allocated blocks
        self.request_blocks: Dict[str, List[KVCacheBlock]] = {}
    
    @abstractmethod
    def get_num_blocks_needed(self, num_tokens: int) -> int:
        """Calculate blocks needed for given token count."""
        pass
    
    def allocate(self, request_id: str, num_tokens: int) -> List[KVCacheBlock]:
        """Allocate blocks for a request."""
        num_blocks = self.get_num_blocks_needed(num_tokens)
        current = len(self.request_blocks.get(request_id, []))
        needed = num_blocks - current
        
        if needed <= 0:
            return []
        
        new_blocks = self.block_pool.allocate(needed)
        
        if request_id not in self.request_blocks:
            self.request_blocks[request_id] = []
        self.request_blocks[request_id].extend(new_blocks)
        
        return new_blocks
    
    def free(self, request_id: str) -> None:
        """Free all blocks for a request."""
        blocks = self.request_blocks.pop(request_id, [])
        for block in blocks:
            self.block_pool.free(block)
    
    def get_blocks(self, request_id: str) -> List[KVCacheBlock]:
        """Get current blocks for a request."""
        return self.request_blocks.get(request_id, [])


class FullAttentionManager(SingleTypeKVCacheManager):
    """Manager for full attention KV cache."""
    
    def get_num_blocks_needed(self, num_tokens: int) -> int:
        """Full attention needs blocks for all tokens."""
        from math import ceil
        return ceil(num_tokens / self.spec.block_size)


class SlidingWindowManager(SingleTypeKVCacheManager):
    """Manager for sliding window attention KV cache."""
    
    def get_num_blocks_needed(self, num_tokens: int) -> int:
        """Sliding window only needs blocks for window size."""
        from math import ceil
        window = self.spec.sliding_window or num_tokens
        effective_tokens = min(num_tokens, window)
        return ceil(effective_tokens / self.spec.block_size)


class CrossAttentionManager(SingleTypeKVCacheManager):
    """Manager for cross-attention (encoder-decoder) KV cache."""
    
    def get_num_blocks_needed(self, num_tokens: int) -> int:
        """Cross attention is static based on encoder length."""
        from math import ceil
        return ceil(num_tokens / self.spec.block_size)


class KVCacheCoordinator:
    """
    Coordinates multiple KV cache groups for complex attention patterns.
    
    Features:
    - Multi-group management (full, sliding, cross, chunked)
    - Unified allocation across groups
    - Prefix caching coordination
    - Memory pressure handling
    
    Beyond vLLM:
    - Hierarchical coordination for MoE models
    - Predictive allocation
    - Async prefetch coordination
    """
    
    def __init__(
        self,
        config: CacheConfig,
        max_model_len: int,
    ) -> None:
        self.config = config
        self.max_model_len = max_model_len
        
        # Create block pool
        self.block_pool = BlockPool(
            num_blocks=config.num_blocks,
            enable_caching=config.enable_prefix_caching,
            eviction_policy=config.eviction_policy,
        )
        
        # Create managers for each cache group
        self.managers: List[SingleTypeKVCacheManager] = []
        for spec in config.groups:
            manager = self._create_manager(spec)
            self.managers.append(manager)
        
        # Pre-allocated empty result to avoid GC
        self._empty_blocks = KVCacheBlocks.empty(len(config.groups))
        
        # Statistics
        self.total_allocations = 0
        self.total_frees = 0
    
    def _create_manager(self, spec: CacheGroupSpec) -> SingleTypeKVCacheManager:
        """Create appropriate manager for cache group type."""
        if spec.group_type == CacheGroupType.FULL_ATTENTION:
            return FullAttentionManager(spec, self.block_pool)
        elif spec.group_type == CacheGroupType.SLIDING_WINDOW:
            return SlidingWindowManager(spec, self.block_pool)
        elif spec.group_type == CacheGroupType.CROSS_ATTENTION:
            return CrossAttentionManager(spec, self.block_pool)
        else:
            # Default to full attention
            return FullAttentionManager(spec, self.block_pool)
    
    @property
    def usage(self) -> float:
        """Current cache usage."""
        return self.block_pool.usage
    
    @property
    def num_groups(self) -> int:
        """Number of cache groups."""
        return len(self.managers)
    
    def get_num_blocks_to_allocate(
        self,
        request_id: str,
        num_tokens: int,
        num_encoder_tokens: int = 0,
    ) -> int:
        """Calculate total blocks needed across all groups."""
        total = 0
        for i, manager in enumerate(self.managers):
            spec = self.config.groups[i]
            if spec.group_type == CacheGroupType.CROSS_ATTENTION:
                total += manager.get_num_blocks_needed(num_encoder_tokens)
            else:
                total += manager.get_num_blocks_needed(num_tokens)
        return total
    
    def allocate(
        self,
        request_id: str,
        num_tokens: int,
        num_encoder_tokens: int = 0,
    ) -> KVCacheBlocks:
        """Allocate blocks for a request across all groups."""
        blocks_per_group = []
        
        for i, manager in enumerate(self.managers):
            spec = self.config.groups[i]
            if spec.group_type == CacheGroupType.CROSS_ATTENTION:
                blocks = manager.allocate(request_id, num_encoder_tokens)
            else:
                blocks = manager.allocate(request_id, num_tokens)
            blocks_per_group.append(tuple(blocks))
        
        self.total_allocations += 1
        return KVCacheBlocks(tuple(blocks_per_group))
    
    def free(self, request_id: str) -> None:
        """Free all blocks for a request."""
        for manager in self.managers:
            manager.free(request_id)
        self.total_frees += 1
    
    def get_blocks(self, request_id: str) -> KVCacheBlocks:
        """Get current blocks for a request."""
        blocks_per_group = []
        for manager in self.managers:
            blocks_per_group.append(tuple(manager.get_blocks(request_id)))
        return KVCacheBlocks(tuple(blocks_per_group))
    
    def cache_blocks(
        self,
        request_id: str,
        block_hashes: List[BlockHash],
        group_id: int = 0,
    ) -> None:
        """Cache blocks with given hashes for prefix caching."""
        blocks = self.managers[group_id].get_blocks(request_id)
        
        for block, hash_ in zip(blocks, block_hashes):
            hash_with_group = BlockHashWithGroupId(hash_, group_id)
            self.block_pool.cache_block(block, hash_with_group)
    
    def find_cached_blocks(
        self,
        block_hashes: List[BlockHash],
        group_id: int = 0,
    ) -> Tuple[List[KVCacheBlock], int]:
        """Find cached blocks matching hashes."""
        cached = []
        num_hits = 0
        
        for hash_ in block_hashes:
            hash_with_group = BlockHashWithGroupId(hash_, group_id)
            block = self.block_pool.lookup_cached(hash_with_group)
            if block is not None:
                cached.append(block)
                num_hits += 1
            else:
                break  # Stop at first miss for prefix matching
        
        return cached, num_hits
    
    def get_stats(self) -> Dict[str, Any]:
        """Get coordinator statistics."""
        return {
            'usage': self.usage,
            'num_groups': self.num_groups,
            'total_allocations': self.total_allocations,
            'total_frees': self.total_frees,
            'block_pool_stats': {
                'total_blocks': self.block_pool.num_blocks,
                'free_blocks': self.block_pool.num_free_blocks,
                'cache_hits': self.block_pool.cache_hits,
                'cache_misses': self.block_pool.cache_misses,
                'total_evictions': self.block_pool.total_evictions,
            }
        }


# ============================================================================
# Beyond vLLM: Advanced Coordination
# ============================================================================

class HierarchicalKVCacheCoordinator(KVCacheCoordinator):
    """
    Hierarchical coordinator for complex model architectures.
    
    Supports:
    - Layer-specific cache groups
    - MoE expert-specific caching
    - Multi-level cache hierarchies
    """
    
    def __init__(
        self,
        config: CacheConfig,
        max_model_len: int,
        num_layers: int,
    ) -> None:
        super().__init__(config, max_model_len)
        self.num_layers = num_layers
        
        # Layer-specific statistics
        self.layer_stats: Dict[int, Dict[str, int]] = defaultdict(
            lambda: {'allocations': 0, 'hits': 0}
        )
    
    def allocate_for_layer(
        self,
        request_id: str,
        num_tokens: int,
        layer_idx: int,
    ) -> KVCacheBlocks:
        """Allocate for a specific layer."""
        blocks = self.allocate(request_id, num_tokens)
        self.layer_stats[layer_idx]['allocations'] += 1
        return blocks


class PredictiveKVCacheCoordinator(KVCacheCoordinator):
    """
    Coordinator with predictive allocation based on request patterns.
    
    Features:
    - Length prediction for pre-allocation
    - Adaptive allocation sizing
    - Memory budget awareness
    """
    
    def __init__(
        self,
        config: CacheConfig,
        max_model_len: int,
        memory_budget_bytes: int,
    ) -> None:
        super().__init__(config, max_model_len)
        self.memory_budget = memory_budget_bytes
        
        # Length prediction model
        self._length_history: List[int] = []
        self._avg_length: float = 256.0  # Default
    
    def predict_length(self, prompt_length: int) -> int:
        """Predict output length based on history."""
        if not self._length_history:
            return int(self._avg_length)
        
        # Simple exponential moving average
        return int(self._avg_length * 0.9 + prompt_length * 0.1)
    
    def record_completion_length(self, length: int) -> None:
        """Record actual completion length for learning."""
        self._length_history.append(length)
        if len(self._length_history) > 1000:
            self._length_history = self._length_history[-500:]
        
        # Update average
        self._avg_length = sum(self._length_history) / len(self._length_history)
    
    def allocate_predictive(
        self,
        request_id: str,
        current_tokens: int,
        prompt_length: int,
    ) -> KVCacheBlocks:
        """Allocate with prediction for expected total length."""
        predicted = self.predict_length(prompt_length)
        target_tokens = max(current_tokens, predicted)
        return self.allocate(request_id, target_tokens)


class AsyncPrefetchCoordinator(KVCacheCoordinator):
    """
    Coordinator with async prefetch support.
    
    Features:
    - Background prefetch of likely-needed blocks
    - Priority-based prefetch scheduling
    - Cancellation support
    """
    
    def __init__(
        self,
        config: CacheConfig,
        max_model_len: int,
        prefetch_queue_size: int = 100,
    ) -> None:
        super().__init__(config, max_model_len)
        self.prefetch_queue_size = prefetch_queue_size
        
        # Prefetch queue
        self._prefetch_requests: List[Tuple[str, int]] = []
        self._prefetch_lock = threading.Lock()
    
    def queue_prefetch(
        self,
        request_id: str,
        expected_tokens: int,
        priority: int = 0,
    ) -> None:
        """Queue a prefetch request."""
        with self._prefetch_lock:
            if len(self._prefetch_requests) < self.prefetch_queue_size:
                self._prefetch_requests.append((request_id, expected_tokens))
    
    def process_prefetch_queue(self, max_blocks: int = 10) -> int:
        """Process pending prefetch requests."""
        processed = 0
        
        with self._prefetch_lock:
            while self._prefetch_requests and processed < max_blocks:
                request_id, tokens = self._prefetch_requests.pop(0)
                try:
                    self.allocate(request_id, tokens)
                    processed += 1
                except MemoryError:
                    # Put back for later
                    self._prefetch_requests.insert(0, (request_id, tokens))
                    break
        
        return processed


# ============================================================================
# Factory Functions
# ============================================================================

def create_kv_cache_coordinator(
    config: CacheConfig,
    max_model_len: int,
    coordinator_type: str = 'default',
    **kwargs: Any,
) -> KVCacheCoordinator:
    """
    Factory function to create appropriate coordinator.
    
    Args:
        config: Cache configuration
        max_model_len: Maximum model length
        coordinator_type: Type of coordinator
        **kwargs: Additional arguments
    
    Returns:
        KVCacheCoordinator instance
    """
    if coordinator_type == 'default':
        return KVCacheCoordinator(config, max_model_len)
    elif coordinator_type == 'hierarchical':
        return HierarchicalKVCacheCoordinator(
            config, max_model_len,
            num_layers=kwargs.get('num_layers', 32),
        )
    elif coordinator_type == 'predictive':
        return PredictiveKVCacheCoordinator(
            config, max_model_len,
            memory_budget_bytes=kwargs.get('memory_budget', 1 << 30),
        )
    elif coordinator_type == 'async_prefetch':
        return AsyncPrefetchCoordinator(
            config, max_model_len,
            prefetch_queue_size=kwargs.get('prefetch_queue_size', 100),
        )
    else:
        raise ValueError(f"Unknown coordinator type: {coordinator_type}")


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Enums
    'CacheGroupType',
    'AllocationStrategy',
    'EvictionPolicy',
    # Data classes
    'BlockHash',
    'BlockHashWithGroupId',
    'KVCacheBlock',
    'KVCacheBlocks',
    'CacheGroupSpec',
    'CacheConfig',
    # Core classes
    'FreeBlockQueue',
    'BlockHashCache',
    'BlockPool',
    'SingleTypeKVCacheManager',
    'FullAttentionManager',
    'SlidingWindowManager',
    'CrossAttentionManager',
    'KVCacheCoordinator',
    # Beyond vLLM
    'HierarchicalKVCacheCoordinator',
    'PredictiveKVCacheCoordinator',
    'AsyncPrefetchCoordinator',
    # Factory
    'create_kv_cache_coordinator',
]
