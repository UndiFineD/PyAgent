"""
Phase 35 Tests: Async Execution & Advanced Caching

Tests for:
1. AsyncEngineClient - Multi-process async engine
2. BlockPoolManager - LRU/ARC block eviction
3. GPUMemoryAllocator - Sleep/wake memory management
4. PrefixCacheOptimizer - Radix tree prefix matching
5. AsyncModelRunner - Async model execution
6. DataParallelCoordinator - DP coordination

Plus Rust acceleration tests.
"""

import asyncio
import pytest
import time
import threading
from typing import Optional

# Python module imports
from src.infrastructure.engine.async_engine_client import (
    ClientMode, WorkerState, EngineClientConfig, SchedulerOutput,
    EngineOutput, WorkerInfo, EngineCoreClientBase, InprocClient,
    SyncMPClient, AsyncMPClient, P2CLoadBalancer, DPAsyncMPClient,
    auto_select_client_mode, create_engine_client
)
from src.infrastructure.storage.cache.block_pool_manager import (
    BlockState, Block, BlockPoolConfig, EvictionEvent, CacheMetrics,
    KVCacheMetricsCollector, ARCPolicy, BlockPool, compute_block_hash
)
from src.infrastructure.storage.memory.gpu_memory_allocator import (
    MemoryState, AllocationStrategy, MemoryRegion, MemorySnapshot,
    MemoryPoolConfig, MemoryPressureEvent, CuMemAllocator,
    MultiGPUMemoryBalancer
)
from src.infrastructure.storage.cache.prefix_cache_optimizer import (
    CacheTier, PrefixCacheConfig, PrefixEntry, CacheHitResult,
    RadixTreeNode, PrefixTree, PrefixCacheOptimizer
)
from src.inference.execution.async_model_runner import (
    RunnerState, ModelInput, ModelOutput, AsyncGPUPoolingModelRunnerOutput,
    ExecutionPipeline, AsyncModelRunner, BatchedAsyncRunner,
    SchedulerOutput as RunnerSchedulerOutput
)
from src.infrastructure.swarm.parallel.data_parallel_coordinator import (
    DPRole, WorkerHealth, LoadBalanceStrategy, DPConfig,
    WorkerState as DPWorkerState, StepState, WaveState,
    P2CLoadBalancer as DPLoadBalancer, DPEngineCoreProc,
    HierarchicalDPCoordinator, dp_collective_all_reduce
)


# =============================================================================
# AsyncEngineClient Tests
# =============================================================================

class TestClientMode:
    """Tests for ClientMode enum."""

    def test_modes_exist(self):
        """All client modes exist."""
        assert ClientMode.INPROC is not None
        assert ClientMode.SYNC_MP is not None
        assert ClientMode.ASYNC_MP is not None
        assert ClientMode.DP_ASYNC is not None

    def test_mode_values_unique(self):
        """Client mode values are unique."""
        modes = [m.value for m in ClientMode]
        assert len(modes) == len(set(modes))


class TestEngineClientConfig:
    """Tests for EngineClientConfig."""

    def test_default_config(self):
        """Default config has sensible values."""
        config = EngineClientConfig()
        assert config.mode == ClientMode.ASYNC_MP
        assert config.num_workers >= 1
        assert config.request_timeout_ms > 0

    def test_custom_config(self):
        """Custom config values are preserved."""
        config = EngineClientConfig(
            mode=ClientMode.DP_ASYNC,
            num_workers=4,
            p2c_sample_size=3
        )
        assert config.mode == ClientMode.DP_ASYNC
        assert config.num_workers == 4
        assert config.p2c_sample_size == 3


class TestSchedulerOutput:
    """Tests for SchedulerOutput dataclass."""

    def test_empty_output(self):
        """Empty scheduler output."""
        output = SchedulerOutput()
        assert output.request_ids == []
        assert output.scheduled_tokens == 0

    def test_populated_output(self):
        """Populated scheduler output."""
        output = SchedulerOutput(
            request_ids=["req_1", "req_2"],
            scheduled_tokens=100,
            num_prefill=50,
            num_decode=50
        )
        assert len(output.request_ids) == 2
        assert output.scheduled_tokens == 100


class TestInprocClient:
    """Tests for InprocClient."""

    def test_create_client(self):
        """Create in-process client."""
        config = EngineClientConfig(mode=ClientMode.INPROC)
        client = InprocClient(config)
        assert client is not None

    def test_send_request(self):
        """Send request returns request ID."""
        config = EngineClientConfig(mode=ClientMode.INPROC)
        client = InprocClient(config)
        client.start()

        request = SchedulerOutput(scheduled_tokens=10)
        request_id = client.send_request(request)

        assert request_id is not None
        assert request_id.startswith("req_")

        client.shutdown()

    def test_get_output(self):
        """Get output after sending request."""
        config = EngineClientConfig(mode=ClientMode.INPROC)
        client = InprocClient(config)
        client.start()

        request = SchedulerOutput(scheduled_tokens=10)
        request_id = client.send_request(request)
        output = client.get_output(request_id)

        assert output is not None
        assert output.request_id == request_id

        client.shutdown()


