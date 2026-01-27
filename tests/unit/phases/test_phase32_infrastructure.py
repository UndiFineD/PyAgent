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

"""Tests for Phase 32: Beyond vLLM - High-Performance GPU Infrastructure.

This module tests:
- UvaBufferPool: Zero-copy GPU transfers
- StagedBatchWriter: Batched GPU writes
- MicroBatchContext: Micro-batch orchestration
- CudaStreamPool: Stream management
- AdvancedRequestScheduler: Priority scheduling with preemption
- ChunkedPrefillManager: Chunked prefill orchestration
- Rust accelerations for Phase 32
"""

import pytest
import time
import threading
from unittest.mock import Mock, patch, MagicMock

# =============================================================================
# UvaBufferPool Tests
# =============================================================================

class TestUvaBuffer:
    """Tests for UvaBuffer class."""

    def test_buffer_creation(self):
        """Test UVA buffer creation."""
        from src.core.base.logic.structures.uva_buffer_pool import UvaBuffer, BufferState

        buffer = UvaBuffer(
            buffer_id=0,
            size=1024 * 1024,  # 1 MB
            state=BufferState.FREE,
        )

        assert buffer.buffer_id == 0
        assert buffer.size == 1024 * 1024
        assert buffer.state == BufferState.FREE
        assert buffer.stats.allocations == 0

    def test_buffer_state_transitions(self):
        """Test buffer state changes."""
        from src.core.base.logic.structures.uva_buffer_pool import UvaBuffer, BufferState

        buffer = UvaBuffer(buffer_id=1, size=1024)

        assert buffer.state == BufferState.FREE
        buffer.state = BufferState.ACQUIRED
        assert buffer.state == BufferState.ACQUIRED
        buffer.reset()
        assert buffer.state == BufferState.FREE

    def test_buffer_stats(self):
        """Test buffer statistics."""
        from src.core.base.logic.structures.uva_buffer_pool import BufferStats

        stats = BufferStats(
            allocations=100,
            total_bytes_transferred=1024 * 1024 * 100,
            total_transfer_time_ns=1_000_000_000,  # 1 second
        )

        assert stats.avg_transfer_time_ms == 10.0  # 1s / 100 = 10ms
        assert stats.throughput_gbps > 0


class TestUvaBufferPool:
    """Tests for UvaBufferPool class."""

    def test_pool_creation(self):
        """Test pool initialization."""
        from src.core.base.logic.structures.uva_buffer_pool import (
            UvaBufferPool, AllocationStrategy
        )

        pool = UvaBufferPool(
            buffer_count=4,
            buffer_size=1024 * 1024,
            strategy=AllocationStrategy.ROUND_ROBIN,
        )

        assert pool.buffer_count == 4
        assert pool.buffer_size == 1024 * 1024

    def test_acquire_release(self):
        """Test buffer acquisition and release."""
        from src.core.base.logic.structures.uva_buffer_pool import UvaBufferPool

        pool = UvaBufferPool(buffer_count=2, buffer_size=1024)

        # Acquire first buffer
        buffer1 = pool.acquire()
        assert buffer1 is not None
        assert buffer1.buffer_id == 0

        # Acquire second buffer
        buffer2 = pool.acquire()
        assert buffer2 is not None
        assert buffer2.buffer_id == 1

        # Release first buffer
        pool.release(buffer1)

        # Acquire again - should get first buffer back
        buffer3 = pool.acquire()
        assert buffer3 is not None
        assert buffer3.buffer_id == 0

    def test_pool_exhaustion(self):
        """Test behavior when pool is exhausted."""
        from src.core.base.logic.structures.uva_buffer_pool import UvaBufferPool

        pool = UvaBufferPool(buffer_count=2, buffer_size=1024, max_buffers=2)

        buffer1 = pool.acquire()
        buffer2 = pool.acquire()

        # Non-blocking acquire should return None
        buffer3 = pool.acquire(blocking=False)
        assert buffer3 is None

        # Timeout acquire should also return None
        buffer4 = pool.acquire(blocking=True, timeout=0.01)
        assert buffer4 is None

        # Release and try again
        pool.release(buffer1)
        buffer5 = pool.acquire(blocking=False)
        assert buffer5 is not None

    def test_pool_stats(self):
        """Test pool statistics."""
        from src.core.base.logic.structures.uva_buffer_pool import UvaBufferPool

        pool = UvaBufferPool(buffer_count=4, buffer_size=1024)

        buffer = pool.acquire()
        pool.release(buffer)

        stats = pool.stats
        assert stats["buffer_count"] == 4
        assert stats["total_allocations"] >= 1


