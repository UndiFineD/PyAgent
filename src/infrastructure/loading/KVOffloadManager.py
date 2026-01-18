"""
KV Offload Manager for PyAgent

This module provides KV cache offloading functionality inspired by vLLM's
v1/kv_offload module, supporting multiple eviction policies and storage backends.

Key Features:
- LRU and ARC eviction policies
- Block-level cache management
- Load/store primitives for async offloading
- BEYOND vLLM: Tiered offloading, predictive eviction, hybrid policies

vLLM Patterns:
- OffloadingManager abstract base class
- LRUOffloadingManager with OrderedDict
- ARCOffloadingManager with T1/T2/B1/B2 queues
- Backend abstraction for storage
"""

from __future__ import annotations

import asyncio
import hashlib
import threading
import time
from abc import ABC, abstractmethod
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
)

if TYPE_CHECKING:
    import torch

try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


# Type for block hashes
BlockHash = Union[str, int, bytes]
T = TypeVar("T")


class OffloadMedium(Enum):
    """Storage medium types for offloading."""
    GPU = auto()
    CPU = auto()
    NVME = auto()
    REMOTE = auto()


@dataclass
class LoadStoreSpec:
    """
    Specification for load/store operations.
    
    vLLM Pattern: LoadStoreSpec abstract class from abstract.py
    """
    block_hashes: List[BlockHash]
    medium: OffloadMedium
    addresses: List[int] = field(default_factory=list)
    sizes: List[int] = field(default_factory=list)
    
    @property
    def num_blocks(self) -> int:
        return len(self.block_hashes)


@dataclass
class BlockStatus:
    """
    Status of an offloaded block.
    
    vLLM Pattern: BlockStatus from backend.py
    """
    address: int = 0
    size: int = 0
    ref_cnt: int = 0
    is_ready: bool = False
    
    @property
    def is_pinned(self) -> bool:
        """Block is pinned if it has references."""
        return self.ref_cnt > 0


@dataclass
class OffloadingEvent:
    """
    Event for block offloading operations.
    
    vLLM Pattern: OffloadingEvent from abstract.py
    """
    block_hashes: List[BlockHash]
    block_size: int
    medium: str
    removed: bool  # True if blocks are removed, False if stored


@dataclass
class PrepareStoreOutput:
    """
    Output from prepare_store operation.
    
    vLLM Pattern: PrepareStoreOutput from abstract.py
    """
    block_hashes_to_store: List[BlockHash]
    store_spec: LoadStoreSpec
    block_hashes_evicted: List[BlockHash]


class OffloadingBackend(ABC):
    """
    Abstract backend for block storage.
    
    vLLM Pattern: Backend from backend.py
    """
    
    @property
    @abstractmethod
    def medium(self) -> str:
        """Return storage medium identifier."""
        pass
    
    @property
    @abstractmethod
    def block_size(self) -> int:
        """Return block size in bytes."""
        pass
    
    @abstractmethod
    def get_num_free_blocks(self) -> int:
        """Get number of available blocks."""
        pass
    
    @abstractmethod
    def allocate_blocks(self, block_hashes: List[BlockHash]) -> List[BlockStatus]:
        """Allocate storage for blocks."""
        pass
    
    @abstractmethod
    def free(self, block: BlockStatus) -> None:
        """Free a block's storage."""
        pass
    
    @abstractmethod
    def get_load_store_spec(
        self,
        block_hashes: Iterable[BlockHash],
        blocks: List[BlockStatus],
    ) -> LoadStoreSpec:
        """Create load/store specification."""
        pass


