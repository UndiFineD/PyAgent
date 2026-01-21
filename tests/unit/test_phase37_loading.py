"""
Phase 37: Weight Loading, KV Offload & Expert Load Balancing Tests

Tests for:
- WeightLoader.py: Multi-threaded weight loading, atomic writing
- ShardedStateLoader.py: Sharded checkpoint loading
- KVOffloadManager.py: LRU/ARC offloading, tiered storage
- ExpertLoadBalancer.py: EPLB policies and rebalancing
- Rust accelerations: 9 new functions
"""

import os
import sys
import tempfile
import threading
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Try import Rust module
try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


# =============================================================================
# WeightLoader Tests
# =============================================================================

class TestWeightLoader:
    """Tests for WeightLoader module."""
    
    def test_weight_format_enum(self):
        """Test WeightFormat enum values."""
        from src.infrastructure.engine.loading.weight_loader import WeightFormat
        
        assert WeightFormat.SAFETENSORS.value > 0
        assert WeightFormat.PYTORCH.value > 0
        assert WeightFormat.NUMPY.value > 0
        assert WeightFormat.GGUF.value > 0
        assert WeightFormat.UNKNOWN.value > 0
    
    def test_weight_spec_creation(self):
        """Test WeightSpec dataclass."""
        from src.infrastructure.engine.loading.weight_loader import WeightSpec
        
        spec = WeightSpec(
            name="model.layer.weight",
            shape=(512, 768),
            dtype="float32",
            file_path="/path/to/weights.safetensors",
        )
        
        assert spec.name == "model.layer.weight"
        assert spec.shape == (512, 768)
        assert spec.numel == 512 * 768
        assert hash(spec) is not None  # Hashable
    
    def test_load_stats(self):
        """Test LoadStats dataclass."""
        from src.infrastructure.engine.loading.weight_loader import LoadStats
        
        stats = LoadStats(
            total_bytes=1024 * 1024 * 1024,  # 1GB
            load_time_seconds=2.0,
        )
        
        # 1GB / 1e9 / 2s = ~0.537 GB/s (1GB in bytes = 1073741824)
        assert abs(stats.throughput_gbps - 0.537) < 0.01
        
        # Zero time edge case
        zero_stats = LoadStats(total_bytes=1000, load_time_seconds=0.0)
        assert zero_stats.throughput_gbps == 0.0
    
    def test_atomic_writer(self):
        """Test AtomicWriter context manager."""
        from src.infrastructure.engine.loading.weight_loader import AtomicWriter
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_atomic.txt"
            
            # Successful write
            writer = AtomicWriter(filepath, mode="wb")
            with writer as f:
                f.write(b"test content")
            
            assert filepath.exists()
            assert filepath.read_bytes() == b"test content"
    
    def test_atomic_writer_failure(self):
        """Test AtomicWriter rollback on failure."""
        from src.infrastructure.engine.loading.weight_loader import AtomicWriter
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_atomic_fail.txt"
            
            # Write initial content
            filepath.write_text("original")
            
            # Failed write should not corrupt original
            try:
                writer = AtomicWriter(filepath, mode="wb")
                with writer as f:
                    f.write(b"new content")
                    raise ValueError("Simulated failure")
            except ValueError:
                pass
            
            # Original should be preserved
            assert filepath.read_text() == "original"
    
    def test_detect_weight_format(self):
        """Test weight format detection."""
        from src.infrastructure.engine.loading.weight_loader import detect_weight_format, WeightFormat
        
        assert detect_weight_format("model.safetensors") == WeightFormat.SAFETENSORS
        assert detect_weight_format("model.bin") == WeightFormat.PYTORCH
        assert detect_weight_format("model.pt") == WeightFormat.PYTORCH
        assert detect_weight_format("model.npy") == WeightFormat.NUMPY
        assert detect_weight_format("model.gguf") == WeightFormat.GGUF
        assert detect_weight_format("model.unknown") == WeightFormat.UNKNOWN
    
    def test_filter_shared_tensors(self):
        """Test shared tensor filtering."""
        from src.infrastructure.engine.loading.weight_loader import filter_shared_tensors
        
        # Create mock tensors
        class MockTensor:
            def __init__(self, ptr):
                self._ptr = ptr
            def data_ptr(self):
                return self._ptr
        
        tensors = {
            "a": MockTensor(100),
            "b": MockTensor(100),  # Same storage
            "c": MockTensor(200),  # Different storage
        }
        
        result = filter_shared_tensors(tensors)
        
        # Should keep one of a/b and c
        assert "c" in result
        assert len(result) == 2
    
    def test_multi_thread_loader_worker_count(self):
        """Test adaptive worker count."""
        from src.infrastructure.engine.loading.weight_loader import MultiThreadWeightLoader
        
        loader = MultiThreadWeightLoader(
            max_workers=8,
            adaptive_workers=True,
            min_file_size_per_worker=10 * 1024 * 1024,  # 10MB
        )
        
        # Empty files should use minimal workers
        optimal = loader._get_optimal_workers([])
        assert optimal >= 1
    
    def test_streaming_loader_priority(self):
        """Test StreamingWeightLoader priority handling."""
        from src.infrastructure.engine.loading.weight_loader import StreamingWeightLoader
        
        loader = StreamingWeightLoader(
            memory_budget_mb=512.0,
            priority_weights={"embed", "lm_head"},
        )
        
        # Priority detection
        assert loader._should_prefetch("embed_tokens")
        assert loader._should_prefetch("lm_head")
        assert loader._should_prefetch("attention.query")