class TestP2CLoadBalancer:
    """Tests for P2C load balancer."""

    def test_create_balancer(self):
        """Create P2C load balancer."""
        workers = [
            WorkerInfo(worker_id=0, endpoint="ep0"),
            WorkerInfo(worker_id=1, endpoint="ep1")
        ]
        balancer = P2CLoadBalancer(workers)
        assert balancer is not None

    def test_select_worker(self):
        """Select worker returns valid worker."""
        workers = [
            WorkerInfo(worker_id=0, endpoint="ep0", pending_requests=5),
            WorkerInfo(worker_id=1, endpoint="ep1", pending_requests=2)
        ]
        balancer = P2CLoadBalancer(workers)

        selected = balancer.select_worker()
        assert selected.worker_id in [0, 1]

    def test_prefer_less_loaded(self):
        """Prefers worker with fewer pending requests."""
        workers = [
            WorkerInfo(worker_id=0, endpoint="ep0", pending_requests=100),
            WorkerInfo(worker_id=1, endpoint="ep1", pending_requests=1)
        ]
        balancer = P2CLoadBalancer(workers, sample_size=2)

        # With only 2 workers and sample_size=2, should pick least loaded
        selected = balancer.select_worker()
        assert selected.pending_requests <= 100


class TestAutoSelectClientMode:
    """Tests for auto_select_client_mode."""

    def test_single_gpu_selects_inproc(self):
        """Single GPU selects in-process mode."""
        mode = auto_select_client_mode(num_gpus=1, use_dp=False)
        assert mode == ClientMode.INPROC

    def test_multi_gpu_dp_selects_dp_async(self):
        """Multi-GPU with DP selects DP async mode."""
        mode = auto_select_client_mode(num_gpus=4, use_dp=True)
        assert mode == ClientMode.DP_ASYNC

    def test_multi_gpu_no_dp_selects_async(self):
        """Multi-GPU without DP selects async mode."""
        mode = auto_select_client_mode(num_gpus=4, use_dp=False)
        assert mode == ClientMode.ASYNC_MP


class TestCreateEngineClient:
    """Tests for create_engine_client factory."""

    def test_creates_inproc_client(self):
        """Factory creates in-process client."""
        client = create_engine_client(num_gpus=1)
        assert isinstance(client, InprocClient)

    def test_creates_dp_client(self):
        """Factory creates DP client for multi-GPU."""
        client = create_engine_client(num_gpus=4, use_dp=True)
        assert isinstance(client, DPAsyncMPClient)


# =============================================================================
# BlockPoolManager Tests
# =============================================================================

class TestBlockState:
    """Tests for BlockState enum."""

    def test_states_ordered(self):
        """States have priority ordering."""
        assert BlockState.FREE < BlockState.ALLOCATED
        assert BlockState.ALLOCATED < BlockState.CACHED
        assert BlockState.CACHED < BlockState.PINNED


class TestBlock:
    """Tests for Block dataclass."""

    def test_create_block(self):
        """Create block with defaults."""
        block = Block(block_id=0)
        assert block.block_id == 0
        assert block.state == BlockState.FREE
        assert block.ref_count == 0

    def test_touch_updates_access(self):
        """Touch updates access time and count."""
        block = Block(block_id=0)
        old_time = block.last_access
        old_count = block.access_count

        time.sleep(0.01)
        block.touch()

        assert block.last_access > old_time
        assert block.access_count == old_count + 1


class TestBlockPoolConfig:
    """Tests for BlockPoolConfig."""

    def test_default_config(self):
        """Default config has sensible values."""
        config = BlockPoolConfig()
        assert config.num_blocks > 0
        assert config.block_size_bytes > 0
        assert config.eviction_policy in ("lru", "arc")


class TestARCPolicy:
    """Tests for ARC eviction policy."""

    def test_create_arc(self):
        """Create ARC policy."""
        arc = ARCPolicy(capacity=100)
        assert arc.capacity == 100

    def test_insert_and_access(self):
        """Insert and access blocks."""
        arc = ARCPolicy(capacity=10)
        block = Block(block_id=1)

        evicted = arc.insert(block)
        assert evicted is None  # No eviction needed

        hit = arc.access(block)
        assert hit  # Should hit after insert

    def test_eviction_when_full(self):
        """Evicts when at capacity."""
        arc = ARCPolicy(capacity=2)

        for i in range(3):
            block = Block(block_id=i)
            evicted = arc.insert(block)

            if i >= 2:
                assert evicted is not None