class TestUvaBackedTensor:
    """Tests for UvaBackedTensor class."""

    def test_tensor_creation(self):
        """Test UVA-backed tensor creation."""
        pytest.importorskip("torch")
        from src.core.base.logic.structures.uva_buffer_pool import UvaBackedTensor

        tensor = UvaBackedTensor(
            shape=(32, 64),
            dtype=None,  # Default float32
        )

        assert tensor.shape == (32, 64)


# =============================================================================
# StagedBatchWriter Tests
# =============================================================================

class TestStagedBatchWriter:
    """Tests for StagedBatchWriter class."""

    def test_writer_creation(self):
        """Test staged batch writer creation."""
        from src.core.base.logic.structures.staged_batch_writer import (
            StagedBatchWriter, WritePolicy, CoalesceStrategy
        )

        writer = StagedBatchWriter(
            initial_capacity=1024,
            policy=WritePolicy.LAST_WRITE_WINS,
            coalesce=CoalesceStrategy.SORT_BY_INDEX,
        )

        assert writer.capacity >= 1024
        assert writer.policy == WritePolicy.LAST_WRITE_WINS

    def test_stage_writes(self):
        """Test staging write operations."""
        from src.core.base.logic.structures.staged_batch_writer import StagedBatchWriter

        writer = StagedBatchWriter()

        writer.stage_write(index=10, value=1.5)
        writer.stage_write(index=20, value=2.0)
        writer.stage_write(index=30, value=3.0)

        assert writer.pending_count() == 3
        assert writer.stats.total_writes == 3

    def test_clear_staged(self):
        """Test clearing staged writes."""
        from src.core.base.logic.structures.staged_batch_writer import StagedBatchWriter

        writer = StagedBatchWriter()

        writer.stage_write(index=10, value=1.5)
        writer.stage_write(index=20, value=2.0)

        assert writer.pending_count() == 2

        writer.clear_staged()

        assert writer.pending_count() == 0

    def test_conflict_resolution_last_wins(self):
        """Test last-write-wins conflict resolution."""
        from src.core.base.logic.structures.staged_batch_writer import (
            StagedBatchWriter, WritePolicy
        )

        writer = StagedBatchWriter(policy=WritePolicy.LAST_WRITE_WINS)

        # Multiple writes to same index
        writer.stage_write(index=10, value=1.0)
        time.sleep(0.001)  # Ensure different timestamps
        writer.stage_write(index=10, value=2.0)
        time.sleep(0.001)
        writer.stage_write(index=10, value=3.0)

        # Internal coalescing should keep last value
        indices, values = writer._coalesce_writes()

        assert len(indices) == 1
        assert indices[0] == 10
        assert values[0] == 3.0

    def test_coalesce_indices(self):
        """Test write index coalescing."""
        from src.core.base.logic.structures.staged_batch_writer import coalesce_write_indices

        indices = [100, 10, 50, 11, 12, 51]
        coalesced = coalesce_write_indices(indices, block_size=32)

        # Should be sorted by block then offset
        assert coalesced[0] == 10
        assert coalesced[1] == 11
        assert coalesced[2] == 12


class TestStagedWriteTensor:
    """Tests for StagedWriteTensor class."""

    def test_staged_tensor_creation(self):
        """Test staged write tensor creation."""
        pytest.importorskip("torch")
        from src.core.base.logic.structures.staged_batch_writer import StagedWriteTensor

        tensor = StagedWriteTensor(
            shape=(100,),
            fill_value=0.0,
        )

        assert tensor.shape == (100,)
        assert tensor.pending_count == 0


# =============================================================================
# MicroBatchContext Tests
# =============================================================================

class TestStreamManager:
    """Tests for StreamManager class."""

    def test_stream_manager_creation(self):
        """Test stream manager creation."""
        from src.core.base.logic.core.micro_batch_context import StreamManager

        manager = StreamManager(
            num_compute_streams=2,
            num_comm_streams=1,
        )

        assert manager.num_compute_streams == 2
        assert manager.num_comm_streams == 1

    def test_stream_round_robin(self):
        """Test round-robin stream allocation."""
        from src.core.base.logic.core.micro_batch_context import StreamManager

        manager = StreamManager(num_compute_streams=2)

        stream1 = manager.get_compute_stream()
        stream2 = manager.get_compute_stream()
        stream3 = manager.get_compute_stream()

        if stream1 is not None:
            assert stream1.stream_id == 0
            assert stream2.stream_id == 1
            assert stream3.stream_id == 0  # Round-robin back to first


