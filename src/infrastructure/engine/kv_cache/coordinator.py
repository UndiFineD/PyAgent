# SPDX-License-Identifier: Apache-2.0
from typing import Dict, List, Optional, Any, Tuple
from .enums import CacheGroupType
from .data_classes import CacheConfig, KVCacheBlocks, BlockHash, BlockHashWithGroupId, KVCacheBlock, CacheGroupSpec
from .structural import BlockPool
from .managers import SingleTypeKVCacheManager, FullAttentionManager, SlidingWindowManager, CrossAttentionManager
from .pack_kv import PackKVManager

class KVCacheCoordinator:
    """Coordinates multiple KV cache groups for complex attention patterns."""
    def __init__(self, config: CacheConfig, max_model_len: int) -> None:
        self.config = config
        self.max_model_len = max_model_len
        self.block_pool = BlockPool(num_blocks=config.num_blocks, enable_caching=config.enable_prefix_caching, eviction_policy=config.eviction_policy)
        self.managers: List[SingleTypeKVCacheManager] = []
        for spec in config.groups:
            manager = self._create_manager(spec)
            self.managers.append(manager)
        self._empty_blocks = KVCacheBlocks.empty(len(config.groups))
        self.total_allocations = 0
        self.total_frees = 0
    
    def _create_manager(self, spec: CacheGroupSpec) -> SingleTypeKVCacheManager:
        if spec.group_type == CacheGroupType.FULL_ATTENTION: return FullAttentionManager(spec, self.block_pool)
        elif spec.group_type == CacheGroupType.SLIDING_WINDOW: return SlidingWindowManager(spec, self.block_pool)
        elif spec.group_type == CacheGroupType.CROSS_ATTENTION: return CrossAttentionManager(spec, self.block_pool)
        elif spec.group_type == CacheGroupType.PACKKV_COMPRESSED: return PackKVManager(spec, self.block_pool)
        return FullAttentionManager(spec, self.block_pool)
    
    @property
    def usage(self) -> float: return self.block_pool.usage
    @property
    def num_groups(self) -> int: return len(self.managers)
    
    def get_num_blocks_to_allocate(self, request_id: str, num_tokens: int, num_encoder_tokens: int = 0) -> int:
        total = 0
        for i, manager in enumerate(self.managers):
            spec = self.config.groups[i]
            total += manager.get_num_blocks_needed(num_encoder_tokens if spec.group_type == CacheGroupType.CROSS_ATTENTION else num_tokens)
        return total
    
    def allocate(self, request_id: str, num_tokens: int, num_encoder_tokens: int = 0) -> KVCacheBlocks:
        blocks_per_group = []
        for i, manager in enumerate(self.managers):
            spec = self.config.groups[i]
            blocks = manager.allocate(request_id, num_encoder_tokens if spec.group_type == CacheGroupType.CROSS_ATTENTION else num_tokens)
            blocks_per_group.append(tuple(blocks))
        self.total_allocations += 1
        return KVCacheBlocks(tuple(blocks_per_group))
    
    def free(self, request_id: str) -> None:
        for manager in self.managers: manager.free(request_id)
        self.total_frees += 1
    
    def get_blocks(self, request_id: str) -> KVCacheBlocks:
        blocks_per_group = [tuple(manager.get_blocks(request_id)) for manager in self.managers]
        return KVCacheBlocks(tuple(blocks_per_group))

    def get_compression_metadata(self, request_id: str) -> Dict[int, Dict[str, Any]]:
        """Collect compression metadata from all managers supporting it."""
        metadata = {}
        for manager in self.managers:
            if hasattr(manager, "compression_metadata"):
                # manager.compression_metadata is Dict[int, Dict[str, Any]]
                # where key is block_id
                metadata.update(getattr(manager, "compression_metadata"))
        return metadata
    
    def cache_blocks(self, request_id: str, block_hashes: List[BlockHash], group_id: int = 0) -> None:
        blocks = self.managers[group_id].get_blocks(request_id)
        for block, hash_ in zip(blocks, block_hashes):
            hash_with_group = BlockHashWithGroupId(hash_, group_id)
            self.block_pool.cache_block(block, hash_with_group)
    
    def find_cached_blocks(self, block_hashes: List[BlockHash], group_id: int = 0) -> Tuple[List[KVCacheBlock], int]:
        cached = []
        num_hits = 0
        for hash_ in block_hashes:
            hash_with_group = BlockHashWithGroupId(hash_, group_id)
            block = self.block_pool.lookup_cached(hash_with_group)
            if block is not None:
                cached.append(block); num_hits += 1
            else: break
        return cached, num_hits
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            'usage': self.usage, 'num_groups': self.num_groups, 'total_allocations': self.total_allocations, 'total_frees': self.total_frees,
            'block_pool_stats': {'total_blocks': self.block_pool.num_blocks, 'free_blocks': self.block_pool.num_free_blocks, 'cache_hits': self.block_pool.cache_hits, 'cache_misses': self.block_pool.cache_misses, 'total_evictions': self.block_pool.total_evictions}
        }