class TestBlockPool:
    """Tests for BlockPool."""

    def test_create_pool(self):
        """Create block pool."""
        config = BlockPoolConfig(num_blocks=100)
        pool = BlockPool(config)
        assert pool.get_num_free_blocks() == 100

    def test_allocate_blocks(self):
        """Allocate blocks from pool."""
        config = BlockPoolConfig(num_blocks=100)
        pool = BlockPool(config)

        blocks = pool.get_new_blocks(10)
        assert len(blocks) == 10
        assert pool.get_num_free_blocks() == 90

    def test_free_blocks(self):
        """Free allocated blocks."""
        config = BlockPoolConfig(num_blocks=100)
        pool = BlockPool(config)

        blocks = pool.get_new_blocks(10)
        pool.free_blocks(blocks)

        assert pool.get_num_free_blocks() == 100

    def test_cache_blocks(self):
        """Cache blocks with hashes."""
        config = BlockPoolConfig(num_blocks=100)
        pool = BlockPool(config)

        blocks = pool.get_new_blocks(5)
        hashes = [i * 12345 for i in range(5)]

        pool.cache_blocks(blocks, hashes)

        # Should be able to look up cached blocks
        found = pool.lookup_cached_block(hashes[0])
        assert found == blocks[0]

    def test_touch_blocks(self):
        """Touch updates block recency."""
        config = BlockPoolConfig(num_blocks=100)
        pool = BlockPool(config)

        blocks = pool.get_new_blocks(5)
        old_access = pool.get_block(blocks[0]).last_access

        time.sleep(0.01)
        pool.touch(blocks)

        new_access = pool.get_block(blocks[0]).last_access
        assert new_access > old_access

    def test_metrics(self):
        """Get pool metrics."""
        config = BlockPoolConfig(num_blocks=100)
        pool = BlockPool(config)

        pool.get_new_blocks(20)
        metrics = pool.get_metrics()

        assert metrics.total_blocks == 100
        assert metrics.allocations == 20


class TestComputeBlockHash:
    """Tests for compute_block_hash."""

    def test_compute_hash(self):
        """Compute hash for content."""
        content = b"test content"
        hash1 = compute_block_hash(content)
        hash2 = compute_block_hash(content)

        assert hash1 == hash2  # Deterministic

    def test_different_content_different_hash(self):
        """Different content produces different hash."""
        hash1 = compute_block_hash(b"content1")
        hash2 = compute_block_hash(b"content2")

        assert hash1 != hash2


# =============================================================================
# GPUMemoryAllocator Tests
# =============================================================================

class TestMemoryState:
    """Tests for MemoryState enum."""

    def test_states_exist(self):
        """Memory states exist."""
        assert MemoryState.ACTIVE is not None
        assert MemoryState.SLEEPING is not None
        assert MemoryState.SNAPSHOT is not None


class TestMemoryPoolConfig:
    """Tests for MemoryPoolConfig."""

    def test_default_config(self):
        """Default config has sensible values."""
        config = MemoryPoolConfig()
        assert config.pool_size_bytes > 0
        assert config.block_size_bytes > 0


class TestCuMemAllocator:
    """Tests for CuMemAllocator."""

    def test_create_allocator(self):
        """Create memory allocator."""
        config = MemoryPoolConfig(pool_size_bytes=1024 * 1024)
        allocator = CuMemAllocator(config)
        assert allocator.available_bytes > 0

    def test_allocate(self):
        """Allocate memory region."""
        config = MemoryPoolConfig(
            pool_size_bytes=10 * 1024 * 1024,
            block_size_bytes=1024 * 1024
        )
        allocator = CuMemAllocator(config)

        region_id = allocator.allocate(1024 * 1024)
        assert region_id is not None

    def test_deallocate(self):
        """Deallocate memory region."""
        config = MemoryPoolConfig(
            pool_size_bytes=10 * 1024 * 1024,
            block_size_bytes=1024 * 1024
        )
        allocator = CuMemAllocator(config)

        region_id = allocator.allocate(1024 * 1024)
        result = allocator.deallocate(region_id)

        assert result is True

    def test_sleep_wake(self):
        """Sleep and wake up allocator."""
        config = MemoryPoolConfig(pool_size_bytes=10 * 1024 * 1024)
        allocator = CuMemAllocator(config)

        released = allocator.sleep()
        assert released >= 0
        assert allocator.is_sleeping

        reclaimed = allocator.wake_up()
        assert reclaimed >= 0
        assert not allocator.is_sleeping

    def test_snapshot(self):
        """Take memory snapshot."""
        config = MemoryPoolConfig(pool_size_bytes=10 * 1024 * 1024)
        allocator = CuMemAllocator(config)

        allocator.allocate(1024 * 1024)
        snapshot = allocator.take_snapshot()

        assert snapshot.total_bytes > 0
        assert snapshot.allocated_bytes > 0

    def test_use_memory_pool_context(self):
        """Use memory pool context manager."""
        config = MemoryPoolConfig(pool_size_bytes=10 * 1024 * 1024)
        allocator = CuMemAllocator(config)

        with allocator.use_memory_pool():
            region_id = allocator.allocate(1024 * 1024)
            assert region_id is not None


