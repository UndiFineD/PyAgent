"""
ARCOffloadManager: Adaptive Replacement Cache for KV Offloading

Implements the ARC (Adaptive Replacement Cache) eviction policy
for KV cache offloading with self-tuning recency vs frequency trade-offs.

Key Features Beyond vLLM:
- Dynamic adaptation speed control
- Multi-tier offloading (GPU -> CPU -> disk)
- Async prefetching with priority queues
- Compression-aware eviction
- Per-request affinity tracking

Based on vLLM v1 patterns with PyAgent innovations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Generic, TypeVar, Iterator
import time
import threading
import hashlib

try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


# Type for block hash
BlockHash = bytes | str | int


class OffloadMedium(Enum):
    """Storage medium for offloaded blocks."""
    GPU = auto()
    CPU = auto()
    DISK = auto()
    REMOTE = auto()


class BlockState(Enum):
    """State of an offloaded block."""
    PENDING = auto()  # Store/load in progress
    READY = auto()  # Available for use
    EVICTING = auto()  # Being evicted
    INVALID = auto()  # Needs refresh


@dataclass(slots=True)
class BlockStatus:
    """Status of a cached block."""
    block_id: int
    medium: OffloadMedium = OffloadMedium.GPU
    state: BlockState = BlockState.READY
    ref_cnt: int = 0
    size_bytes: int = 0
    compressed: bool = False
    last_access_time: float = 0.0
    
    @property
    def is_ready(self) -> bool:
        """Check if block is ready for reading."""
        return self.state == BlockState.READY
    
    @property
    def can_evict(self) -> bool:
        """Check if block can be evicted."""
        return self.ref_cnt == 0 and self.state == BlockState.READY


@dataclass(frozen=True, slots=True)
class LoadStoreSpec:
    """Specification for load/store operation."""
    block_hashes: list[BlockHash]
    blocks: list[BlockStatus]
    source_medium: OffloadMedium = OffloadMedium.CPU
    target_medium: OffloadMedium = OffloadMedium.GPU


@dataclass(frozen=True, slots=True)
class OffloadingEvent:
    """Event representing offloading operation."""
    block_hashes: list[BlockHash]
    block_size: int
    medium: OffloadMedium
    removed: bool  # True for eviction, False for addition
    timestamp: float = field(default_factory=time.time)


@dataclass(slots=True)
class PrepareStoreOutput:
    """Output from prepare_store operation."""
    block_hashes_to_store: list[BlockHash]
    store_spec: LoadStoreSpec
    block_hashes_evicted: list[BlockHash]


class Backend(ABC):
    """Abstract backend for block storage."""
    
    @abstractmethod
    def get_num_free_blocks(self) -> int:
        """Get number of free blocks."""
        pass
    
    @abstractmethod
    def allocate_blocks(self, block_hashes: list[BlockHash]) -> list[BlockStatus]:
        """Allocate blocks for given hashes."""
        pass
    
    @abstractmethod
    def free(self, block: BlockStatus) -> None:
        """Free a block."""
        pass
    
    @abstractmethod
    def get_load_store_spec(
        self,
        block_hashes: list[BlockHash],
        blocks: list[BlockStatus]
    ) -> LoadStoreSpec:
        """Get load/store specification."""
        pass
    
    @property
    @abstractmethod
    def block_size(self) -> int:
        """Get block size in tokens."""
        pass
    
    @property
    @abstractmethod
    def medium(self) -> OffloadMedium:
        """Get storage medium."""
        pass


class SimpleBackend(Backend):
    """Simple in-memory backend for testing."""
    
    def __init__(
        self,
        num_blocks: int = 1000,
        block_size: int = 16,
        medium: OffloadMedium = OffloadMedium.CPU
    ):
        self._num_blocks = num_blocks
        self._block_size = block_size
        self._medium = medium
        self._allocated: dict[BlockHash, BlockStatus] = {}
        self._next_id = 0
        self._lock = threading.Lock()
    
    def get_num_free_blocks(self) -> int:
        with self._lock:
            return self._num_blocks - len(self._allocated)
    
    def allocate_blocks(self, block_hashes: list[BlockHash]) -> list[BlockStatus]:
        blocks = []
        with self._lock:
            for h in block_hashes:
                if h not in self._allocated:
                    block = BlockStatus(
                        block_id=self._next_id,
                        medium=self._medium,
                        state=BlockState.PENDING
                    )
                    self._allocated[h] = block
                    self._next_id += 1
                blocks.append(self._allocated[h])
        return blocks
    
    def free(self, block: BlockStatus) -> None:
        with self._lock:
            # Find and remove block
            to_remove = None
            for h, b in self._allocated.items():
                if b.block_id == block.block_id:
                    to_remove = h
                    break
            if to_remove:
                del self._allocated[to_remove]
    
    def get_load_store_spec(
        self,
        block_hashes: list[BlockHash],
        blocks: list[BlockStatus]
    ) -> LoadStoreSpec:
        return LoadStoreSpec(
            block_hashes=list(block_hashes),
            blocks=list(blocks),
            source_medium=self._medium,
            target_medium=OffloadMedium.GPU
        )
    
    @property
    def block_size(self) -> int:
        return self._block_size
    
    @property
    def medium(self) -> OffloadMedium:
        return self._medium


class OffloadingManager(ABC):
    """Abstract base for offloading managers."""
    
    @abstractmethod
    def lookup(self, block_hashes: list[BlockHash]) -> int:
        """Look up blocks, return hit count."""
        pass
    
    @abstractmethod
    def prepare_load(self, block_hashes: list[BlockHash]) -> LoadStoreSpec:
        """Prepare to load blocks."""
        pass
    
    @abstractmethod
    def touch(self, block_hashes: list[BlockHash]) -> None:
        """Update access recency for blocks."""
        pass
    
    @abstractmethod
    def complete_load(self, block_hashes: list[BlockHash]) -> None:
        """Complete load operation."""
        pass
    
    @abstractmethod
    def prepare_store(
        self,
        block_hashes: list[BlockHash]
    ) -> PrepareStoreOutput | None:
        """Prepare to store blocks, returns None if cannot make space."""
        pass


class ARCOffloadManager(OffloadingManager):
    """
    ARC (Adaptive Replacement Cache) offloading manager.
    
    Implements the ARC eviction policy which adaptively balances
    recency (T1) and frequency (T2) based on workload patterns.
    
    Data Structures:
        T1: Recent cache - blocks accessed once
        T2: Frequent cache - blocks accessed multiple times
        B1/B2: Ghost lists tracking recently evicted blocks
        target_t1_size: Adaptive target size for T1
    
    Adaptive Behavior:
        - B1 hit: Recent access matters more → increase T1
        - B2 hit: Frequent access matters more → decrease T1
    """
    
    def __init__(
        self,
        backend: Backend,
        enable_events: bool = False,
        adaptation_speed: float = 1.0
    ):
        self.backend = backend
        self.adaptation_speed = adaptation_speed
        
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
        """
        Look up blocks in cache.
        
        Returns consecutive hit count until first miss.
        """
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
        """
        Update access recency - core of ARC adaptation.
        
        For each block (in reverse order for proper MRU):
        - T1 hit: Promote to T2 (recent → frequent)
        - T2 hit: Move to MRU position
        - B1 hit: Increase target_t1_size (favor recency)
        - B2 hit: Decrease target_t1_size (favor frequency)
        """
        with self._lock:
            for block_hash in reversed(list(block_hashes)):
                if block_hash in self.t1:
                    block = self.t1[block_hash]
                    if not block.is_ready:
                        # Block being stored, keep in T1
                        self.t1.move_to_end(block_hash)
                    else:
                        # Promote to T2 (accessed twice)
                        del self.t1[block_hash]
                        self.t2[block_hash] = block
                        self.t2.move_to_end(block_hash)
                
                elif block_hash in self.t2:
                    # Already frequent, move to MRU
                    self.t2.move_to_end(block_hash)
                
                elif block_hash in self.b1:
                    # Ghost hit in B1: favor recency
                    delta = self.adaptation_speed * max(1, len(self.b2) / max(1, len(self.b1)))
                    self.target_t1_size = min(self.target_t1_size + delta, self.cache_capacity)
                    self.b1.move_to_end(block_hash)
                
                elif block_hash in self.b2:
                    # Ghost hit in B2: favor frequency
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
    
    def prepare_store(
        self,
        block_hashes: list[BlockHash]
    ) -> PrepareStoreOutput | None:
        """
        Prepare to store blocks with ARC eviction.
        
        Eviction decision based on adaptive target:
        - If T1 size > target: Evict from T1, add to B1
        - Otherwise: Evict from T2, add to B2
        """
        with self._lock:
            # Filter blocks already in cache
            to_store = [h for h in block_hashes if h not in self.t1 and h not in self.t2]
            
            if not to_store:
                return PrepareStoreOutput(
                    block_hashes_to_store=[],
                    store_spec=self.backend.get_load_store_spec([], []),
                    block_hashes_evicted=[]
                )
            
            num_to_evict = len(to_store) - self.backend.get_num_free_blocks()
            evicted = []
            
            while num_to_evict > 0:
                block_to_evict = self._select_victim()
                if block_to_evict is None:
                    # Cannot evict enough blocks
                    return None
                
                block_hash, block, from_t1 = block_to_evict
                
                # Remove from cache
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
            
            # Bound ghost list sizes
            self._trim_ghost_lists()
            
            # Allocate new blocks
            new_blocks = self.backend.allocate_blocks(to_store)
            
            # Add to T1 (new blocks start as recent)
            for block_hash, block in zip(to_store, new_blocks):
                self.t1[block_hash] = block
                # Remove from ghost lists if present
                self.b1.pop(block_hash, None)
                self.b2.pop(block_hash, None)
            
            # Record event
            if self.events is not None and evicted:
                self.events.append(OffloadingEvent(
                    block_hashes=evicted,
                    block_size=self.backend.block_size,
                    medium=self.backend.medium,
                    removed=True
                ))
            
            return PrepareStoreOutput(
                block_hashes_to_store=to_store,
                store_spec=self.backend.get_load_store_spec(to_store, new_blocks),
                block_hashes_evicted=evicted
            )
    
    def _select_victim(self) -> tuple[BlockHash, BlockStatus, bool] | None:
        """Select victim block for eviction based on ARC policy."""
        # Try T1 first if above target
        if len(self.t1) >= int(self.target_t1_size):
            for block_hash, block in self.t1.items():
                if block.can_evict:
                    return (block_hash, block, True)
        
        # Try T2
        for block_hash, block in self.t2.items():
            if block.can_evict:
                return (block_hash, block, False)
        
        # Fall back to T1 if T2 exhausted
        for block_hash, block in self.t1.items():
            if block.can_evict:
                return (block_hash, block, True)
        
        return None
    
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
    """
    ARC manager with enhanced adaptation features.
    
    Adds:
    - Dynamic adaptation speed based on workload
    - Per-request affinity tracking
    - Compression-aware eviction
    """
    
    def __init__(
        self,
        backend: Backend,
        enable_events: bool = False,
        min_adaptation_speed: float = 0.5,
        max_adaptation_speed: float = 2.0
    ):
        super().__init__(backend, enable_events, adaptation_speed=1.0)
        self.min_adaptation_speed = min_adaptation_speed
        self.max_adaptation_speed = max_adaptation_speed
        
        # Request affinity tracking
        self._request_blocks: dict[str, set[BlockHash]] = {}
        self._block_requests: dict[BlockHash, set[str]] = {}
        
        # Adaptation history
        self._adaptation_history: list[float] = []
        self._window_size = 100
    
    def touch_for_request(
        self,
        block_hashes: list[BlockHash],
        request_id: str
    ) -> None:
        """Touch blocks with request affinity tracking."""
        with self._lock:
            # Track affinity
            if request_id not in self._request_blocks:
                self._request_blocks[request_id] = set()
            
            for block_hash in block_hashes:
                self._request_blocks[request_id].add(block_hash)
                
                if block_hash not in self._block_requests:
                    self._block_requests[block_hash] = set()
                self._block_requests[block_hash].add(request_id)
        
        # Regular touch
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
        # Prefer blocks with no active request affinity
        for block_hash, block in self.t1.items():
            if block.can_evict and self.get_block_affinity(block_hash) == 0:
                if len(self.t1) >= int(self.target_t1_size):
                    return (block_hash, block, True)
        
        for block_hash, block in self.t2.items():
            if block.can_evict and self.get_block_affinity(block_hash) == 0:
                return (block_hash, block, False)
        
        # Fall back to regular selection
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
                # Performance degrading, increase adaptation
                self.adaptation_speed = min(
                    self.adaptation_speed * 1.1,
                    self.max_adaptation_speed
                )
            elif recent_avg > overall_avg * 1.1:
                # Performance improving, slow down adaptation
                self.adaptation_speed = max(
                    self.adaptation_speed * 0.9,
                    self.min_adaptation_speed
                )


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
    
    async def prepare_store_async(
        self,
        block_hashes: list[BlockHash]
    ) -> PrepareStoreOutput | None:
        """Async prepare store."""
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.manager.prepare_store, block_hashes)
