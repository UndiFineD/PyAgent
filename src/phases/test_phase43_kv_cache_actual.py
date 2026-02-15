#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Phase 43: KV Cache Coordinator Tests - Actual API

Tests for the actual KVCacheCoordinator implementation API.
"""

import pytest
import time

# Python implementations
from src.infrastructure.engine.kv_cache_coordinator import (
    CacheGroupType,
    AllocationStrategy,
    EvictionPolicy,
    BlockHash,
    BlockHashWithGroupId,
    KVCacheBlock,
    KVCacheBlocks,
    FreeBlockQueue,
    BlockHashCache,
    BlockPool,
    CacheConfig,
    CacheGroupSpec,
    KVCacheCoordinator,
    HierarchicalKVCacheCoordinator,
    PredictiveKVCacheCoordinator,
    AsyncPrefetchCoordinator,
)

# Rust accelerations
try:
    import rust_core
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False


# =============================================================================
# Enum Tests
# =============================================================================

class TestCacheGroupType:
    """Test CacheGroupType enum."""

    def test_enum_values(self):
        """Test all enum values exist."""
        assert CacheGroupType.FULL_ATTENTION is not None
        assert CacheGroupType.SLIDING_WINDOW is not None
        assert CacheGroupType.CROSS_ATTENTION is not None
        assert CacheGroupType.MLA_COMPRESSED is not None
        assert CacheGroupType.CHUNKED_LOCAL is not None

    def test_enum_iteration(self):
        """Test enum is iterable."""
        types = list(CacheGroupType)
        assert len(types) >= 5


class TestAllocationStrategy:
    """Test AllocationStrategy enum."""

    def test_strategies(self):
        """Test allocation strategies."""
        assert AllocationStrategy.GREEDY is not None


class TestEvictionPolicy:
    """Test EvictionPolicy enum."""

    def test_policies(self):
        """Test eviction policies."""
        assert EvictionPolicy.LRU is not None


# =============================================================================
# Dataclass Tests
# =============================================================================

class TestBlockHash:
    """Test BlockHash dataclass."""

    def test_block_hash_creation(self):
        """Test creating a block hash."""
        bh = BlockHash(hash_bytes=b'\x01\x02\x03\x04')
        assert bh.hash_bytes == b'\x01\x02\x03\x04'

    def test_block_hash_equality(self):
        """Test block hash equality."""
        bh1 = BlockHash(hash_bytes=b'\x01\x02\x03\x04')
        bh2 = BlockHash(hash_bytes=b'\x01\x02\x03\x04')
        assert bh1 == bh2

    def test_block_hash_immutable(self):
        """Test block hash is frozen/hashable."""
        bh = BlockHash(hash_bytes=b'\x01\x02')
        assert hash(bh) != 0  # Should be hashable


class TestBlockHashWithGroupId:
    """Test BlockHashWithGroupId dataclass."""

    def test_with_group_id(self):
        """Test block hash with group ID."""
        bh = BlockHash(hash_bytes=b'\x01\x02')
        bhg = BlockHashWithGroupId(block_hash=bh, group_id=1)
        assert bhg.group_id == 1
        assert bhg.block_hash == bh


class TestKVCacheBlock:
    """Test KVCacheBlock dataclass."""

    def test_block_creation(self):
        """Test creating a cache block."""
        block = KVCacheBlock(block_id=42)
        assert block.block_id == 42
        assert block.ref_cnt == 0
        assert block.block_hash is None
        assert block.is_null is False

    def test_block_touch(self):
        """Test touching a block updates access time."""
        block = KVCacheBlock(block_id=1)
        initial_time = block.last_access_time
        time.sleep(0.01)
        block.touch()
        assert block.last_access_time > initial_time
        assert block.access_count > 0

    def test_block_reset(self):
        """Test resetting a block."""
        block = KVCacheBlock(block_id=1)
        block.ref_cnt = 5
        block.access_count = 10
        block.reset()
        assert block.ref_cnt == 0
        assert block.block_hash is None


class TestKVCacheBlocks:
    """Test KVCacheBlocks tuple wrapper."""

    def test_blocks_creation(self):
        """Test creating blocks tuple."""
        block = KVCacheBlock(block_id=0)
        blocks = KVCacheBlocks(blocks=([block],))
        assert len(blocks.blocks) == 1


# =============================================================================
# FreeBlockQueue Tests
# =============================================================================

class TestFreeBlockQueue:
    """Test FreeBlockQueue O(1) operations."""

    def test_init_with_blocks(self):
        """Test initialization with blocks."""
        blocks = [KVCacheBlock(block_id=i) for i in range(5)]
        queue = FreeBlockQueue(blocks)
        assert queue.num_free_blocks == 5

    def test_pop_front(self):
        """Test popping from front."""
        blocks = [KVCacheBlock(block_id=i) for i in range(3)]
        queue = FreeBlockQueue(blocks)

        block = queue.pop_front()
        assert block is not None
        assert block.block_id == 0
        assert queue.num_free_blocks == 2

    def test_append(self):
        """Test appending blocks."""
        queue = FreeBlockQueue([])
        block = KVCacheBlock(block_id=99)
        queue.append(block)
        assert queue.num_free_blocks == 1

    def test_remove(self):
        """Test removing specific block."""
        blocks = [KVCacheBlock(block_id=i) for i in range(3)]
        queue = FreeBlockQueue(blocks)

        queue.remove(blocks[1])
        assert queue.num_free_blocks == 2

    def test_empty_pop(self):
        """Test popping from empty queue."""
        queue = FreeBlockQueue([])
        block = queue.pop_front()
        assert block is None


# =============================================================================
# BlockHashCache Tests
# =============================================================================

class TestBlockHashCache:
    """Test BlockHashCache for prefix caching."""

    def test_insert_and_get(self):
        """Test inserting and getting block hashes."""
        cache = BlockHashCache()
        bh = BlockHash(hash_bytes=b'\x01\x02\x03\x04')
        bhg = BlockHashWithGroupId(block_hash=bh, group_id=0)
        block = KVCacheBlock(block_id=42)

        cache.insert(bhg, block)
        result = cache.get(bhg)
        assert result is not None
        assert result.block_id == 42

    def test_missing_key(self):
        """Test missing key returns None."""
        cache = BlockHashCache()
        bh = BlockHash(hash_bytes=b'\xff\xff')
        bhg = BlockHashWithGroupId(block_hash=bh, group_id=0)
        assert cache.get(bhg) is None

    def test_remove(self):
        """Test removing from cache."""
        cache = BlockHashCache()
        bh = BlockHash(hash_bytes=b'\x01\x02')
        bhg = BlockHashWithGroupId(block_hash=bh, group_id=0)
        block = KVCacheBlock(block_id=1)

        cache.insert(bhg, block)
        cache.remove(bhg, block.block_id)
        # After removal, the block should not be cached
        assert cache.get(bhg) is None


# =============================================================================
# BlockPool Tests
# =============================================================================

class TestBlockPool:
    """Test BlockPool allocation."""

    def test_creation(self):
        """Test creating a block pool."""
        pool = BlockPool(num_blocks=100)
        assert pool is not None

    def test_allocate_blocks(self):
        """Test allocating blocks."""
        pool = BlockPool(num_blocks=10)
        blocks = pool.allocate(3)
        assert len(blocks) == 3

    def test_free_blocks(self):
        """Test freeing blocks."""
        pool = BlockPool(num_blocks=10)
        blocks = pool.allocate(3)
        for block in blocks:
            pool.free(block)


# =============================================================================
# CacheConfig and CacheGroupSpec Tests
# =============================================================================

class TestCacheGroupSpec:
    """Test CacheGroupSpec configuration."""

    def test_full_attention_spec(self):
        """Test full attention group spec."""
        spec = CacheGroupSpec(
            group_id=0,
            group_type=CacheGroupType.FULL_ATTENTION,
            block_size=16,
            num_kv_heads=32,
            head_dim=128,
        )
        assert spec.group_id == 0
        assert spec.group_type == CacheGroupType.FULL_ATTENTION
        assert spec.block_size == 16

    def test_sliding_window_spec(self):
        """Test sliding window group spec."""
        spec = CacheGroupSpec(
            group_id=1,
            group_type=CacheGroupType.SLIDING_WINDOW,
            block_size=16,
            num_kv_heads=8,
            head_dim=128,
            sliding_window=4096,
        )
        assert spec.sliding_window == 4096


class TestCacheConfig:
    """Test CacheConfig."""

    def test_basic_config(self):
        """Test basic cache configuration."""
        spec = CacheGroupSpec(
            group_id=0,
            group_type=CacheGroupType.FULL_ATTENTION,
            block_size=16,
            num_kv_heads=32,
            head_dim=128,
        )
        config = CacheConfig(
            num_blocks=1000,
            block_size=16,
            groups=[spec],
        )
        assert config.num_blocks == 1000
        assert config.block_size == 16
        assert len(config.groups) == 1
        assert config.enable_prefix_caching is True


# =============================================================================
# KVCacheCoordinator Tests
# =============================================================================

class TestKVCacheCoordinator:
    """Test KVCacheCoordinator main class."""

    @pytest.fixture
    def basic_config(self):
        """Create a basic cache config."""
        spec = CacheGroupSpec(
            group_id=0,
            group_type=CacheGroupType.FULL_ATTENTION,
            block_size=16,
            num_kv_heads=32,
            head_dim=128,
        )
        return CacheConfig(
            num_blocks=100,
            block_size=16,
            groups=[spec],
        )

    def test_initialization(self, basic_config):
        """Test coordinator initialization."""
        coord = KVCacheCoordinator(
            config=basic_config,
            max_model_len=2048,
        )
        assert coord is not None

    def test_allocate(self, basic_config):
        """Test allocation."""
        coord = KVCacheCoordinator(
            config=basic_config,
            max_model_len=2048,
        )
        # allocate takes request_id, num_tokens, num_encoder_tokens
        blocks = coord.allocate(request_id="req_001", num_tokens=80)
        assert blocks is not None

    def test_free(self, basic_config):
        """Test freeing allocated blocks."""
        coord = KVCacheCoordinator(
            config=basic_config,
            max_model_len=2048,
        )
        coord.allocate(request_id="req_001", num_tokens=80)
        coord.free(request_id="req_001")

    def test_get_stats(self, basic_config):
        """Test getting cache statistics."""
        coord = KVCacheCoordinator(
            config=basic_config,
            max_model_len=2048,
        )
        stats = coord.get_stats()
        assert isinstance(stats, dict)


# =============================================================================
# Advanced Coordinator Tests
# =============================================================================

class TestHierarchicalKVCacheCoordinator:
    """Test HierarchicalKVCacheCoordinator."""

    @pytest.fixture
    def config(self):
        """Create config."""
        spec = CacheGroupSpec(
            group_id=0,
            group_type=CacheGroupType.FULL_ATTENTION,
            block_size=16,
            num_kv_heads=32,
            head_dim=128,
        )
        return CacheConfig(
            num_blocks=100,
            block_size=16,
            groups=[spec],
        )

    def test_init(self, config):
        """Test hierarchical coordinator initialization."""
        coord = HierarchicalKVCacheCoordinator(
            config=config,
            max_model_len=2048,
            num_layers=32,
        )
        assert coord is not None


class TestPredictiveKVCacheCoordinator:
    """Test PredictiveKVCacheCoordinator."""

    @pytest.fixture
    def config(self):
        """Create config."""
        spec = CacheGroupSpec(
            group_id=0,
            group_type=CacheGroupType.FULL_ATTENTION,
            block_size=16,
            num_kv_heads=32,
            head_dim=128,
        )
        return CacheConfig(
            num_blocks=100,
            block_size=16,
            groups=[spec],
        )

    def test_init(self, config):
        """Test predictive coordinator initialization."""
        coord = PredictiveKVCacheCoordinator(
            config=config,
            max_model_len=2048,
            memory_budget_bytes=1024 * 1024 * 1024,
        )
        assert coord is not None


class TestAsyncPrefetchCoordinator:
    """Test AsyncPrefetchCoordinator."""

    @pytest.fixture
    def config(self):
        """Create config."""
        spec = CacheGroupSpec(
            group_id=0,
            group_type=CacheGroupType.FULL_ATTENTION,
            block_size=16,
            num_kv_heads=32,
            head_dim=128,
        )
        return CacheConfig(
            num_blocks=100,
            block_size=16,
            groups=[spec],
        )

    def test_init(self, config):
        """Test async prefetch coordinator initialization."""
        coord = AsyncPrefetchCoordinator(
            config=config,
            max_model_len=2048,
            prefetch_queue_size=50,
        )
        assert coord is not None


# =============================================================================
# Rust Acceleration Integration Tests
# =============================================================================

@pytest.mark.skipif(not RUST_AVAILABLE, reason="Rust module not available")
class TestRustIntegration:
    """Test Rust acceleration integration."""

    def test_block_hashes_batched(self):
        """Test compute_block_hashes_batched_rust."""
        tokens = list(range(64))
        hashes = rust_core.compute_block_hashes_batched_rust(tokens, 16, 42)
        assert len(hashes) == 4  # 64 tokens / 16 block size

    def test_calculate_blocks_needed(self):
        """Test calculate_blocks_needed_rust."""
        num_blocks = rust_core.calculate_blocks_needed_rust(100, 16, 0)
        assert num_blocks == 7  # ceil(100/16)

    def test_find_prefix_match(self):
        """Test find_prefix_match_rust."""
        # This tests the Rust prefix matching function
        cached_hashes = [1, 2, 3, 4, 5]
        query_hashes = [1, 2, 3]

        match_len = rust_core.find_prefix_match_rust(cached_hashes, query_hashes)
        assert match_len == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