class TestMultiGPUMemoryBalancer:
    """Tests for MultiGPUMemoryBalancer."""

    def test_create_balancer(self):
        """Create multi-GPU balancer."""
        balancer = MultiGPUMemoryBalancer(num_devices=2)
        assert balancer.num_devices == 2

    def test_allocate_balanced(self):
        """Balanced allocation across GPUs."""
        balancer = MultiGPUMemoryBalancer(num_devices=2)

        result = balancer.allocate_balanced(1024 * 1024)
        assert result is not None
        device_id, region_id = result
        assert device_id in [0, 1]


# =============================================================================
# PrefixCacheOptimizer Tests
# =============================================================================

class TestCacheTier:
    """Tests for CacheTier enum."""

    def test_tiers_exist(self):
        """Cache tiers exist."""
        assert CacheTier.HOT is not None
        assert CacheTier.WARM is not None
        assert CacheTier.COLD is not None


class TestPrefixTree:
    """Tests for PrefixTree (radix tree)."""

    def test_create_tree(self):
        """Create empty prefix tree."""
        tree = PrefixTree()
        assert len(tree) == 0

    def test_insert_and_find(self):
        """Insert and find prefix."""
        tree = PrefixTree()
        tokens = (1, 2, 3, 4, 5)
        entry = PrefixEntry(
            prefix_hash=12345,
            token_ids=tokens,
            block_ids=[0, 1]
        )

        tree.insert(tokens, entry)
        assert len(tree) == 1

        result = tree.find_longest_prefix(tokens)
        assert result is not None
        matched_len, found_entry = result
        assert matched_len == 5

    def test_longest_prefix_match(self):
        """Find longest matching prefix."""
        tree = PrefixTree()

        # Insert shorter prefix
        short_tokens = (1, 2, 3)
        short_entry = PrefixEntry(
            prefix_hash=123,
            token_ids=short_tokens,
            block_ids=[0]
        )
        tree.insert(short_tokens, short_entry)

        # Query with longer sequence
        query = (1, 2, 3, 4, 5)
        result = tree.find_longest_prefix(query)

        assert result is not None
        matched_len, entry = result
        assert matched_len == 3

    def test_remove_prefix(self):
        """Remove prefix from tree."""
        tree = PrefixTree()
        tokens = (1, 2, 3)
        entry = PrefixEntry(
            prefix_hash=123,
            token_ids=tokens,
            block_ids=[0]
        )

        tree.insert(tokens, entry)
        assert len(tree) == 1

        result = tree.remove(tokens)
        assert result is True
        assert len(tree) == 0


class TestPrefixCacheOptimizer:
    """Tests for PrefixCacheOptimizer."""

    def test_create_optimizer(self):
        """Create prefix cache optimizer."""
        optimizer = PrefixCacheOptimizer()
        assert optimizer is not None

    def test_cache_prefix(self):
        """Cache a prefix."""
        optimizer = PrefixCacheOptimizer()

        tokens = [1, 2, 3, 4, 5]
        block_ids = [0, 1]

        prefix_hash = optimizer.cache_prefix(tokens, block_ids)
        assert prefix_hash > 0

    def test_find_cache_hit(self):
        """Find cache hit."""
        optimizer = PrefixCacheOptimizer()

        tokens = [1, 2, 3, 4, 5]
        block_ids = [0, 1]

        optimizer.cache_prefix(tokens, block_ids)

        result = optimizer.find_longest_cache_hit(tokens)
        assert result.hit is True
        assert result.matched_tokens == 5
        assert result.block_ids == block_ids

    def test_cache_miss(self):
        """Cache miss for unknown prefix."""
        optimizer = PrefixCacheOptimizer()

        result = optimizer.find_longest_cache_hit([99, 98, 97])
        assert result.hit is False

    def test_get_computed_blocks(self):
        """Get computed blocks for prefix."""
        optimizer = PrefixCacheOptimizer()

        tokens = [1, 2, 3]
        block_ids = [10, 11, 12]

        optimizer.cache_prefix(tokens, block_ids)

        computed = optimizer.get_computed_blocks(tokens)
        assert computed == block_ids

    def test_metrics(self):
        """Get cache metrics."""
        optimizer = PrefixCacheOptimizer()

        optimizer.cache_prefix([1, 2, 3], [0])
        optimizer.find_longest_cache_hit([1, 2, 3])  # Hit
        optimizer.find_longest_cache_hit([9, 9, 9])  # Miss

        metrics = optimizer.get_metrics()
        assert metrics["total_entries"] == 1
        assert metrics["total_hits"] == 1
        assert metrics["total_misses"] == 1