class TestMicroBatchContext:
    """Tests for MicroBatchContext class."""

    def test_context_creation(self):
        """Test micro-batch context creation."""
        from src.core.base.logic.core.micro_batch_context import MicroBatchContext

        ctx = MicroBatchContext(
            batch_size=100,
            micro_batch_size=10,
        )

        assert ctx.batch_size == 100
        assert ctx.micro_batch_size == 10
        assert ctx.num_micro_batches == 10

    def test_micro_batch_iteration(self):
        """Test iterating over micro-batches."""
        from src.core.base.logic.core.micro_batch_context import MicroBatchContext

        ctx = MicroBatchContext(batch_size=32, micro_batch_size=8)

        batches = []
        with ctx:
            for mb in ctx.iterate():
                batches.append(mb)
                ctx.record_output(f"output_{mb.batch_idx}")

        assert len(batches) == 4
        assert batches[0].start_idx == 0
        assert batches[0].end_idx == 8
        assert batches[3].start_idx == 24
        assert batches[3].end_idx == 32

    def test_output_gathering(self):
        """Test gathering outputs from micro-batches."""
        from src.core.base.logic.core.micro_batch_context import MicroBatchContext

        ctx = MicroBatchContext(batch_size=20, micro_batch_size=10)

        with ctx:
            for i, mb in enumerate(ctx.iterate()):
                ctx.record_output(f"result_{i}")

        outputs = ctx.gather_outputs()
        assert len(outputs) == 2
        assert outputs[0] == "result_0"
        assert outputs[1] == "result_1"

    def test_context_stats(self):
        """Test context statistics."""
        from src.core.base.logic.core.micro_batch_context import MicroBatchContext

        ctx = MicroBatchContext(batch_size=30, micro_batch_size=10)

        with ctx:
            for mb in ctx.iterate():
                ctx.record_output("done")

        stats = ctx.stats
        assert stats["batch_size"] == 30
        assert stats["num_micro_batches"] == 3
        assert stats["completed_micro_batches"] == 3
        assert stats["outputs_recorded"] == 3


class TestAdaptiveMicroBatchContext:
    """Tests for AdaptiveMicroBatchContext."""

    def test_adaptive_context(self):
        """Test adaptive micro-batch sizing."""
        from src.core.base.logic.core.micro_batch_context import AdaptiveMicroBatchContext

        ctx = AdaptiveMicroBatchContext(
            batch_size=100,
            initial_micro_batch=10,
            target_time_ms=5.0,
        )

        assert ctx.target_time_ms == 5.0


# =============================================================================
# CudaStreamPool Tests
# =============================================================================

class TestPooledStream:
    """Tests for PooledStream class."""

    def test_stream_creation(self):
        """Test pooled stream creation."""
        from src.core.base.logic.core.cuda_stream_pool import PooledStream, StreamPriority

        stream = PooledStream(
            stream_id=0,
            priority=StreamPriority.HIGH,
        )

        assert stream.stream_id == 0
        assert stream.priority == StreamPriority.HIGH

    def test_stream_query(self):
        """Test stream query (simulated)."""
        from src.core.base.logic.core.cuda_stream_pool import PooledStream

        stream = PooledStream(stream_id=0)

        # Without actual CUDA, query should return True
        assert stream.query() is True


class TestEventPool:
    """Tests for EventPool class."""

    def test_event_pool_creation(self):
        """Test event pool creation."""
        from src.core.base.logic.core.cuda_stream_pool import EventPool

        pool = EventPool(initial_size=8, max_size=64)

        assert pool.max_size == 64

    def test_event_acquire_release(self):
        """Test event acquisition and release."""
        from src.core.base.logic.core.cuda_stream_pool import EventPool

        pool = EventPool(initial_size=4)

        event1 = pool.acquire()
        assert event1 is not None
        assert event1.in_use is True

        pool.release(event1)
        assert event1.in_use is False