# =============================================================================
# ShardedStateLoader Tests
# =============================================================================

class TestShardedStateLoader:
    """Tests for ShardedStateLoader module."""
    
    def test_shard_pattern_default(self):
        """Test default shard pattern."""
        from src.infrastructure.engine.loading.sharded_state_loader import ShardPattern
        
        pattern = ShardPattern()
        
        assert pattern.format_for_rank(0) == "model-rank-0-part-*.safetensors"
        assert pattern.format_for_rank(3, "0") == "model-rank-3-part-0.safetensors"
    
    def test_shard_pattern_parse(self):
        """Test shard filename parsing."""
        from src.infrastructure.engine.loading.sharded_state_loader import ShardPattern
        
        pattern = ShardPattern()
        
        result = pattern.parse_filename("model-rank-2-part-1.safetensors")
        assert result == (2, 1)
        
        result = pattern.parse_filename("invalid.safetensors")
        assert result is None
    
    def test_sharded_tensor_local_shape(self):
        """Test ShardedTensor local shape calculation."""
        from src.infrastructure.engine.loading.sharded_state_loader import ShardedTensor
        
        tensor = ShardedTensor(
            name="weight",
            shape=(1024, 768),
            dtype="float32",
            shard_dim=0,
            num_shards=4,
            local_shard_index=1,
        )
        
        assert tensor.local_shape == (256, 768)
    
    def test_subtensor_filter(self):
        """Test SubtensorFilter for shared storage."""
        from src.infrastructure.engine.loading.sharded_state_loader import SubtensorFilter
        
        # Basic filter test (without actual torch tensors)
        filter_obj = SubtensorFilter()
        
        # Should handle empty dict
        result = filter_obj.filter_subtensors({})
        assert result == {}
    
    def test_sharded_state_loader_init(self):
        """Test ShardedStateLoader initialization."""
        from src.infrastructure.engine.loading.sharded_state_loader import (
            ShardedStateLoader, ShardPattern
        )
        
        loader = ShardedStateLoader(
            pattern=ShardPattern(),
            rank=2,
            world_size=8,
        )
        
        assert loader.rank == 2
        assert loader.world_size == 8
    
    def test_incremental_loader_eviction(self):
        """Test IncrementalShardLoader cache eviction."""
        from src.infrastructure.engine.loading.sharded_state_loader import (
            ShardedStateLoader, IncrementalShardLoader
        )
        
        base_loader = ShardedStateLoader(rank=0)
        loader = IncrementalShardLoader(
            base_loader,
            cache_size=2,
        )
        
        # Simulate cache operations
        loader._cache["shard1"] = {"weight": "data1"}
        loader._cache_order.append("shard1")
        
        loader._cache["shard2"] = {"weight": "data2"}
        loader._cache_order.append("shard2")
        
        # Adding third should evict first
        loader._evict_if_needed()
        
        assert len(loader._cache) == 1
        assert "shard1" not in loader._cache
    
    def test_async_shard_loader(self):
        """Test AsyncShardLoader initialization."""
        from src.infrastructure.engine.loading.sharded_state_loader import (
            ShardedStateLoader, AsyncShardLoader
        )
        
        base_loader = ShardedStateLoader(rank=0)
        async_loader = AsyncShardLoader(
            base_loader,
            prefetch_count=3,
            max_workers=2,
        )
        
        assert async_loader.prefetch_count == 3
        assert async_loader.max_workers == 2