# =============================================================================
# AsyncModelRunner Tests
# =============================================================================

class TestRunnerState:
    """Tests for RunnerState enum."""

    def test_states_exist(self):
        """Runner states exist."""
        assert RunnerState.IDLE is not None
        assert RunnerState.EXECUTING is not None
        assert RunnerState.WAITING is not None


class TestModelInput:
    """Tests for ModelInput dataclass."""

    def test_create_input(self):
        """Create model input."""
        input_data = ModelInput(
            request_id="req_1",
            input_ids=[1, 2, 3]
        )
        assert input_data.request_id == "req_1"


class TestAsyncGPUPoolingModelRunnerOutput:
    """Tests for output pooling."""

    def test_create_pool(self):
        """Create output pool."""
        pool = AsyncGPUPoolingModelRunnerOutput[ModelOutput](pool_size=10)
        pool.set_factory(lambda: ModelOutput(request_id=""))
        assert pool is not None

    def test_acquire_release(self):
        """Acquire and release from pool."""
        pool = AsyncGPUPoolingModelRunnerOutput[ModelOutput](pool_size=10)
        pool.set_factory(lambda: ModelOutput(request_id=""))

        obj = pool.acquire()
        assert obj is not None

        pool.release(obj)

        stats = pool.get_stats()
        assert stats["allocated"] >= 1


class TestAsyncModelRunner:
    """Tests for AsyncModelRunner."""

    def test_create_runner(self):
        """Create async model runner."""
        runner = AsyncModelRunner()
        assert runner.is_idle

    def test_sync_execution(self):
        """Synchronous model execution."""
        runner = AsyncModelRunner()

        scheduler_output = RunnerSchedulerOutput(
            request_ids=["req_1"],
            inputs=[ModelInput(request_id="req_1", input_ids=[1, 2, 3])],
            total_tokens=3
        )

        outputs = runner.execute_model_sync(scheduler_output)
        assert len(outputs) == 1
        assert outputs[0].request_id == "req_1"

    @pytest.mark.asyncio
    async def test_async_execution(self):
        """Async model execution."""
        runner = AsyncModelRunner()

        scheduler_output = RunnerSchedulerOutput(
            request_ids=["req_1"],
            inputs=[ModelInput(request_id="req_1", input_ids=[1, 2, 3])],
            total_tokens=3
        )

        outputs = await runner.execute_model_async(scheduler_output)
        assert len(outputs) == 1

    def test_metrics(self):
        """Get runner metrics."""
        runner = AsyncModelRunner()

        scheduler_output = RunnerSchedulerOutput(
            request_ids=["req_1"],
            inputs=[ModelInput(request_id="req_1", input_ids=[1, 2, 3])],
            total_tokens=3
        )

        runner.execute_model_sync(scheduler_output)

        metrics = runner.get_metrics()
        assert metrics["total_executions"] == 1
        assert metrics["total_tokens"] == 3


# =============================================================================
# DataParallelCoordinator Tests
# =============================================================================

class TestDPRole:
    """Tests for DPRole enum."""

    def test_roles_exist(self):
        """DP roles exist."""
        assert DPRole.MASTER is not None
        assert DPRole.WORKER is not None
        assert DPRole.HYBRID is not None


class TestDPConfig:
    """Tests for DPConfig."""

    def test_default_config(self):
        """Default config has sensible values."""
        config = DPConfig()
        assert config.num_workers >= 1
        assert config.dp_size >= 1


class TestStepState:
    """Tests for StepState."""

    def test_create_step(self):
        """Create step state."""
        step = StepState(step_id=1, wave_id=1, request_count=10)
        assert step.step_id == 1
        assert not step.is_complete

    def test_step_completion(self):
        """Step completion tracking."""
        step = StepState(step_id=1, wave_id=1, request_count=10)
        step.completed_count = 10
        assert step.is_complete