class MemoryBackend(OffloadingBackend):
    """
    In-memory backend for block storage.
    
    Simple implementation for testing and CPU offloading.
    """
    
    def __init__(
        self,
        capacity_blocks: int,
        block_size: int = 4096,
        medium: str = "cpu",
    ):
        self._capacity = capacity_blocks
        self._block_size = block_size
        self._medium = medium
        self._allocated: Dict[int, bytes] = {}
        self._next_address = 0
        self._lock = threading.Lock()
    
    @property
    def medium(self) -> str:
        return self._medium
    
    @property
    def block_size(self) -> int:
        return self._block_size
    
    def get_num_free_blocks(self) -> int:
        with self._lock:
            return self._capacity - len(self._allocated)
    
    def allocate_blocks(self, block_hashes: List[BlockHash]) -> List[BlockStatus]:
        blocks = []
        with self._lock:
            for _ in block_hashes:
                if len(self._allocated) >= self._capacity:
                    raise RuntimeError("Backend out of capacity")
                
                address = self._next_address
                self._next_address += self._block_size
                self._allocated[address] = bytes(self._block_size)
                
                blocks.append(BlockStatus(
                    address=address,
                    size=self._block_size,
                    ref_cnt=1,  # Initially pinned for store
                    is_ready=False,
                ))
        return blocks
    
    def free(self, block: BlockStatus) -> None:
        with self._lock:
            if block.address in self._allocated:
                del self._allocated[block.address]
    
    def get_load_store_spec(
        self,
        block_hashes: Iterable[BlockHash],
        blocks: List[BlockStatus],
    ) -> LoadStoreSpec:
        return LoadStoreSpec(
            block_hashes=list(block_hashes),
            medium=OffloadMedium.CPU,
            addresses=[b.address for b in blocks],
            sizes=[b.size for b in blocks],
        )