# =============================================================================
# KVOffloadManager Tests
# =============================================================================

class TestKVOffloadManager:
    """Tests for KVOffloadManager module."""
    
    def test_offload_medium_enum(self):
        """Test OffloadMedium enum."""
        from src.infrastructure.engine.loading.kv_offload_manager import OffloadMedium
        
        assert OffloadMedium.GPU.value > 0
        assert OffloadMedium.CPU.value > 0
        assert OffloadMedium.NVME.value > 0
        assert OffloadMedium.REMOTE.value > 0
    
    def test_block_status(self):
        """Test BlockStatus dataclass."""
        from src.infrastructure.engine.loading.kv_offload_manager import BlockStatus
        
        block = BlockStatus(
            address=1000,
            size=4096,
            ref_cnt=1,
            is_ready=True,
        )
        
        assert block.is_pinned  # ref_cnt > 0
        
        block.ref_cnt = 0
        assert not block.is_pinned
    
    def test_load_store_spec(self):
        """Test LoadStoreSpec dataclass."""
        from src.infrastructure.engine.loading.kv_offload_manager import (
            LoadStoreSpec, OffloadMedium
        )
        
        spec = LoadStoreSpec(
            block_hashes=["hash1", "hash2", "hash3"],
            medium=OffloadMedium.CPU,
            addresses=[100, 200, 300],
        )
        
        assert spec.num_blocks == 3
    
    def test_memory_backend(self):
        """Test MemoryBackend operations."""
        from src.infrastructure.engine.loading.kv_offload_manager import MemoryBackend
        
        backend = MemoryBackend(
            capacity_blocks=10,
            block_size=4096,
            medium="cpu",
        )
        
        assert backend.medium == "cpu"
        assert backend.block_size == 4096
        assert backend.get_num_free_blocks() == 10
        
        # Allocate blocks
        blocks = backend.allocate_blocks(["h1", "h2"])
        assert len(blocks) == 2
        assert backend.get_num_free_blocks() == 8
        
        # Free a block
        backend.free(blocks[0])
        assert backend.get_num_free_blocks() == 9
    
    def test_lru_manager_lookup(self):
        """Test LRUOffloadingManager lookup."""
        from src.infrastructure.engine.loading.kv_offload_manager import (
            LRUOffloadingManager, MemoryBackend, BlockStatus
        )
        
        backend = MemoryBackend(10, 4096)
        manager = LRUOffloadingManager(backend, enable_events=True)
        
        # Empty lookup
        assert manager.lookup(["h1", "h2"]) == 0
        
        # Add ready block
        manager.blocks["h1"] = BlockStatus(address=100, size=4096, is_ready=True)
        assert manager.lookup(["h1", "h2"]) == 1
        
        # Add another ready block
        manager.blocks["h2"] = BlockStatus(address=200, size=4096, is_ready=True)
        assert manager.lookup(["h1", "h2"]) == 2
    
    def test_lru_manager_touch(self):
        """Test LRUOffloadingManager touch (LRU update)."""
        from src.infrastructure.engine.loading.kv_offload_manager import (
            LRUOffloadingManager, MemoryBackend, BlockStatus
        )
        
        backend = MemoryBackend(10, 4096)
        manager = LRUOffloadingManager(backend)
        
        # Add blocks
        manager.blocks["h1"] = BlockStatus(address=100, size=4096, is_ready=True)
        manager.blocks["h2"] = BlockStatus(address=200, size=4096, is_ready=True)
        
        # Touch h1 - should move to end
        manager.touch(["h1"])
        
        keys = list(manager.blocks.keys())
        assert keys[-1] == "h1"
    
    def test_lru_manager_prepare_store(self):
        """Test LRUOffloadingManager prepare_store with eviction."""
        from src.infrastructure.engine.loading.kv_offload_manager import (
            LRUOffloadingManager, MemoryBackend, BlockStatus
        )
        
        backend = MemoryBackend(2, 4096)  # Only 2 blocks
        manager = LRUOffloadingManager(backend, enable_events=True)
        
        # Store 2 blocks
        result = manager.prepare_store(["h1", "h2"])
        assert result is not None
        assert len(result.block_hashes_to_store) == 2
        manager.complete_store(["h1", "h2"], success=True)
        
        # Store another should evict
        result = manager.prepare_store(["h3"])
        assert result is not None
        assert len(result.block_hashes_evicted) == 1
    
    def test_arc_manager_lookup(self):
        """Test ARCOffloadingManager lookup in T1/T2."""
        from src.infrastructure.engine.loading.kv_offload_manager import (
            ARCOffloadingManager, MemoryBackend, BlockStatus
        )
        
        backend = MemoryBackend(10, 4096)
        manager = ARCOffloadingManager(backend)
        
        # Add to T1
        manager.t1["h1"] = BlockStatus(address=100, size=4096, is_ready=True)
        assert manager.lookup(["h1"]) == 1
        
        # Add to T2
        manager.t2["h2"] = BlockStatus(address=200, size=4096, is_ready=True)
        assert manager.lookup(["h1", "h2"]) == 2
    
    def test_arc_manager_touch_promotion(self):
        """Test ARCOffloadingManager touch promotes T1→T2."""
        from src.infrastructure.engine.loading.kv_offload_manager import (
            ARCOffloadingManager, MemoryBackend, BlockStatus
        )
        
        backend = MemoryBackend(10, 4096)
        manager = ARCOffloadingManager(backend)
        
        # Add to T1
        manager.t1["h1"] = BlockStatus(address=100, size=4096, is_ready=True)
        
        # Touch should promote to T2
        manager.touch(["h1"])
        
        assert "h1" not in manager.t1
        assert "h1" in manager.t2
    
    def test_arc_manager_ghost_list(self):
        """Test ARCOffloadingManager ghost list adaptation."""
        from src.infrastructure.engine.loading.kv_offload_manager import (
            ARCOffloadingManager, MemoryBackend
        )
        
        backend = MemoryBackend(10, 4096)
        manager = ARCOffloadingManager(backend)
        
        initial_target = manager.target_t1_size
        
        # Add to B1 ghost list
        manager.b1["ghost1"] = None
        
        # Touch should increase target
        manager.touch(["ghost1"])
        
        assert manager.target_t1_size > initial_target
    
    def test_arc_manager_stats(self):
        """Test ARCOffloadingManager stats property."""
        from src.infrastructure.engine.loading.kv_offload_manager import (
            ARCOffloadingManager, MemoryBackend, BlockStatus
        )
        
        backend = MemoryBackend(10, 4096)
        manager = ARCOffloadingManager(backend)
        
        manager.t1["h1"] = BlockStatus(address=100, size=4096, is_ready=True)
        manager.t2["h2"] = BlockStatus(address=200, size=4096, is_ready=True)
        manager.b1["g1"] = None
        
        stats = manager.stats
        
        assert stats["t1_size"] == 1
        assert stats["t2_size"] == 1
        assert stats["b1_size"] == 1
        assert stats["cache_capacity"] == 10
    
    def test_tiered_manager(self):
        """Test TieredOffloadManager with multiple backends."""
        from src.infrastructure.engine.loading.kv_offload_manager import (
            TieredOffloadManager, MemoryBackend
        )
        
        # Two tiers: fast (2 blocks) and slow (10 blocks)
        fast_backend = MemoryBackend(2, 4096, medium="gpu")
        slow_backend = MemoryBackend(10, 4096, medium="cpu")
        
        manager = TieredOffloadManager([fast_backend, slow_backend])
        
        # Store blocks - should go to fast tier first
        result = manager.prepare_store(["h1", "h2"])
        assert result is not None
        manager.complete_store(["h1", "h2"], success=True)
        
        # Check tier assignment
        assert manager._get_tier("h1") == 0
        assert manager._get_tier("h2") == 0