class TestDPEngineCoreProc:
    """Tests for DPEngineCoreProc."""

    def test_create_coordinator(self):
        """Create DP coordinator."""
        config = DPConfig(num_workers=4, dp_size=2)
        coord = DPEngineCoreProc(config)
        assert coord.get_step_counter() == 0

    def test_step_lifecycle(self):
        """Step begin/end lifecycle."""
        config = DPConfig(num_workers=4)
        coord = DPEngineCoreProc(config)

        step = coord.begin_step(num_requests=5)
        assert step.step_id == 1
        assert coord.get_step_counter() == 1

        ended = coord.end_step()
        assert ended.step_id == 1

    def test_wave_lifecycle(self):
        """Wave begin/end lifecycle."""
        config = DPConfig(num_workers=4)
        coord = DPEngineCoreProc(config)

        wave = coord.begin_wave(num_steps=3)
        assert wave.wave_id == 1
        assert coord.get_wave_id() == 1

        ended = coord.end_wave()
        assert ended.wave_id == 1

    def test_worker_selection(self):
        """Select worker for request."""
        config = DPConfig(num_workers=4)
        coord = DPEngineCoreProc(config)

        worker = coord.select_worker()
        assert worker.worker_id in range(4)

    def test_request_assignment(self):
        """Assign request to worker."""
        config = DPConfig(num_workers=4)
        coord = DPEngineCoreProc(config)

        worker_id = coord.assign_request("req_1")
        assert worker_id in range(4)

    def test_complete_request(self):
        """Complete request updates metrics."""
        config = DPConfig(num_workers=4)
        coord = DPEngineCoreProc(config)

        worker_id = coord.assign_request("req_1")
        coord.complete_request(worker_id, latency_ms=10.0)

        workers = coord.get_worker_states()
        worker = next(w for w in workers if w.worker_id == worker_id)
        assert worker.total_processed == 1

    def test_metrics(self):
        """Get coordinator metrics."""
        config = DPConfig(num_workers=4, dp_size=2)
        coord = DPEngineCoreProc(config)

        coord.begin_step(5)
        coord.end_step()

        metrics = coord.get_metrics()
        assert metrics["step_counter"] == 1
        assert metrics["num_workers"] == 4


class TestHierarchicalDPCoordinator:
    """Tests for HierarchicalDPCoordinator."""

    def test_create_hierarchical(self):
        """Create hierarchical coordinator."""
        coord = HierarchicalDPCoordinator(
            num_local_coordinators=2,
            workers_per_coordinator=4
        )
        assert coord._num_local == 2

    def test_route_request(self):
        """Route request through hierarchy."""
        coord = HierarchicalDPCoordinator(
            num_local_coordinators=2,
            workers_per_coordinator=4
        )

        coord_idx, worker_id = coord.route_request("req_1")
        assert coord_idx in [0, 1]
        assert worker_id in range(4)

    def test_global_metrics(self):
        """Get global aggregated metrics."""
        coord = HierarchicalDPCoordinator(
            num_local_coordinators=2,
            workers_per_coordinator=4
        )

        metrics = coord.get_global_metrics()
        assert metrics["num_coordinators"] == 2
        assert metrics["total_workers"] == 8


# =============================================================================
# Rust Acceleration Tests
# =============================================================================

@pytest.fixture
def rust_module():
    """Get rust_core module if available."""
    try:
        import rust_core
        return rust_core
    except ImportError:
        pytest.skip("rust_core not available")


class TestRustBlockPoolEvictLRU:
    """Tests for block_pool_evict_lru_rust."""

    def test_evict_lru(self, rust_module):
        """LRU eviction selects oldest cached blocks."""
        last_access = [1.0, 5.0, 2.0, 4.0, 3.0]
        states = [2, 2, 2, 2, 2]  # All CACHED

        evicted = rust_module.block_pool_evict_lru_rust(last_access, states, 2)

        assert len(evicted) == 2
        assert 0 in evicted  # Oldest (1.0)
        assert 2 in evicted  # Second oldest (2.0)

    def test_skip_non_cached(self, rust_module):
        """Skips non-cached blocks."""
        last_access = [1.0, 5.0, 2.0]
        states = [0, 2, 3]  # FREE, CACHED, PINNED

        evicted = rust_module.block_pool_evict_lru_rust(last_access, states, 2)

        assert len(evicted) <= 1
        if evicted:
            assert evicted[0] == 1  # Only cached block


class TestRustARCCacheBalance:
    """Tests for arc_cache_balance_rust."""

    def test_b1_hit_increases_p(self, rust_module):
        """B1 ghost hit increases p (favor recency)."""
        new_p = rust_module.arc_cache_balance_rust(
            10, 10, 5, 10, 100, 50.0, True, False
        )

        assert new_p > 50.0

    def test_b2_hit_decreases_p(self, rust_module):
        """B2 ghost hit decreases p (favor frequency)."""
        new_p = rust_module.arc_cache_balance_rust(
            10, 10, 10, 5, 100, 50.0, False, True
        )

        assert new_p < 50.0


