"""
ARCOffloadManager: Adaptive Replacement Cache for KV Offloading

Refactored to modular package structure for Phase 317.
Decomposed into types, backend, base, and manager modules.
"""

from src.infrastructure.kv_transfer.arc.types import (
    BlockHash, OffloadMedium, BlockState, BlockStatus,
    LoadStoreSpec, OffloadingEvent, PrepareStoreOutput
)
from src.infrastructure.kv_transfer.arc.backend import Backend, SimpleBackend
from src.infrastructure.kv_transfer.arc.base import OffloadingManager
from src.infrastructure.kv_transfer.arc.manager import (
    ARCOffloadManager, AdaptiveARCManager, AsyncARCManager
)

__all__ = [
    "BlockHash",
    "OffloadMedium",
    "BlockState",
    "BlockStatus",
    "LoadStoreSpec",
    "OffloadingEvent",
    "PrepareStoreOutput",
    "Backend",
    "SimpleBackend",
    "OffloadingManager",
    "ARCOffloadManager",
    "AdaptiveARCManager",
    "AsyncARCManager",
]
        if not self.pruner:
            return
            
        block = self.t1.get(block_hash) or self.t2.get(block_hash)
        if block:
            scores = self.pruner.get_importance_scores(hidden_states)
            # Use mean importance across tokens and heads for the block
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