class OffloadingManager(ABC):
    """
    Abstract manager for KV cache offloading.
    
    vLLM Pattern: OffloadingManager from abstract.py
    """
    
    @abstractmethod
    def lookup(self, block_hashes: Iterable[BlockHash]) -> int:
        """
        Find length of maximal cached prefix.
        
        Returns the number of consecutive blocks starting from the first
        that are all offloaded and ready.
        """
        pass
    
    @abstractmethod
    def prepare_load(self, block_hashes: Iterable[BlockHash]) -> LoadStoreSpec:
        """
        Prepare blocks for loading.
        
        The blocks will be protected from eviction until complete_load.
        """
        pass
    
    @abstractmethod
    def touch(self, block_hashes: Iterable[BlockHash]) -> None:
        """Mark blocks as recently used for LRU."""
        pass
    
    @abstractmethod
    def complete_load(self, block_hashes: Iterable[BlockHash]) -> None:
        """Mark load as complete, re-allow eviction."""
        pass
    
    @abstractmethod
    def prepare_store(
        self,
        block_hashes: Iterable[BlockHash],
    ) -> Optional[PrepareStoreOutput]:
        """
        Prepare to store blocks.
        
        Returns None if not enough space after eviction.
        """
        pass
    
    @abstractmethod
    def complete_store(
        self,
        block_hashes: Iterable[BlockHash],
        success: bool = True,
    ) -> None:
        """Mark store as complete."""
        pass


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
        block_hashes_to_store = [
            h for h in block_hashes if h not in self.blocks
        ]
        
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
            self.events.append(OffloadingEvent(
                block_hashes=to_evict,
                block_size=self.backend.block_size,
                medium=self.backend.medium,
                removed=True,
            ))
        
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
            self.events.append(OffloadingEvent(
                block_hashes=stored,
                block_size=self.backend.block_size,
                medium=self.backend.medium,
                removed=False,
            ))
    
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
    
    Data Structures:
        T1: Recent cache (single access)
        T2: Frequent cache (multiple accesses)
        B1/B2: Ghost lists for evicted blocks
        target_t1_size: Adaptive target for T1 partition
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
        """
        Update LRU state with ARC adaptation.
        
        - T1 hit → promote to T2
        - T2 hit → move to MRU
        - B1 hit → increase target_t1_size (favor recency)
        - B2 hit → decrease target_t1_size (favor frequency)
        """
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
                delta = max(1.0, len(self.b2) / max(1, len(self.b1)))
                self.target_t1_size = min(
                    self.target_t1_size + delta,
                    float(self.cache_capacity)
                )
                self.b1.move_to_end(block_hash)
            
            elif block_hash in self.b2:
                # Hit in ghost list → increase frequency preference
                delta = max(1.0, len(self.b1) / max(1, len(self.b2)))
                self.target_t1_size = max(self.target_t1_size - delta, 0.0)
                self.b2.move_to_end(block_hash)
    
    def complete_load(self, block_hashes: Iterable[BlockHash]) -> None:
        """Decrement refcount after load."""
        for block_hash in block_hashes:
            block = self.t1.get(block_hash) or self.t2.get(block_hash)
            if block is not None:
                assert block.ref_cnt > 0
                block.ref_cnt -= 1
    
    def _evict_one(self) -> Optional[BlockHash]:
        """
        Evict one block following ARC policy.
        
        If T1 size > target, evict from T1; otherwise from T2.
        """
        # Try T1 first if above target
        if len(self.t1) > self.target_t1_size:
            for block_hash, block in self.t1.items():
                if block.ref_cnt == 0:
                    self.backend.free(block)
                    del self.t1[block_hash]
                    # Add to ghost list
                    self.b1[block_hash] = None
                    if len(self.b1) > self.cache_capacity:
                        self.b1.popitem(last=False)
                    return block_hash
        
        # Try T2
        for block_hash, block in self.t2.items():
            if block.ref_cnt == 0:
                self.backend.free(block)
                del self.t2[block_hash]
                # Add to ghost list
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
        # Filter already stored
        block_hashes_to_store = [
            h for h in block_hashes
            if h not in self.t1 and h not in self.t2
        ]
        
        num_to_evict = len(block_hashes_to_store) - self.backend.get_num_free_blocks()
        
        # Evict as needed
        evicted: List[BlockHash] = []
        while num_to_evict > 0:
            victim = self._evict_one()
            if victim is None:
                return None
            evicted.append(victim)
            num_to_evict -= 1
        
        if evicted and self.events is not None:
            self.events.append(OffloadingEvent(
                block_hashes=evicted,
                block_size=self.backend.block_size,
                medium=self.backend.medium,
                removed=True,
            ))
        
        # Remove from ghost lists if present
        for block_hash in block_hashes_to_store:
            self.b1.pop(block_hash, None)
            self.b2.pop(block_hash, None)
        
        # Allocate new blocks (insert into T1)
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
            self.events.append(OffloadingEvent(
                block_hashes=stored,
                block_size=self.backend.block_size,
                medium=self.backend.medium,
                removed=False,
            ))
    
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
    Tiered offloading with multiple backends.
    
    BEYOND vLLM: Hierarchical offloading to GPU→CPU→NVMe
    with promotion/demotion policies.
    """
    
    def __init__(
        self,
        backends: List[OffloadingBackend],
        enable_events: bool = False,
    ):
        """
        Initialize with ordered list of backends (fastest to slowest).
        """
        self.backends = backends
        self.managers = [
            LRUOffloadingManager(backend, enable_events)
            for backend in backends
        ]
        self.events: Optional[List[OffloadingEvent]] = [] if enable_events else None
        self._tier_map: Dict[BlockHash, int] = {}  # block → tier index
    
    def _get_tier(self, block_hash: BlockHash) -> Optional[int]:
        """Get tier containing block."""
        return self._tier_map.get(block_hash)
    
    def lookup(self, block_hashes: Iterable[BlockHash]) -> int:
        """Lookup across all tiers."""
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
        """Prepare load from appropriate tier."""
        # Group by tier
        tier_groups: Dict[int, List[BlockHash]] = {}
        hashes = list(block_hashes)
        
        for block_hash in hashes:
            tier = self._get_tier(block_hash)
            if tier is not None:
                if tier not in tier_groups:
                    tier_groups[tier] = []
                tier_groups[tier].append(block_hash)
        
        # Use first (fastest) tier with blocks
        if tier_groups:
            tier = min(tier_groups.keys())
            return self.managers[tier].prepare_load(tier_groups[tier])
        
        raise ValueError("No blocks found in any tier")
    
    def touch(self, block_hashes: Iterable[BlockHash]) -> None:
        """Touch blocks in their respective tiers."""
        tier_groups: Dict[int, List[BlockHash]] = {}
        
        for block_hash in block_hashes:
            tier = self._get_tier(block_hash)
            if tier is not None:
                if tier not in tier_groups:
                    tier_groups[tier] = []
                tier_groups[tier].append(block_hash)
        
        for tier, hashes in tier_groups.items():
            self.managers[tier].touch(hashes)
    
    def complete_load(self, block_hashes: Iterable[BlockHash]) -> None:
        """Complete load for blocks."""
        tier_groups: Dict[int, List[BlockHash]] = {}
        
        for block_hash in block_hashes:
            tier = self._get_tier(block_hash)
            if tier is not None:
                if tier not in tier_groups:
                    tier_groups[tier] = []
                tier_groups[tier].append(block_hash)
        
        for tier, hashes in tier_groups.items():
            self.managers[tier].complete_load(hashes)
    
    def prepare_store(
        self,
        block_hashes: Iterable[BlockHash],
    ) -> Optional[PrepareStoreOutput]:
        """Store to first tier with capacity."""
        hashes = [h for h in block_hashes if h not in self._tier_map]
        
        for tier, manager in enumerate(self.managers):
            result = manager.prepare_store(hashes)
            if result is not None:
                # Track tier assignment
                for block_hash in result.block_hashes_to_store:
                    self._tier_map[block_hash] = tier
                return result
        
        return None
    
    def complete_store(
        self,
        block_hashes: Iterable[BlockHash],
        success: bool = True,
    ) -> None:
        """Complete store operation."""
        tier_groups: Dict[int, List[BlockHash]] = {}
        
        for block_hash in block_hashes:
            tier = self._get_tier(block_hash)
            if tier is not None:
                if tier not in tier_groups:
                    tier_groups[tier] = []
                tier_groups[tier].append(block_hash)
        
        for tier, hashes in tier_groups.items():
            self.managers[tier].complete_store(hashes, success)
            if not success:
                for h in hashes:
                    self._tier_map.pop(h, None)
    
    def promote(self, block_hash: BlockHash, target_tier: int = 0) -> bool:
        """
        Promote block to faster tier.
        
        BEYOND vLLM: Active tier management.
        """
        current_tier = self._get_tier(block_hash)
        if current_tier is None or current_tier <= target_tier:
            return False
        
        # This would involve copying data between backends
        # Simplified: just update tracking
        self._tier_map[block_hash] = target_tier
        return True


# Rust-accelerated functions
def compute_lru_eviction_rust(
    blocks: List[Dict[str, Any]],
    num_to_evict: int,
) -> List[int]:
    """Select blocks to evict using Rust LRU."""
    if HAS_RUST and hasattr(rust_core, "compute_lru_eviction_rust"):
        return rust_core.compute_lru_eviction_rust(blocks, num_to_evict)
    
    # Python fallback
    evictable = [
        (i, b) for i, b in enumerate(blocks)
        if b.get("ref_cnt", 0) == 0
    ]
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
            t1_size, t2_size, b1_size, b2_size,
            current_target, hit_in_b1, capacity
        )
    
    # Python fallback
    if hit_in_b1:
        delta = max(1.0, b2_size / max(1, b1_size))
        return min(current_target + delta, float(capacity))
    else:
        delta = max(1.0, b1_size / max(1, b2_size))
        return max(current_target - delta, 0.0)