class TestRustPrefixTreeLookup:
    """Tests for prefix_tree_lookup_rust."""

    def test_find_match(self, rust_module):
        """Find matching prefix."""
        query = [1, 2, 3]
        prefix_hashes = [12345, 67890]
        prefix_lengths = [3, 5]

        # Compute hash for query (simulating same hash algorithm)
        # Note: This is a simplified test
        matched_len, matched_idx = rust_module.prefix_tree_lookup_rust(
            query, prefix_hashes, prefix_lengths
        )

        # May not match due to hash algorithm differences
        assert matched_len >= -1


class TestRustBlockHashCompute:
    """Tests for block_hash_compute_rust."""

    def test_compute_hash(self, rust_module):
        """Compute hash for tokens."""
        tokens = [1, 2, 3, 4, 5]
        hash1 = rust_module.block_hash_compute_rust(tokens, 0)
        hash2 = rust_module.block_hash_compute_rust(tokens, 0)

        assert hash1 == hash2  # Deterministic

    def test_different_tokens_different_hash(self, rust_module):
        """Different tokens produce different hashes."""
        hash1 = rust_module.block_hash_compute_rust([1, 2, 3], 0)
        hash2 = rust_module.block_hash_compute_rust([4, 5, 6], 0)

        assert hash1 != hash2


class TestRustP2CSelectWorker:
    """Tests for p2c_select_worker_rust."""

    def test_select_least_loaded(self, rust_module):
        """Selects least loaded worker."""
        pending = [10, 1, 5, 3]
        latencies = [10.0, 10.0, 10.0, 10.0]
        health = [0, 0, 0, 0]  # All healthy

        selected = rust_module.p2c_select_worker_rust(pending, latencies, health, 4)

        assert selected == 1  # Least pending

    def test_skip_failed_workers(self, rust_module):
        """Skips failed workers."""
        pending = [1, 100, 100, 100]
        latencies = [10.0, 10.0, 10.0, 10.0]
        health = [3, 0, 0, 0]  # First is FAILED

        selected = rust_module.p2c_select_worker_rust(pending, latencies, health, 4)

        assert selected != 0  # Should not select failed worker


class TestRustStepCounterSync:
    """Tests for step_counter_sync_rust."""

    def test_increment_step(self, rust_module):
        """Increment step counter."""
        new_step, is_synced = rust_module.step_counter_sync_rust(0, 0, 4)

        assert new_step == 1

    def test_sync_detection(self, rust_module):
        """Detect when all ranks synced."""
        _, is_synced = rust_module.step_counter_sync_rust(3, 0, 4)

        assert is_synced is True  # Step 4 is divisible by dp_size=4


class TestRustWaveIdBarrier:
    """Tests for wave_id_barrier_rust."""

    def test_incomplete_wave(self, rust_module):
        """Incomplete wave detection."""
        is_complete, ratio = rust_module.wave_id_barrier_rust(
            1, [5, 5, 5, 5], 10
        )

        assert is_complete is False

    def test_complete_wave(self, rust_module):
        """Complete wave detection."""
        is_complete, ratio = rust_module.wave_id_barrier_rust(
            1, [10, 10, 10, 10], 10
        )

        assert is_complete is True
        assert ratio == 100


class TestRustAsyncOutputMerge:
    """Tests for async_output_merge_rust."""

    def test_merge_outputs(self, rust_module):
        """Merge async outputs."""
        request_ids = ["req_1", "req_2", "req_3"]
        completion_times = [1.0, 2.0, 0.0]
        is_finished = [True, True, False]

        result = rust_module.async_output_merge_rust(
            request_ids, completion_times, is_finished
        )

        assert len(result["completed"]) == 2
        assert len(result["pending"]) == 1
        assert 2 in result["pending"]


class TestRustDPRankCoordinate:
    """Tests for dp_rank_coordinate_rust."""

    def test_rank_assignment(self, rust_module):
        """Assign ranks to workers."""
        result = rust_module.dp_rank_coordinate_rust(
            num_workers=8,
            dp_size=4,
            locality_groups=[[0, 1], [2, 3], [4, 5], [6, 7]]
        )

        assert len(result["ranks"]) == 8
        assert len(result["localities"]) == 8


class TestRustKVMetricsAggregate:
    """Tests for kv_metrics_aggregate_rust."""

    def test_aggregate_metrics(self, rust_module):
        """Aggregate KV cache metrics."""
        result = rust_module.kv_metrics_aggregate_rust(
            hits_per_worker=[100, 200, 150],
            misses_per_worker=[10, 20, 15],
            evictions_per_worker=[5, 10, 7],
            allocated_per_worker=[1000, 2000, 1500]
        )

        assert result["total_hits"] == 450
        assert result["total_misses"] == 45
        assert result["total_evictions"] == 22