# =============================================================================
# ExpertLoadBalancer Tests
# =============================================================================

class TestExpertLoadBalancer:
    """Tests for ExpertLoadBalancer module."""
    
    def test_expert_type_enum(self):
        """Test ExpertType enum."""
        from src.infrastructure.engine.loading.expert_load_balancer import ExpertType
        
        assert ExpertType.LOGICAL.value > 0
        assert ExpertType.PHYSICAL.value > 0
        assert ExpertType.REDUNDANT.value > 0
    
    def test_eplb_metrics(self):
        """Test EplbMetrics dataclass."""
        from src.infrastructure.engine.loading.expert_load_balancer import EplbMetrics
        
        metrics = EplbMetrics(
            physical_to_logical=[[0, 1, 2, 0], [0, 1, 2, 1]],
            logical_replica_count=[[2, 1, 1], [1, 2, 1]],
        )
        
        assert metrics.num_layers == 2
        assert metrics.num_physical_experts == 4
        assert metrics.num_logical_experts == 3
    
    def test_expert_mapping(self):
        """Test ExpertMapping class."""
        from src.infrastructure.engine.loading.expert_load_balancer import ExpertMapping
        
        mapping = ExpertMapping(
            phy_to_log=[[0, 1, 2, 0]],
            log_to_phy=[[[0, 3], [1, -1], [2, -1]]],
            replica_count=[[2, 1, 1]],
        )
        
        assert mapping.get_logical_expert(0, 0) == 0
        assert mapping.get_logical_expert(0, 3) == 0
        assert mapping.get_physical_experts(0, 0) == [0, 3]
        assert mapping.get_physical_experts(0, 1) == [1]
    
    def test_default_policy_balanced_packing(self):
        """Test DefaultEplbPolicy balanced packing."""
        pytest.importorskip("numpy")
        from src.infrastructure.engine.loading.expert_load_balancer import DefaultEplbPolicy
        
        weights = [[10.0, 5.0, 8.0, 3.0]]  # 4 groups, pack into 2
        
        pack_index, rank_in_pack = DefaultEplbPolicy.balanced_packing(
            weights, num_packs=2
        )
        
        assert len(pack_index[0]) == 4
        # Each pack should have 2 groups
        pack_counts = {}
        for p in pack_index[0]:
            pack_counts[p] = pack_counts.get(p, 0) + 1
        assert all(c == 2 for c in pack_counts.values())
    
    def test_default_policy_replicate_experts(self):
        """Test DefaultEplbPolicy expert replication."""
        pytest.importorskip("numpy")
        from src.infrastructure.engine.loading.expert_load_balancer import DefaultEplbPolicy
        
        weights = [[10.0, 5.0, 3.0]]  # 3 logical experts
        
        phy_to_log, rank, log_count = DefaultEplbPolicy.replicate_experts(
            weights, num_physical=5  # 2 redundant
        )
        
        assert len(phy_to_log[0]) == 5
        # Most loaded expert (10.0) should get replicas
        assert log_count[0][0] >= 2  # Expert 0 has highest load
    
    def test_default_policy_rebalance(self):
        """Test DefaultEplbPolicy full rebalancing."""
        pytest.importorskip("numpy")
        from src.infrastructure.engine.loading.expert_load_balancer import DefaultEplbPolicy
        
        weights = [[10.0, 5.0, 3.0, 2.0]]
        
        mapping = DefaultEplbPolicy.rebalance_experts(
            weight=weights,
            num_replicas=6,
            num_groups=4,
            num_nodes=1,
            num_ranks=1,
        )
        
        assert len(mapping.phy_to_log[0]) == 6
        assert len(mapping.replica_count[0]) == 4
    
    def test_locality_aware_policy(self):
        """Test LocalityAwarePolicy."""
        pytest.importorskip("numpy")
        from src.infrastructure.engine.loading.expert_load_balancer import LocalityAwarePolicy
        
        weights = [[10.0, 5.0, 3.0, 2.0]]
        
        mapping = LocalityAwarePolicy.rebalance_experts(
            weight=weights,
            num_replicas=8,
            num_groups=4,
            num_nodes=2,
            num_ranks=4,
        )
        
        assert len(mapping.phy_to_log[0]) == 8
    
    def test_expert_load_balancer_record_load(self):
        """Test ExpertLoadBalancer load recording."""
        from src.infrastructure.engine.loading.expert_load_balancer import ExpertLoadBalancer
        
        balancer = ExpertLoadBalancer(
            num_layers=2,
            num_logical_experts=4,
            num_physical_experts=6,
            window_size=10,
        )
        
        balancer.record_load(0, [1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        
        assert balancer.metrics.expert_load_pass[0][0] == 1.0
        assert balancer.metrics.expert_load_pass[0][5] == 6.0
    
    def test_expert_load_balancer_average(self):
        """Test ExpertLoadBalancer average load calculation."""
        from src.infrastructure.engine.loading.expert_load_balancer import ExpertLoadBalancer
        
        balancer = ExpertLoadBalancer(
            num_layers=1,
            num_logical_experts=2,
            num_physical_experts=2,
            window_size=2,
        )
        
        balancer.record_load(0, [10.0, 20.0])
        balancer.advance_window()
        balancer.record_load(0, [30.0, 40.0])
        
        avg = balancer.get_average_load()
        
        # Average of [10, 30] and [20, 40]
        assert avg[0][0] == 20.0
        assert avg[0][1] == 30.0
    
    def test_expert_load_balancer_rebalance(self):
        """Test ExpertLoadBalancer rebalancing."""
        pytest.importorskip("numpy")
        from src.infrastructure.engine.loading.expert_load_balancer import ExpertLoadBalancer
        
        balancer = ExpertLoadBalancer(
            num_layers=1,
            num_logical_experts=4,
            num_physical_experts=6,
        )
        
        # Provide explicit weights
        import numpy as np
        weights = np.array([[10.0, 5.0, 3.0, 2.0]])
        
        mapping = balancer.rebalance(weight=weights)
        
        assert mapping is not None
        assert balancer.mapping is not None
        assert len(mapping.phy_to_log[0]) == 6
    
    def test_async_rebalancer_should_rebalance(self):
        """Test AsyncExpertRebalancer threshold check."""
        from src.infrastructure.engine.loading.expert_load_balancer import (
            ExpertLoadBalancer, AsyncExpertRebalancer
        )
        
        balancer = ExpertLoadBalancer(
            num_layers=1,
            num_logical_experts=2,
            num_physical_experts=2,
            window_size=1,
        )
        
        async_rebal = AsyncExpertRebalancer(
            balancer,
            rebalance_interval=0.0,  # No time limit
            load_threshold=2.0,
        )
        
        # Balanced load
        balancer.record_load(0, [10.0, 10.0])
        assert not async_rebal._should_rebalance()
        
        # Imbalanced load
        balancer.record_load(0, [100.0, 10.0])
        assert async_rebal._should_rebalance()


# =============================================================================
# Rust Function Tests
# =============================================================================

class TestRustPhase37Functions:
    """Tests for Phase 37 Rust accelerations."""
    
    @pytest.mark.skipif(not HAS_RUST, reason="Rust module not available")
    def test_weight_hash_compute(self):
        """Test weight_hash_compute_rust."""
        data = b"test weight data for hashing"
        hash1 = rust_core.weight_hash_compute_rust(list(data))
        
        # Same data should produce same hash
        hash2 = rust_core.weight_hash_compute_rust(list(data))
        assert hash1 == hash2
        
        # Different data should produce different hash
        hash3 = rust_core.weight_hash_compute_rust(list(b"different data"))
        assert hash1 != hash3
    
    @pytest.mark.skipif(not HAS_RUST, reason="Rust module not available")
    def test_validate_weight_shapes(self):
        """Test validate_weight_shapes_rust."""
        specs = [
            {"name": "layer1.weight", "shape": "(512, 768)"},
            {"name": "layer2.weight", "shape": "(768, 768)"},
        ]
        expected = [
            {"name": "layer1.weight", "shape": "(512, 768)"},
            {"name": "layer2.weight", "shape": "(768, 768)"},
            {"name": "layer3.weight", "shape": "(768, 1024)"},  # Missing
        ]
        
        errors = rust_core.validate_weight_shapes_rust(specs, expected)
        
        assert len(errors) == 1
        assert "layer3.weight" in errors[0]
    
    @pytest.mark.skipif(not HAS_RUST, reason="Rust module not available")
    def test_compute_shard_assignment(self):
        """Test compute_shard_assignment_rust."""
        param_sizes = [1000, 500, 800, 200, 600]
        
        assignments = rust_core.compute_shard_assignment_rust(
            5, 2, param_sizes
        )
        
        assert len(assignments) == 5
        # Each rank should get ~equal total size
        rank_totals = [0, 0]
        for i, rank in enumerate(assignments):
            rank_totals[rank] += param_sizes[i]
        
        # Should be reasonably balanced
        assert max(rank_totals) / min(rank_totals) < 1.5
    
    @pytest.mark.skipif(not HAS_RUST, reason="Rust module not available")
    def test_validate_shard_shapes(self):
        """Test validate_shard_shapes_rust."""
        specs = [
            {"name": "layer1", "num_shards": "4"},
            {"name": "layer2", "num_shards": "2"},  # Wrong
        ]
        
        errors = rust_core.validate_shard_shapes_rust(specs, 0, 4)
        
        assert len(errors) == 1
        assert "layer2" in errors[0]
    
    @pytest.mark.skipif(not HAS_RUST, reason="Rust module not available")
    def test_compute_lru_eviction(self):
        """Test compute_lru_eviction_rust."""
        blocks = [
            {"ref_cnt": 1},  # Pinned
            {"ref_cnt": 0},  # Evictable
            {"ref_cnt": 0},  # Evictable
            {"ref_cnt": 2},  # Pinned
            {"ref_cnt": 0},  # Evictable
        ]
        
        to_evict = rust_core.compute_lru_eviction_rust(blocks, 2)
        
        assert len(to_evict) == 2
        assert 0 not in to_evict  # Pinned
        assert 3 not in to_evict  # Pinned
    
    @pytest.mark.skipif(not HAS_RUST, reason="Rust module not available")
    def test_compute_arc_target(self):
        """Test compute_arc_target_rust."""
        # B1 hit should increase target
        new_target = rust_core.compute_arc_target_rust(
            t1_size=5,
            t2_size=5,
            b1_size=3,
            b2_size=6,
            current_target=5.0,
            hit_in_b1=True,
            capacity=10,
        )
        
        assert new_target > 5.0
        
        # B2 hit should decrease target
        new_target = rust_core.compute_arc_target_rust(
            t1_size=5,
            t2_size=5,
            b1_size=6,
            b2_size=3,
            current_target=5.0,
            hit_in_b1=False,
            capacity=10,
        )
        
        assert new_target < 5.0
    
    @pytest.mark.skipif(not HAS_RUST, reason="Rust module not available")
    def test_compute_balanced_packing(self):
        """Test compute_balanced_packing_rust."""
        weights = [[10.0, 5.0, 8.0, 3.0]]  # 4 groups
        
        pack_index, rank_in_pack = rust_core.compute_balanced_packing_rust(
            weights, 2  # 2 packs
        )
        
        assert len(pack_index) == 1
        assert len(pack_index[0]) == 4
        
        # Each pack should have 2 groups
        pack_counts = {}
        for p in pack_index[0]:
            if p >= 0:
                pack_counts[p] = pack_counts.get(p, 0) + 1
        
        assert all(c == 2 for c in pack_counts.values())
    
    @pytest.mark.skipif(not HAS_RUST, reason="Rust module not available")
    def test_compute_expert_replication(self):
        """Test compute_expert_replication_rust."""
        weights = [[10.0, 5.0, 3.0]]  # 3 logical
        
        phy_to_log, rank, log_count = rust_core.compute_expert_replication_rust(
            weights, 5  # 5 physical (2 redundant)
        )
        
        assert len(phy_to_log) == 1
        assert len(phy_to_log[0]) == 5
        
        # Highest load expert should get most replicas
        assert log_count[0][0] >= 2
    
    @pytest.mark.skipif(not HAS_RUST, reason="Rust module not available")
    def test_compute_load_imbalance(self):
        """Test compute_load_imbalance_rust."""
        # Balanced
        loads = [[10.0, 10.0, 10.0]]
        ratio = rust_core.compute_load_imbalance_rust(loads)
        assert ratio == 1.0
        
        # Imbalanced
        loads = [[100.0, 10.0, 10.0]]
        ratio = rust_core.compute_load_imbalance_rust(loads)
        assert ratio == 10.0


# =============================================================================
# Integration Tests
# =============================================================================

class TestPhase37Integration:
    """Integration tests for Phase 37 components."""
    
    def test_weight_loading_pipeline(self):
        """Test weight loading pipeline end-to-end."""
        from src.infrastructure.engine.loading.weight_loader import (
            WeightSpec, LoadStats, detect_weight_format, WeightFormat
        )
        
        # Create specs
        specs = [
            WeightSpec("layer1.weight", (512, 768), "float32", "model.safetensors"),
            WeightSpec("layer2.weight", (768, 768), "float32", "model.safetensors"),
        ]
        
        # Calculate total size
        total_elements = sum(s.numel for s in specs)
        assert total_elements == 512 * 768 + 768 * 768
    
    def test_kv_offload_with_arc(self):
        """Test KV offloading with ARC policy."""
        from src.infrastructure.engine.loading.kv_offload_manager import (
            ARCOffloadingManager, MemoryBackend
        )
        
        backend = MemoryBackend(5, 4096)
        manager = ARCOffloadingManager(backend, enable_events=True)
        
        # Store blocks
        result = manager.prepare_store(["h1", "h2", "h3"])
        assert result is not None
        manager.complete_store(["h1", "h2", "h3"], success=True)
        
        # Lookup
        hits = manager.lookup(["h1", "h2", "h3"])
        assert hits == 3
        
        # Touch to promote T1→T2
        manager.touch(["h1", "h2"])
        
        # h1, h2 should be in T2 now
        assert "h1" in manager.t2
        assert "h2" in manager.t2
    
    def test_expert_rebalancing_flow(self):
        """Test expert rebalancing end-to-end."""
        pytest.importorskip("numpy")
        from src.infrastructure.engine.loading.expert_load_balancer import (
            ExpertLoadBalancer, DefaultEplbPolicy
        )
        import numpy as np
        
        balancer = ExpertLoadBalancer(
            num_layers=2,
            num_logical_experts=8,
            num_physical_experts=10,
            num_ranks=2,
            num_nodes=1,
        )
        
        # Simulate load recording
        for layer in range(2):
            loads = [float(i + 1) for i in range(10)]
            balancer.record_load(layer, loads)
        
        # Rebalance
        weights = np.random.rand(2, 8) * 100
        mapping = balancer.rebalance(weight=weights)
        
        assert mapping is not None
        assert len(mapping.phy_to_log) == 2
        assert len(mapping.replica_count) == 2
    
    @pytest.mark.skipif(not HAS_RUST, reason="Rust module not available")
    def test_rust_integration(self):
        """Test Rust functions work together."""
        # Test weight hash
        data = list(b"model weight data")
        hash1 = rust_core.weight_hash_compute_rust(data)
        assert isinstance(hash1, int)
        
        # Test LRU eviction
        blocks = [{"ref_cnt": 0}, {"ref_cnt": 1}, {"ref_cnt": 0}]
        evict = rust_core.compute_lru_eviction_rust(blocks, 1)
        assert len(evict) == 1
        
        # Test load imbalance
        loads = [[10.0, 20.0, 30.0]]
        ratio = rust_core.compute_load_imbalance_rust(loads)
        assert ratio == 3.0


# =============================================================================
# Module Import Tests
# =============================================================================

class TestModuleImports:
    """Test that all Phase 37 modules import correctly."""
    
    def test_import_weight_loader(self):
        """Test WeightLoader module imports."""
        from src.infrastructure.engine.loading.weight_loader import (
            WeightFormat,
            WeightSpec,
            AtomicWriter,
            WeightLoader,
            MultiThreadWeightLoader,
            StreamingWeightLoader,
        )
        assert WeightFormat is not None
    
    def test_import_sharded_state_loader(self):
        """Test ShardedStateLoader module imports."""
        from src.infrastructure.engine.loading.sharded_state_loader import (
            ShardPattern,
            ShardedTensor,
            SubtensorFilter,
            ShardedStateLoader,
            IncrementalShardLoader,
            AsyncShardLoader,
        )
        assert ShardPattern is not None
    
    def test_import_kv_offload_manager(self):
        """Test KVOffloadManager module imports."""
        from src.infrastructure.engine.loading.kv_offload_manager import (
            OffloadMedium,
            LoadStoreSpec,
            BlockStatus,
            OffloadingEvent,
            MemoryBackend,
            LRUOffloadingManager,
            ARCOffloadingManager,
            TieredOffloadManager,
        )
        assert OffloadMedium is not None
    
    def test_import_expert_load_balancer(self):
        """Test ExpertLoadBalancer module imports."""
        from src.infrastructure.engine.loading.expert_load_balancer import (
            ExpertType,
            EplbMetrics,
            ExpertMapping,
            AbstractEplbPolicy,
            DefaultEplbPolicy,
            LocalityAwarePolicy,
            ExpertLoadBalancer,
            AsyncExpertRebalancer,
        )
        assert ExpertType is not None
    
    def test_import_from_package(self):
        """Test imports from package __init__."""
        from src.infrastructure.engine.loading import (
            WeightFormat,
            ShardPattern,
            OffloadMedium,
            ExpertType,
        )
        assert WeightFormat is not None
        assert ShardPattern is not None
        assert OffloadMedium is not None
        assert ExpertType is not None