class TestCudaStreamPool:
    """Tests for CudaStreamPool class."""

    def test_pool_creation(self):
        """Test stream pool creation."""
        from src.core.base.logic.core.cuda_stream_pool import CudaStreamPool

        pool = CudaStreamPool(
            compute_streams=4,
            comm_streams=2,
            high_priority_streams=1,
        )

        assert pool.compute_streams_count == 4
        assert pool.comm_streams_count == 2

    def test_compute_stream_acquisition(self):
        """Test compute stream acquisition."""
        from src.core.base.logic.core.cuda_stream_pool import CudaStreamPool

        pool = CudaStreamPool(compute_streams=2)

        stream1 = pool.acquire_compute()
        stream2 = pool.acquire_compute()

        if stream1 is not None:
            assert stream1.stream_id != stream2.stream_id

            pool.release(stream1)
            pool.release(stream2)

    def test_stream_affinity(self):
        """Test stream affinity tracking."""
        from src.core.base.logic.core.cuda_stream_pool import CudaStreamPool

        pool = CudaStreamPool(compute_streams=2, enable_affinity=True)

        # First acquire with key
        stream1 = pool.acquire_compute(affinity_key="model_A")
        if stream1 is not None:
            stream_id = stream1.stream_id
            pool.release(stream1)

            # Second acquire with same key should get same stream
            stream2 = pool.acquire_compute(affinity_key="model_A")
            assert stream2.stream_id == stream_id
            pool.release(stream2)

    def test_pool_stats(self):
        """Test pool statistics."""
        from src.core.base.logic.core.cuda_stream_pool import CudaStreamPool

        pool = CudaStreamPool(compute_streams=2, comm_streams=1)

        stream = pool.acquire_compute()
        if stream:
            pool.release(stream)

        stats = pool.stats
        assert "compute" in stats
        assert "comm" in stats


# =============================================================================
# AdvancedRequestScheduler Tests
# =============================================================================

class TestScheduledRequest:
    """Tests for ScheduledRequest class."""

    def test_request_creation(self):
        """Test request creation."""
        from src.infrastructure.engine.scheduling.advanced_request_scheduler import (
            ScheduledRequest, RequestPriority, RequestState
        )

        request = ScheduledRequest(
            request_id="req1",
            prompt="Hello world",
            priority=RequestPriority.HIGH,
            max_tokens=100,
        )

        assert request.request_id == "req1"
        assert request.priority == RequestPriority.HIGH
        assert request.state == RequestState.WAITING

    def test_request_preemption(self):
        """Test request preemption."""
        from src.infrastructure.engine.scheduling.advanced_request_scheduler import (
            ScheduledRequest, RequestPriority, RequestState, PreemptionReason
        )

        request = ScheduledRequest(
            request_id="req1",
            prompt="Hello",
            priority=RequestPriority.NORMAL,
        )
        request.state = RequestState.RUNNING

        request.preempt(PreemptionReason.HIGHER_PRIORITY, state={"kv": "cache"})

        assert request.state == RequestState.PREEMPTED
        assert request.preemption_reason == PreemptionReason.HIGHER_PRIORITY
        assert request.saved_state == {"kv": "cache"}
        assert request.metrics.preemption_count == 1

    def test_request_resume(self):
        """Test request resumption."""
        from src.infrastructure.engine.scheduling.advanced_request_scheduler import (
            ScheduledRequest, PreemptionReason, RequestState
        )

        request = ScheduledRequest(request_id="req1", prompt="Test")
        request.state = RequestState.RUNNING  # Must be running to preempt
        request.preempt(PreemptionReason.MEMORY_PRESSURE, state="state_data")

        restored = request.resume()

        assert restored == "state_data"
        assert request.metrics.total_preemption_time > 0 or request.metrics.preemption_count == 1


