# SPDX-License-Identifier: Apache-2.0
from abc import ABC, abstractmethod
from typing import Dict, List
from .data_classes import CacheGroupSpec, KVCacheBlock
from .structural import BlockPool

class SingleTypeKVCacheManager(ABC):
    """Abstract base for single-type KV cache management."""
    def __init__(self, spec: CacheGroupSpec, block_pool: BlockPool) -> None:
        self.spec = spec
        self.block_pool = block_pool
        self.request_blocks: Dict[str, List[KVCacheBlock]] = {}
    
    @abstractmethod
    def get_num_blocks_needed(self, num_tokens: int) -> int: pass
    
    def allocate(self, request_id: str, num_tokens: int) -> List[KVCacheBlock]:
        num_blocks = self.get_num_blocks_needed(num_tokens)
        current = len(self.request_blocks.get(request_id, []))
        needed = num_blocks - current
        if needed <= 0: return []
        new_blocks = self.block_pool.allocate(needed)
        if request_id not in self.request_blocks: self.request_blocks[request_id] = []
        self.request_blocks[request_id].extend(new_blocks)
        return new_blocks
    
    def free(self, request_id: str) -> None:
        blocks = self.request_blocks.pop(request_id, [])
        for block in blocks: self.block_pool.free(block)
    
    def get_blocks(self, request_id: str) -> List[KVCacheBlock]:
        return self.request_blocks.get(request_id, [])


class FullAttentionManager(SingleTypeKVCacheManager):
    def get_num_blocks_needed(self, num_tokens: int) -> int:
        from math import ceil
        return ceil(num_tokens / self.spec.block_size)


class SlidingWindowManager(SingleTypeKVCacheManager):
    def get_num_blocks_needed(self, num_tokens: int) -> int:
        from math import ceil
        window = self.spec.sliding_window or num_tokens
        effective_tokens = min(num_tokens, window)
        return ceil(effective_tokens / self.spec.block_size)


class CrossAttentionManager(SingleTypeKVCacheManager):
    def get_num_blocks_needed(self, num_tokens: int) -> int:
        from math import ceil
        return ceil(num_tokens / self.spec.block_size)
