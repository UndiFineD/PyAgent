# SPDX-License-Identifier: Apache-2.0
import time
from typing import Dict, List, Optional, Any
from .Enums import EvictionPolicy
from .DataClasses import KVCacheBlock, BlockHashWithGroupId

class FreeBlockQueue:
    """
    Doubly-linked list queue for free blocks with O(1) operations.
    Maintains LRU order for eviction decisions.
    """
    def __init__(self, blocks: List[KVCacheBlock]) -> None:
        self.num_free_blocks = len(blocks)
        for i in range(len(blocks)):
            if i > 0:
                blocks[i].prev_free_block = blocks[i - 1]
            if i < len(blocks) - 1:
                blocks[i].next_free_block = blocks[i + 1]
        
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
        if self.num_free_blocks == 0:
            return None
        block = self._head.next_free_block
        self._remove(block)
        return block
    
    def append(self, block: KVCacheBlock) -> None:
        prev = self._tail.prev_free_block
        prev.next_free_block = block
        block.prev_free_block = prev
        block.next_free_block = self._tail
        self._tail.prev_free_block = block
        self.num_free_blocks += 1
    
    def remove(self, block: KVCacheBlock) -> None:
        self._remove(block)
    
    def _remove(self, block: KVCacheBlock) -> None:
        prev = block.prev_free_block
        next_ = block.next_free_block
        if prev: prev.next_free_block = next_
        if next_: next_.prev_free_block = prev
        block.prev_free_block = None
        block.next_free_block = None
        self.num_free_blocks -= 1
    
    def __len__(self) -> int: return self.num_free_blocks
    def __bool__(self) -> bool: return self.num_free_blocks > 0


class BlockHashCache:
    """Cache mapping block hashes to blocks for prefix caching."""
    def __init__(self) -> None:
        self._cache: Dict[BlockHashWithGroupId, KVCacheBlock | Dict[int, KVCacheBlock]] = {}
    
    def get(self, key: BlockHashWithGroupId) -> Optional[KVCacheBlock]:
        entry = self._cache.get(key)
        if entry is None: return None
        if isinstance(entry, KVCacheBlock): return entry
        return next(iter(entry.values()))
    
    def insert(self, key: BlockHashWithGroupId, block: KVCacheBlock) -> None:
        entry = self._cache.get(key)
        if entry is None:
            self._cache[key] = block
        elif isinstance(entry, KVCacheBlock):
            self._cache[key] = {entry.block_id: entry, block.block_id: block}
        else:
            entry[block.block_id] = block
    
    def remove(self, key: BlockHashWithGroupId, block_id: int) -> Optional[KVCacheBlock]:
        entry = self._cache.get(key)
        if entry is None: return None
        if isinstance(entry, KVCacheBlock):
            if entry.block_id == block_id:
                del self._cache[key]; return entry
            return None
        block = entry.pop(block_id, None)
        if not entry: del self._cache[key]
        return block
    
    def __len__(self) -> int: return len(self._cache)


class BlockPool:
    """Manages allocation, caching, and eviction of KV cache blocks."""
    def __init__(self, num_blocks: int, enable_caching: bool = True, eviction_policy: EvictionPolicy = EvictionPolicy.LRU) -> None:
        self.num_blocks = num_blocks
        self.enable_caching = enable_caching
        self.eviction_policy = eviction_policy
        self.blocks = [KVCacheBlock(block_id=i) for i in range(num_blocks)]
        self.free_queue = FreeBlockQueue(self.blocks.copy())
        self.hash_cache = BlockHashCache()
        self.null_block = KVCacheBlock(block_id=-1, is_null=True)
        self.total_allocations = 0
        self.total_evictions = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self._eviction_events: List[Dict[str, Any]] = []
    
    @property
    def usage(self) -> float:
        used = self.num_blocks - len(self.free_queue)
        return used / self.num_blocks if self.num_blocks > 0 else 0.0
    
    @property
    def num_free_blocks(self) -> int: return len(self.free_queue)
    
    def allocate(self, num_blocks: int) -> List[KVCacheBlock]:
        allocated = []
        for _ in range(num_blocks):
            block = self._allocate_one()
            if block is None:
                for b in allocated: self.free(b)
                raise MemoryError(f"Cannot allocate {num_blocks} blocks")
            allocated.append(block)
        self.total_allocations += num_blocks
        return allocated
    
    def _allocate_one(self) -> Optional[KVCacheBlock]:
        block = self.free_queue.pop_front()
        if block is None: return None
        if block.block_hash is not None:
            self._record_eviction(block)
            self.hash_cache.remove(block.block_hash, block.block_id)
            block.block_hash = None
        block.ref_cnt = 1
        block.touch()
        return block
    
    def free(self, block: KVCacheBlock) -> None:
        if block.is_null: return
        block.ref_cnt -= 1
        if block.ref_cnt <= 0:
            block.reset()
            self.free_queue.append(block)
    
    def cache_block(self, block: KVCacheBlock, block_hash: BlockHashWithGroupId) -> None:
        if not self.enable_caching: return
        block.block_hash = block_hash
        self.hash_cache.insert(block_hash, block)
    
    def lookup_cached(self, block_hash: BlockHashWithGroupId) -> Optional[KVCacheBlock]:
        if not self.enable_caching: return None
        block = self.hash_cache.get(block_hash)
        if block is not None:
            self.cache_hits += 1; block.ref_cnt += 1; block.touch(); return block
        self.cache_misses += 1; return None
    
    def _record_eviction(self, block: KVCacheBlock) -> None:
        self.total_evictions += 1
        lifetime = time.time() - block.last_access_time
        self._eviction_events.append({'block_id': block.block_id, 'lifetime_seconds': lifetime, 'access_count': block.access_count, 'timestamp': time.time()})
        if len(self._eviction_events) > 10000: self._eviction_events = self._eviction_events[-5000:]
    
    def get_eviction_events(self) -> List[Dict[str, Any]]:
        events = self._eviction_events; self._eviction_events = []; return events