class TestPriorityRequestQueue:
    """Tests for PriorityRequestQueue class."""

    def test_queue_push_pop(self):
        """Test basic queue operations."""
        from src.infrastructure.engine.scheduling.advanced_request_scheduler import (
            PriorityRequestQueue, ScheduledRequest, RequestPriority
        )

        queue = PriorityRequestQueue()

        req1 = ScheduledRequest("r1", "Prompt 1", RequestPriority.LOW)
        req2 = ScheduledRequest("r2", "Prompt 2", RequestPriority.HIGH)
        req3 = ScheduledRequest("r3", "Prompt 3", RequestPriority.NORMAL)

        queue.push(req1)
        queue.push(req2)
        queue.push(req3)

        assert len(queue) == 3

        # Should pop in priority order
        first = queue.pop()
        assert first.priority == RequestPriority.HIGH

    def test_queue_priority_ordering(self):
        """Test priority-based ordering."""
        from src.infrastructure.engine.scheduling.advanced_request_scheduler import (
            PriorityRequestQueue, ScheduledRequest, RequestPriority
        )

        queue = PriorityRequestQueue()

        # Add in reverse order
        for i, priority in enumerate([
            RequestPriority.BACKGROUND,
            RequestPriority.LOW,
            RequestPriority.NORMAL,
            RequestPriority.HIGH,
            RequestPriority.CRITICAL,
        ]):
            queue.push(ScheduledRequest(f"r{i}", f"P{i}", priority))

        # Pop should return in priority order
        order = []
        while queue:
            req = queue.pop()
            if req:
                order.append(req.priority)

        assert order[0] == RequestPriority.CRITICAL
        assert order[-1] == RequestPriority.BACKGROUND


class TestAdvancedRequestScheduler:
    """Tests for AdvancedRequestScheduler class."""

    def test_scheduler_creation(self):
        """Test scheduler creation."""
        from src.infrastructure.engine.scheduling.advanced_request_scheduler import (
            AdvancedRequestScheduler, SchedulerConfig
        )

        config = SchedulerConfig(
            max_running_requests=16,
            max_tokens_per_batch=2048,
        )
        scheduler = AdvancedRequestScheduler(config)

        assert scheduler.config.max_running_requests == 16

    def test_add_request(self):
        """Test adding requests."""
        from src.infrastructure.engine.scheduling.advanced_request_scheduler import (
            AdvancedRequestScheduler, RequestPriority
        )

        scheduler = AdvancedRequestScheduler()

        req = scheduler.add_request(
            prompt="Hello world",
            priority=RequestPriority.HIGH,
            max_tokens=50,
        )

        assert req.request_id is not None
        assert req.prompt == "Hello world"
        assert len(scheduler.waiting) == 1

    def test_schedule_batch(self):
        """Test scheduling a batch."""
        from src.infrastructure.engine.scheduling.advanced_request_scheduler import (
            AdvancedRequestScheduler, RequestPriority, SchedulerConfig
        )

        config = SchedulerConfig(max_running_requests=2, max_tokens_per_batch=1000)
        scheduler = AdvancedRequestScheduler(config)

        scheduler.add_request("Prompt 1", RequestPriority.NORMAL, max_tokens=10)
        scheduler.add_request("Prompt 2", RequestPriority.HIGH, max_tokens=10)
        scheduler.add_request("Prompt 3", RequestPriority.LOW, max_tokens=10)

        batch = scheduler.schedule()

        assert len(batch) == 2
        # High priority should be scheduled first
        assert batch[0].priority == RequestPriority.HIGH

    def test_complete_request(self):
        """Test completing a request."""
        from src.infrastructure.engine.scheduling.advanced_request_scheduler import (
            AdvancedRequestScheduler, RequestState
        )

        scheduler = AdvancedRequestScheduler()
        req = scheduler.add_request("Test", max_tokens=10)

        # Schedule it
        batch = scheduler.schedule()
        assert len(batch) == 1

        # Complete it
        success = scheduler.complete_request(req.request_id, generated_tokens=10)

        assert success is True
        assert req.state == RequestState.COMPLETED
        assert req.request_id in scheduler.completed

    def test_abort_request(self):
        """Test aborting a request."""
        from src.infrastructure.engine.scheduling.advanced_request_scheduler import (
            AdvancedRequestScheduler, RequestState
        )

        scheduler = AdvancedRequestScheduler()
        req = scheduler.add_request("Test")

        success = scheduler.abort_request(req.request_id)

        assert success is True
        assert req.state == RequestState.ABORTED

    def test_scheduler_stats(self):
        """Test scheduler statistics."""
        from src.infrastructure.engine.scheduling.advanced_request_scheduler import (
            AdvancedRequestScheduler
        )

        scheduler = AdvancedRequestScheduler()
        scheduler.add_request("Test 1")
        scheduler.add_request("Test 2")

        stats = scheduler.stats
        assert stats["waiting"] == 2
        assert stats["running"] == 0


# =============================================================================
# ChunkedPrefillManager Tests
# =============================================================================