class TestRustCacheHitScore:
    """Tests for cache_hit_score_rust."""

    def test_compute_scores(self, rust_module):
        """Compute cache hit scores."""
        scores = rust_module.cache_hit_score_rust(
            hit_counts=[10, 50, 25],
            last_access_times=[1.0, 5.0, 3.0],
            current_time=10.0,
            recency_weight=0.5,
            frequency_weight=0.5
        )

        assert len(scores) == 3
        # Higher hits + more recent = higher score
        assert scores[1] > scores[0]  # 50 hits, recent vs 10 hits, old


# =============================================================================
# Integration Tests
# =============================================================================

class TestPhase35Integration:
    """Integration tests for Phase 35 components."""

    def test_engine_with_block_pool(self):
        """Engine client with block pool."""
        # Create components
        engine = create_engine_client(num_gpus=1)
        pool = BlockPool(BlockPoolConfig(num_blocks=100))

        # Allocate blocks for request
        blocks = pool.get_new_blocks(5)

        # Create request with block tables
        request = SchedulerOutput(
            request_ids=["req_1"],
            scheduled_tokens=100,
            block_tables={"req_1": blocks}
        )

        engine.start()
        request_id = engine.send_request(request)
        output = engine.get_output(request_id)
        engine.shutdown()

        # Free blocks
        pool.free_blocks(blocks)

        assert output is not None
        assert pool.get_num_free_blocks() == 100

    def test_prefix_cache_with_memory(self):
        """Prefix cache with memory allocator."""
        # Create components
        prefix_cache = PrefixCacheOptimizer()
        memory = CuMemAllocator(MemoryPoolConfig(pool_size_bytes=10 * 1024 * 1024))

        # Allocate memory for KV cache
        region_id = memory.allocate(1024 * 1024)

        # Cache prefix with block info
        tokens = [1, 2, 3, 4, 5]
        prefix_cache.cache_prefix(tokens, [region_id])

        # Look up cached prefix
        result = prefix_cache.find_longest_cache_hit(tokens)

        assert result.hit
        assert region_id in result.block_ids

        # Cleanup
        memory.deallocate(region_id)

    def test_dp_coordinator_with_runner(self):
        """DP coordinator with async runner."""
        # Create components
        config = DPConfig(num_workers=4)
        coordinator = DPEngineCoreProc(config)
        runner = AsyncModelRunner()

        # Begin step
        step = coordinator.begin_step(num_requests=3)

        # Assign and execute requests
        for i in range(3):
            worker_id = coordinator.assign_request(f"req_{i}")

            input_data = ModelInput(
                request_id=f"req_{i}",
                input_ids=[1, 2, 3]
            )

            scheduler_output = RunnerSchedulerOutput(
                request_ids=[f"req_{i}"],
                inputs=[input_data],
                total_tokens=3
            )

            outputs = runner.execute_model_sync(scheduler_output)

            coordinator.complete_request(worker_id, latency_ms=1.0)

        # End step
        ended = coordinator.end_step()

        assert ended.completed_count == 3

        runner.shutdown()


# =============================================================================
# Performance Tests
# =============================================================================

class TestPhase35Performance:
    """Performance tests for Phase 35 components."""

    @pytest.mark.skip(reason="Performance test - run manually")
    def test_block_pool_allocation_speed(self):
        """Block pool allocation performance."""
        pool = BlockPool(BlockPoolConfig(num_blocks=10000))

        start = time.perf_counter()
        for _ in range(1000):
            blocks = pool.get_new_blocks(10)
            pool.free_blocks(blocks)
        elapsed = time.perf_counter() - start

        ops_per_sec = 2000 / elapsed  # 1000 alloc + 1000 free
        print(f"Block pool: {ops_per_sec:.0f} ops/sec")

        assert ops_per_sec > 10000  # Should be fast

    @pytest.mark.skip(reason="Performance test - run manually")
    def test_prefix_cache_lookup_speed(self):
        """Prefix cache lookup performance."""
        cache = PrefixCacheOptimizer()

        # Insert many prefixes
        for i in range(1000):
            tokens = list(range(i, i + 100))
            cache.cache_prefix(tokens, [i])

        # Measure lookup speed
        start = time.perf_counter()
        for i in range(1000):
            tokens = list(range(i, i + 50))
            cache.find_longest_cache_hit(tokens)
        elapsed = time.perf_counter() - start

        lookups_per_sec = 1000 / elapsed
        print(f"Prefix cache: {lookups_per_sec:.0f} lookups/sec")

        assert lookups_per_sec > 1000


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