class TestPrefillChunk:
    """Tests for PrefillChunk class."""

    def test_chunk_creation(self):
        """Test chunk creation."""
        from src.infrastructure.engine.scheduling.chunked_prefill_manager import (
            PrefillChunk, ChunkState
        )

        chunk = PrefillChunk(
            chunk_id="req1_chunk_0",
            request_id="req1",
            chunk_index=0,
            start_idx=0,
            end_idx=100,
            tokens=list(range(100)),
        )

        assert chunk.chunk_id == "req1_chunk_0"
        assert chunk.size == 100
        assert chunk.is_first is True
        assert chunk.state == ChunkState.PENDING


class TestChunkedPrefillManager:
    """Tests for ChunkedPrefillManager class."""

    def test_manager_creation(self):
        """Test manager creation."""
        from src.infrastructure.engine.scheduling.chunked_prefill_manager import (
            ChunkedPrefillManager, ChunkedPrefillConfig
        )

        config = ChunkedPrefillConfig(
            default_chunk_size=256,
            long_prompt_threshold=128,
        )
        manager = ChunkedPrefillManager(config)

        assert manager.config.default_chunk_size == 256

    def test_should_chunk(self):
        """Test chunking decision."""
        from src.infrastructure.engine.scheduling.chunked_prefill_manager import (
            ChunkedPrefillManager, ChunkedPrefillConfig
        )

        config = ChunkedPrefillConfig(long_prompt_threshold=100)
        manager = ChunkedPrefillManager(config)

        assert manager.should_chunk(50) is False
        assert manager.should_chunk(150) is True

    def test_compute_boundaries(self):
        """Test chunk boundary computation."""
        from src.infrastructure.engine.scheduling.chunked_prefill_manager import (
            ChunkedPrefillManager, ChunkedPrefillConfig
        )

        config = ChunkedPrefillConfig(default_chunk_size=100)
        manager = ChunkedPrefillManager(config)

        boundaries = manager.compute_chunk_boundaries(250)

        assert len(boundaries) == 3
        assert boundaries[0] == (0, 100)
        assert boundaries[1] == (100, 200)
        assert boundaries[2] == (200, 250)

    def test_create_chunks(self):
        """Test chunk creation."""
        from src.infrastructure.engine.scheduling.chunked_prefill_manager import (
            ChunkedPrefillManager
        )

        manager = ChunkedPrefillManager()
        tokens = list(range(1000))

        chunks = manager.create_chunks(
            request_id="req1",
            prompt_tokens=tokens,
            chunk_size=256,
        )

        assert len(chunks) == 4  # 1000 / 256 = ~4 chunks
        assert chunks[0].chunk_index == 0
        assert chunks[0].is_first is True

    def test_schedule_chunks(self):
        """Test chunk scheduling."""
        from src.infrastructure.engine.scheduling.chunked_prefill_manager import (
            ChunkedPrefillManager, ChunkState
        )

        manager = ChunkedPrefillManager()
        tokens = list(range(500))

        manager.create_chunks("req1", tokens, chunk_size=200)

        # Schedule first chunk
        chunk1 = manager.schedule_chunk()
        assert chunk1 is not None
        assert chunk1.chunk_index == 0
        assert chunk1.state == ChunkState.SCHEDULED

        # Complete first chunk
        manager.start_chunk(chunk1.chunk_id)
        manager.complete_chunk(chunk1.chunk_id, output=[1, 2, 3])

        # Schedule second chunk
        chunk2 = manager.schedule_chunk()
        assert chunk2 is not None
        assert chunk2.chunk_index == 1

    def test_chunk_dependencies(self):
        """Test chunk dependency handling."""
        from src.infrastructure.engine.scheduling.chunked_prefill_manager import (
            ChunkedPrefillManager
        )

        manager = ChunkedPrefillManager()
        tokens = list(range(600))

        chunks = manager.create_chunks("req1", tokens, chunk_size=200)

        # Chunks should have dependencies
        assert chunks[1].depends_on == chunks[0].chunk_id
        assert chunks[2].depends_on == chunks[1].chunk_id

    def test_merge_chunks(self):
        """Test merging chunk outputs."""
        from src.infrastructure.engine.scheduling.chunked_prefill_manager import (
            ChunkedPrefillManager
        )

        manager = ChunkedPrefillManager()
        tokens = list(range(300))

        chunks = manager.create_chunks("req1", tokens, chunk_size=100)

        # Complete all chunks with list outputs
        for chunk in chunks:
            manager.start_chunk(chunk.chunk_id)
            manager.complete_chunk(
                chunk.chunk_id,
                output=[f"out_{chunk.chunk_index}"],
            )

        merged = manager.merge_chunks("req1")

        assert merged == ["out_0", "out_1", "out_2"]

    def test_manager_stats(self):
        """Test manager statistics."""
        from src.infrastructure.engine.scheduling.chunked_prefill_manager import (
            ChunkedPrefillManager
        )

        manager = ChunkedPrefillManager()
        tokens = list(range(200))

        chunks = manager.create_chunks("req1", tokens, chunk_size=100)
        for chunk in chunks:
            manager.start_chunk(chunk.chunk_id)
            manager.complete_chunk(chunk.chunk_id)

        stats = manager.stats
        assert stats["total_chunks_created"] == 2
        assert stats["total_chunks_completed"] == 2


# =============================================================================
# Rust Acceleration Tests
# =============================================================================

class TestPhase32RustAccelerations:
    """Tests for Phase 32 Rust accelerations."""

    @pytest.fixture
    def rust_bridge(self):
        """Get Rust bridge if available."""
        try:
            from src.core.rust_bridge import get_bridge
            return get_bridge()
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            pytest.skip("Rust bridge not available")

    def test_uva_copy_rust(self, rust_bridge):
        """Test UVA copy function."""
        if not hasattr(rust_bridge, 'uva_copy_rust'):
            pytest.skip("uva_copy_rust not available")

        pairs = rust_bridge.uva_copy_rust(0, 100, 40, 4)

        assert len(pairs) == 10
        assert pairs[0] == (0, 100)
        assert pairs[1] == (4, 104)

    def test_batch_write_indices_rust(self, rust_bridge):
        """Test batch write index optimization."""
        if not hasattr(rust_bridge, 'batch_write_indices_rust'):
            pytest.skip("batch_write_indices_rust not available")

        indices = [100, 10, 50, 11, 12, 51]
        sorted_indices = rust_bridge.batch_write_indices_rust(indices, 32)

        # Should be sorted by block then offset
        assert sorted_indices[0] == 10
        assert sorted_indices[1] == 11
        assert sorted_indices[2] == 12

    def test_coalesce_writes_rust(self, rust_bridge):
        """Test write coalescing."""
        if not hasattr(rust_bridge, 'coalesce_writes_rust'):
            pytest.skip("coalesce_writes_rust not available")

        indices = [10, 11, 12, 50, 51]
        values = [1.0, 2.0, 3.0, 4.0, 5.0]

        coalesced = rust_bridge.coalesce_writes_rust(indices, values, 4)

        # Should have 2 ranges: 10-12 and 50-51
        assert len(coalesced) == 2

    def test_priority_heap_ops_rust(self, rust_bridge):
        """Test priority heap operations."""
        if not hasattr(rust_bridge, 'priority_heap_ops_rust'):
            pytest.skip("priority_heap_ops_rust not available")

        # (priority, deadline, sequence)
        priorities = [
            (2.0, 100.0, 1),
            (1.0, 50.0, 2),
            (3.0, 200.0, 3),
            (1.0, 60.0, 4),
        ]

        order = rust_bridge.priority_heap_ops_rust(priorities)

        # Should be sorted by priority, then deadline
        assert order[0] == 1  # priority=1, deadline=50
        assert order[1] == 3  # priority=1, deadline=60

    def test_token_budget_check_rust(self, rust_bridge):
        """Test token budget checking."""
        if not hasattr(rust_bridge, 'token_budget_check_rust'):
            pytest.skip("token_budget_check_rust not available")

        request_tokens = [100, 200, 150, 300, 50]
        budget = 400
        max_requests = 3

        selected = rust_bridge.token_budget_check_rust(request_tokens, budget, max_requests)

        # Should select requests that fit in budget
        total = sum(request_tokens[i] for i in selected)
        assert total <= budget
        assert len(selected) <= max_requests

    def test_chunk_boundaries_rust(self, rust_bridge):
        """Test chunk boundary computation."""
        if not hasattr(rust_bridge, 'chunk_boundaries_rust'):
            pytest.skip("chunk_boundaries_rust not available")

        boundaries = rust_bridge.chunk_boundaries_rust(1000, 256, 0.0)

        assert len(boundaries) == 4
        assert boundaries[0] == (0, 256)
        assert boundaries[3] == (768, 1000)

    def test_chunk_boundaries_with_pressure(self, rust_bridge):
        """Test chunk boundaries under memory pressure."""
        if not hasattr(rust_bridge, 'chunk_boundaries_rust'):
            pytest.skip("chunk_boundaries_rust not available")

        # With pressure, chunks should be smaller
        normal = rust_bridge.chunk_boundaries_rust(1000, 256, 0.0)
        pressure = rust_bridge.chunk_boundaries_rust(1000, 256, 0.5)

        # More chunks under pressure (smaller chunks)
        assert len(pressure) >= len(normal)

    def test_stream_sync_rust(self, rust_bridge):
        """Test stream sync check."""
        if not hasattr(rust_bridge, 'stream_sync_rust'):
            pytest.skip("stream_sync_rust not available")

        assert rust_bridge.stream_sync_rust([True, True, True]) is True
        assert rust_bridge.stream_sync_rust([True, False, True]) is False

    def test_event_query_rust(self, rust_bridge):
        """Test event query."""
        if not hasattr(rust_bridge, 'event_query_rust'):
            pytest.skip("event_query_rust not available")

        states = [True, False, True, True, False]
        completed = rust_bridge.event_query_rust(states)

        assert completed == [0, 2, 3]

    def test_preemption_score_rust(self, rust_bridge):
        """Test preemption score calculation."""
        if not hasattr(rust_bridge, 'preemption_score_rust'):
            pytest.skip("preemption_score_rust not available")

        # Lower priority, less progress = easier to preempt (higher score)
        score_low = rust_bridge.preemption_score_rust(3, 10, 100, 5.0)  # Low priority, 10% done
        score_high = rust_bridge.preemption_score_rust(1, 90, 100, 1.0)  # High priority, 90% done

        # Lower priority request should have higher preemption score
        assert score_low > score_high

    def test_deadline_check_rust(self, rust_bridge):
        """Test deadline checking."""
        if not hasattr(rust_bridge, 'deadline_check_rust'):
            pytest.skip("deadline_check_rust not available")

        current_time = 100.0
        deadlines = [99.0, 100.5, 102.0, -1.0, 95.0]  # -1 = no deadline

        missed, urgent = rust_bridge.deadline_check_rust(deadlines, current_time, 1.0)

        assert 0 in missed  # 99 < 100 (missed)
        assert 4 in missed  # 95 < 100 (missed)
        assert 1 in urgent  # 100.5 - 100 = 0.5 < 1.0 (urgent)


# =============================================================================
# Integration Tests
# =============================================================================

class TestPhase32Integration:
    """Integration tests for Phase 32 components."""

    def test_scheduler_with_chunked_prefill(self):
        """Test scheduler integration with chunked prefill."""
        from src.infrastructure.engine.scheduling.advanced_request_scheduler import (
            AdvancedRequestScheduler, RequestPriority
        )
        from src.infrastructure.engine.scheduling.chunked_prefill_manager import (
            ChunkedPrefillManager, ChunkedPrefillConfig
        )

        scheduler = AdvancedRequestScheduler()
        # Use smaller chunk size to ensure multiple chunks
        config = ChunkedPrefillConfig(default_chunk_size=256, min_chunk_size=128)
        prefill_manager = ChunkedPrefillManager(config)

        # Add a request with long prompt (1000 tokens = 4 chunks with chunk_size=256)
        req = scheduler.add_request(
            prompt="A" * 5000,  # Long prompt
            priority=RequestPriority.NORMAL,
            prompt_tokens=1000,  # 1000 tokens > 256 chunk_size
        )

        # Create chunks if needed
        if prefill_manager.should_chunk(req.prompt_tokens):
            chunks = prefill_manager.create_chunks(
                request_id=req.request_id,
                prompt_tokens=list(range(req.prompt_tokens)),
            )

            assert len(chunks) > 1  # Should have at least 4 chunks

    def test_concurrent_buffer_pool(self):
        """Test concurrent access to buffer pool."""
        from src.core.base.logic.structures.uva_buffer_pool import UvaBufferPool

        pool = UvaBufferPool(buffer_count=4, buffer_size=1024)
        acquired = []
        errors = []

        def acquire_and_release():
            try:
                buffer = pool.acquire(timeout=1.0)
                if buffer:
                    acquired.append(buffer.buffer_id)
                    time.sleep(0.01)
                    pool.release(buffer)
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                errors.append(str(e))

        threads = [threading.Thread(target=acquire_and_release) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0
        assert len(acquired) == 8


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
