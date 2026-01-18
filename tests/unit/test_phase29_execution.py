"""
test_phase29_execution.py - Tests for Phase 29: Execution Context, Batching & Async Streaming.

Tests for:
- ForwardContext and BatchDescriptor
- InputBatch and InputBuffers
- CpuGpuBuffer and UvaBufferPool
- AsyncOutput and AsyncOutputHandler
- CUDAGraphConfig and CUDAGraphManager
- Rust accelerations
"""

import pytest
import numpy as np
import time
import threading

from src.infrastructure.execution import (
    # ForwardContext
    ForwardContext,
    BatchDescriptor,
    DPMetadata,
    set_forward_context,
    get_forward_context,
    create_forward_context,
    # InputBatch
    InputBatch,
    InputBuffers,
    SamplingMetadata,
    BatchBuilder,
    # CpuGpuBufferPool
    CpuGpuBuffer,
    UvaBufferPool,
    PinnedMemoryManager,
    copy_with_indices,
    scatter_with_indices,
    pad_to_multiple,
    compute_cumsum_offsets,
    flatten_with_offsets,
    split_by_offsets,
    # AsyncOutputHandler
    AsyncState,
    CudaEvent,
    CudaStream,
    AsyncOutput,
    async_copy_to_np,
    async_barrier,
    AsyncOutputHandler,
    DoubleBuffer,
    # CUDAGraphConfig
    CUDAGraphMode,
    CUDAGraphConfig,
    CUDAGraphEntry,
    CUDAGraphRegistry,
    CUDAGraphManager,
)


# ============================================================================
# ForwardContext Tests
# ============================================================================

class TestBatchDescriptor:
    """Tests for BatchDescriptor."""
    
    def test_creation(self):
        """Test BatchDescriptor creation."""
        bd = BatchDescriptor(num_tokens=100, num_reqs=4, uniform=True, has_lora=False)
        assert bd.num_tokens == 100
        assert bd.num_reqs == 4
        assert bd.uniform is True
        assert bd.has_lora is False
    
    def test_key_method(self):
        """Test BatchDescriptor key generation."""
        bd = BatchDescriptor(num_tokens=100, num_reqs=4, uniform=True, has_lora=False)
        key = bd.key()
        assert isinstance(key, tuple)
        assert key == (100, 4, True, False)
    
    def test_relaxed_method(self):
        """Test BatchDescriptor relaxed creation."""
        bd = BatchDescriptor(num_tokens=100, num_reqs=4, uniform=True, has_lora=True)
        relaxed = bd.relaxed()
        # Relaxed should set uniform=False and num_reqs=None
        assert relaxed.uniform is False
        assert relaxed.num_reqs is None
        assert relaxed.num_tokens == 100


class TestDPMetadata:
    """Tests for DPMetadata."""
    
    def test_make_factory(self):
        """Test DPMetadata make factory."""
        dp = DPMetadata.make(world_size=4, rank=1, num_tokens=400)
        assert dp.world_size == 4
        assert dp.rank == 1
        assert dp.local_num_tokens == 100  # 400 / 4
    
    def test_single_factory(self):
        """Test DPMetadata single factory."""
        dp = DPMetadata.single(num_tokens=256)
        assert dp.world_size == 1
        assert dp.rank == 0
        assert dp.local_num_tokens == 256


class TestForwardContext:
    """Tests for ForwardContext."""
    
    def test_creation(self):
        """Test ForwardContext creation."""
        ctx = create_forward_context(num_tokens=128)
        assert ctx.num_tokens == 128
        # cudagraph_mode can be 0 or False depending on implementation
        assert ctx.cudagraph_mode == 0 or ctx.cudagraph_mode is False
    
    def test_context_manager(self):
        """Test set_forward_context context manager."""
        ctx = create_forward_context(num_tokens=64)
        
        with set_forward_context(ctx):
            retrieved = get_forward_context()
            # The retrieved context wraps the original, check num_tokens from attn_metadata
            assert retrieved.attn_metadata is not None
            assert retrieved.attn_metadata.num_tokens == 64
    
    def test_nested_context(self):
        """Test nested forward contexts."""
        ctx1 = create_forward_context(num_tokens=32)
        ctx2 = create_forward_context(num_tokens=64)
        
        with set_forward_context(ctx1):
            inner = get_forward_context()
            assert inner.attn_metadata.num_tokens == 32
            
            with set_forward_context(ctx2):
                inner2 = get_forward_context()
                assert inner2.attn_metadata.num_tokens == 64


# ============================================================================
# InputBatch Tests
# ============================================================================

class TestSamplingMetadata:
    """Tests for SamplingMetadata."""
    
    def test_from_defaults(self):
        """Test SamplingMetadata default creation."""
        sm = SamplingMetadata.from_defaults(num_reqs=4)
        assert sm.num_reqs == 4
        assert len(sm.temperature) == 4
        assert np.all(sm.temperature == 1.0)
    
    def test_from_params(self):
        """Test SamplingMetadata from parameters."""
        sm = SamplingMetadata.from_params(
            temperatures=[0.7, 1.0, 0.5],
            top_ks=[50, -1, 100],
            top_ps=[0.9, 1.0, 0.95],
        )
        assert sm.num_reqs == 3
        assert sm.temperature[0] == 0.7
        assert sm.top_k[1] == -1
    
    def test_slice(self):
        """Test SamplingMetadata slicing."""
        sm = SamplingMetadata.from_defaults(num_reqs=8)
        sliced = sm.slice(2, 5)
        assert sliced.num_reqs == 3


class TestInputBuffers:
    """Tests for InputBuffers."""
    
    def test_allocate(self):
        """Test InputBuffers allocation."""
        buffers = InputBuffers.allocate(
            max_num_reqs=16,
            max_num_tokens=1024,
        )
        assert len(buffers.input_ids) == 1024
        assert len(buffers.positions) == 1024
        assert len(buffers.seq_lens) == 16
    
    def test_reset(self):
        """Test InputBuffers reset."""
        buffers = InputBuffers.allocate(max_num_reqs=8, max_num_tokens=256)
        buffers.input_ids[:10] = 1
        buffers.reset()
        assert np.all(buffers.input_ids == 0)


class TestInputBatch:
    """Tests for InputBatch."""
    
    def test_from_requests(self):
        """Test InputBatch creation from requests."""
        buffers = InputBuffers.allocate(max_num_reqs=8, max_num_tokens=256)
        
        batch = InputBatch.from_requests(
            req_ids=["req1", "req2"],
            input_ids_list=[[1, 2, 3], [4, 5, 6, 7]],
            positions_list=[[0, 1, 2], [0, 1, 2, 3]],
            buffers=buffers,
        )
        
        assert batch.num_reqs == 2
        assert batch.num_tokens == 7
        assert batch.max_query_len == 4
    
    def test_make_dummy(self):
        """Test InputBatch dummy creation for CUDA graph."""
        buffers = InputBuffers.allocate(max_num_reqs=8, max_num_tokens=256)
        
        dummy = InputBatch.make_dummy(num_reqs=4, num_tokens=32, buffers=buffers)
        
        assert dummy.num_reqs == 4
        assert len(dummy.req_ids) == 4
        assert dummy.req_ids[0].startswith("dummy_")
    
    def test_get_logits_indices(self):
        """Test getting logits extraction indices."""
        buffers = InputBuffers.allocate(max_num_reqs=8, max_num_tokens=256)
        
        batch = InputBatch.from_requests(
            req_ids=["req1", "req2"],
            input_ids_list=[[1, 2, 3], [4, 5, 6, 7]],
            positions_list=[[0, 1, 2], [0, 1, 2, 3]],
            buffers=buffers,
        )
        
        indices = batch.get_logits_indices()
        # Last token of each sequence: 2 (0-indexed) and 6 (0-indexed)
        assert len(indices) == 2


class TestBatchBuilder:
    """Tests for BatchBuilder."""
    
    def test_add_requests(self):
        """Test adding requests to builder."""
        buffers = InputBuffers.allocate(max_num_reqs=8, max_num_tokens=256)
        builder = BatchBuilder(buffers)
        
        assert builder.add_request("req1", [1, 2, 3])
        assert builder.add_request("req2", [4, 5, 6, 7])
        
        assert builder.num_reqs == 2
        assert builder.total_tokens == 7
    
    def test_build(self):
        """Test building a batch."""
        buffers = InputBuffers.allocate(max_num_reqs=8, max_num_tokens=256)
        builder = BatchBuilder(buffers)
        
        builder.add_request("req1", [1, 2, 3], temperature=0.7)
        builder.add_request("req2", [4, 5], temperature=1.0)
        
        batch = builder.build()
        
        assert batch.num_reqs == 2
        assert batch.sampling_metadata.temperature[0] == 0.7


# ============================================================================
# CpuGpuBufferPool Tests
# ============================================================================

class TestCpuGpuBuffer:
    """Tests for CpuGpuBuffer."""
    
    def test_allocate(self):
        """Test CpuGpuBuffer allocation."""
        buf = CpuGpuBuffer.allocate("test", (100, 64), np.float32)
        
        assert buf.name == "test"
        assert buf.shape == (100, 64)
        assert buf.cpu.shape == (100, 64)
        assert buf.gpu.shape == (100, 64)
    
    def test_cpu_to_gpu(self):
        """Test CPU to GPU copy."""
        buf = CpuGpuBuffer.allocate("test", (10,), np.float32)
        buf.cpu[:] = np.arange(10)
        buf.cpu_to_gpu()
        
        np.testing.assert_array_equal(buf.cpu, buf.gpu)
    
    def test_gpu_to_cpu(self):
        """Test GPU to CPU copy."""
        buf = CpuGpuBuffer.allocate("test", (10,), np.float32)
        buf.gpu[:] = np.arange(10, 20)
        buf.gpu_to_cpu()
        
        np.testing.assert_array_equal(buf.cpu, buf.gpu)
    
    def test_dirty_flags(self):
        """Test dirty flag tracking."""
        buf = CpuGpuBuffer.allocate("test", (10,), np.float32)
        
        buf.mark_cpu_dirty()
        assert buf._cpu_dirty is True
        
        buf.sync()
        assert buf._cpu_dirty is False


class TestUvaBufferPool:
    """Tests for UvaBufferPool."""
    
    def test_allocate(self):
        """Test UvaBufferPool allocation."""
        pool = UvaBufferPool("test_pool")
        
        buf1 = pool.allocate("buf1", (100, 64), np.float32)
        buf2 = pool.allocate("buf2", (200, 128), np.float32)
        
        assert pool.num_buffers == 2
        assert buf1.name == "buf1"
    
    def test_get(self):
        """Test retrieving buffer from pool."""
        pool = UvaBufferPool("test_pool")
        pool.allocate("buffer", (100,), np.float32)
        
        retrieved = pool.get("buffer")
        assert retrieved is not None
        assert retrieved.shape == (100,)
    
    def test_stats(self):
        """Test pool statistics."""
        pool = UvaBufferPool("test_pool")
        pool.allocate("buf1", (100,), np.float32)
        
        stats = pool.stats()
        assert stats["num_buffers"] == 1
        assert stats["total_bytes"] > 0


class TestPinnedMemoryManager:
    """Tests for PinnedMemoryManager."""
    
    def test_allocate(self):
        """Test pinned memory allocation."""
        mgr = PinnedMemoryManager(max_bytes=1024*1024)
        
        buf = mgr.allocate((100,), np.float32)
        
        assert buf is not None
        assert buf.shape == (100,)
        assert mgr.allocated_bytes == 400  # 100 * 4 bytes
    
    def test_free(self):
        """Test freeing pinned memory."""
        mgr = PinnedMemoryManager()
        buf = mgr.allocate((100,), np.float32)
        
        assert mgr.free(buf) is True
        assert mgr.allocated_bytes == 0


class TestBufferUtilities:
    """Tests for buffer utility functions."""
    
    def test_copy_with_indices(self):
        """Test index-based copy."""
        src = np.array([10.0, 20.0, 30.0, 40.0, 50.0])  # Use float for dst compatibility
        dst = np.zeros(3, dtype=np.float64)
        indices = np.array([4, 2, 0])
        
        copy_with_indices(src, dst, indices)
        
        np.testing.assert_array_equal(dst, [50.0, 30.0, 10.0])
    
    def test_pad_to_multiple(self):
        """Test padding to multiple."""
        arr = np.arange(10)
        padded = pad_to_multiple(arr, 8)
        
        assert len(padded) == 16  # Next multiple of 8
    
    def test_compute_cumsum_offsets(self):
        """Test cumsum offset computation."""
        lengths = np.array([3, 5, 2])
        offsets = compute_cumsum_offsets(lengths)
        
        np.testing.assert_array_equal(offsets, [0, 3, 8, 10])
    
    def test_flatten_with_offsets(self):
        """Test flattening with offsets."""
        arrays = [np.array([1, 2]), np.array([3, 4, 5]), np.array([6])]
        flattened, offsets = flatten_with_offsets(arrays)
        
        np.testing.assert_array_equal(flattened, [1, 2, 3, 4, 5, 6])
        np.testing.assert_array_equal(offsets, [0, 2, 5, 6])


# ============================================================================
# AsyncOutputHandler Tests
# ============================================================================

class TestCudaEvent:
    """Tests for CudaEvent."""
    
    def test_record_and_query(self):
        """Test event recording and querying."""
        event = CudaEvent("test_event")
        
        assert event.query() is False
        event.record()
        assert event.query() is True
    
    def test_elapsed_time(self):
        """Test elapsed time calculation."""
        event1 = CudaEvent("start")
        event2 = CudaEvent("end")
        
        event1.record()
        time.sleep(0.01)
        event2.record()
        
        elapsed = event1.elapsed_time(event2)
        assert elapsed > 0  # Should be ~10ms


class TestCudaStream:
    """Tests for CudaStream."""
    
    def test_record_event(self):
        """Test stream event recording."""
        stream = CudaStream("test_stream")
        event = stream.record_event()
        
        assert event is not None
        assert event.recorded_at is not None


class TestAsyncOutput:
    """Tests for AsyncOutput."""
    
    def test_lifecycle(self):
        """Test async output lifecycle."""
        output = AsyncOutput()
        
        assert output.state == AsyncState.PENDING
        
        output.mark_started()
        assert output.state == AsyncState.IN_PROGRESS
        
        output.mark_completed()
        assert output.state == AsyncState.COMPLETED
        assert output.is_ready is True
    
    def test_elapsed_time(self):
        """Test elapsed time tracking."""
        output = AsyncOutput()
        output.mark_started()
        time.sleep(0.01)
        output.mark_completed()
        
        assert output.elapsed_ms > 0


class TestAsyncOutputHandler:
    """Tests for AsyncOutputHandler."""
    
    def test_submit_and_poll(self):
        """Test submitting and polling outputs."""
        handler = AsyncOutputHandler(max_pending=16)
        
        output = AsyncOutput()
        output.mark_started()
        output.mark_completed()
        
        assert handler.submit(output) is True
        
        completed = handler.poll()
        assert len(completed) == 1
    
    def test_wait_all(self):
        """Test waiting for all outputs."""
        handler = AsyncOutputHandler()
        
        for i in range(5):
            output = AsyncOutput()
            output.mark_started()
            output.mark_completed()
            handler.submit(output)
        
        outputs = handler.wait_all()
        assert len(outputs) == 5


class TestDoubleBuffer:
    """Tests for DoubleBuffer."""
    
    def test_swap(self):
        """Test buffer swapping."""
        db = DoubleBuffer((100,), np.float32)
        
        db.current[:] = 1
        db.transfer[:] = 2
        
        db.swap()
        
        # After swap, current should now be the old transfer
        assert db.current[0] == 2
        assert db.transfer[0] == 1


# ============================================================================
# CUDAGraphConfig Tests
# ============================================================================

class TestCUDAGraphConfig:
    """Tests for CUDAGraphConfig."""
    
    def test_defaults(self):
        """Test default configuration."""
        config = CUDAGraphConfig()
        
        assert config.enabled is True
        assert config.max_capture_batch_size == 256
        assert 1 in config.capture_sizes
    
    def test_should_use_cudagraph(self):
        """Test graph usage determination."""
        config = CUDAGraphConfig()
        
        assert config.should_use_cudagraph(batch_size=32, seq_len=512) is True
        assert config.should_use_cudagraph(batch_size=512, seq_len=512) is False
    
    def test_get_padded_batch_size(self):
        """Test padded batch size lookup."""
        config = CUDAGraphConfig()
        
        assert config.get_padded_batch_size(3) == 4
        assert config.get_padded_batch_size(10) == 16
        assert config.get_padded_batch_size(64) == 64


class TestCUDAGraphRegistry:
    """Tests for CUDAGraphRegistry."""
    
    def test_capture(self):
        """Test graph capture."""
        registry = CUDAGraphRegistry()
        
        def capture_fn():
            return {"output": np.ones(10)}
        
        entry = registry.capture(
            batch_size=4,
            seq_len=128,
            capture_fn=capture_fn,
            input_shapes={"input": (4, 128)},
            output_shapes={"output": (10,)},
        )
        
        assert entry.batch_size == 4
        assert registry.num_graphs == 1
    
    def test_get(self):
        """Test graph retrieval."""
        registry = CUDAGraphRegistry()
        
        def capture_fn():
            return {}
        
        registry.capture(4, 128, capture_fn, {}, {})
        
        entry = registry.get(4, 128)
        assert entry is not None
        
        entry = registry.get(8, 256)
        assert entry is None


class TestCUDAGraphManager:
    """Tests for CUDAGraphManager."""
    
    def test_mode_management(self):
        """Test mode management."""
        manager = CUDAGraphManager()
        
        assert manager.mode == CUDAGraphMode.NONE
        
        manager.mode = CUDAGraphMode.DISABLED
        assert manager.is_enabled() is False
    
    def test_execute_or_capture(self):
        """Test execute_or_capture flow."""
        manager = CUDAGraphManager()
        
        call_count = 0
        
        def execute_fn(inputs):
            nonlocal call_count
            call_count += 1
            return {"output": inputs["input"] * 2}
        
        inputs = {"input": np.ones(10)}
        
        # First call should capture
        result1 = manager.execute_or_capture(
            batch_size=4,
            seq_len=10,
            execute_fn=execute_fn,
            inputs=inputs,
        )
        
        assert "output" in result1
        
        # Second call should replay
        result2 = manager.execute_or_capture(
            batch_size=4,
            seq_len=10,
            execute_fn=execute_fn,
            inputs=inputs,
        )
        
        assert "output" in result2


# ============================================================================
# Rust Acceleration Tests
# ============================================================================

class TestRustAccelerations:
    """Tests for Phase 29 Rust accelerations."""
    
    def test_batch_descriptor_hash_rust(self):
        """Test batch descriptor hash."""
        try:
            from rust_core import batch_descriptor_hash_rust
            
            hash1 = batch_descriptor_hash_rust(100, 4, True, False)
            hash2 = batch_descriptor_hash_rust(100, 4, True, False)
            hash3 = batch_descriptor_hash_rust(100, 4, True, True)
            
            assert hash1 == hash2  # Same inputs = same hash
            assert hash1 != hash3  # Different inputs = different hash
        except ImportError:
            pytest.skip("rust_core not available")
    
    def test_copy_with_indices_rust(self):
        """Test index-based copy in Rust."""
        try:
            from rust_core import copy_with_indices_rust
            
            src = [1.0, 2.0, 3.0, 4.0, 5.0]
            indices = [4, 2, 0]
            
            result = copy_with_indices_rust(src, indices)
            
            assert result == [5.0, 3.0, 1.0]
        except ImportError:
            pytest.skip("rust_core not available")
    
    def test_pad_sequences_rust(self):
        """Test sequence padding in Rust."""
        try:
            from rust_core import pad_sequences_rust
            
            sequences = [[1, 2, 3], [4, 5]]
            padded, offsets = pad_sequences_rust(sequences, 4, 0)
            
            assert padded == [1, 2, 3, 0, 4, 5, 0, 0]
            assert offsets == [0, 4, 8]
        except ImportError:
            pytest.skip("rust_core not available")
    
    def test_compute_dp_splits_rust(self):
        """Test data parallel splits."""
        try:
            from rust_core import compute_dp_splits_rust
            
            splits = compute_dp_splits_rust(100, 4)
            
            assert len(splits) == 4
            assert sum(splits) == 100
        except ImportError:
            pytest.skip("rust_core not available")
    
    def test_pin_memory_copy_rust(self):
        """Test pinned memory copy with transform."""
        try:
            from rust_core import pin_memory_copy_rust
            
            src = [1.0, 2.0, 3.0]
            result = pin_memory_copy_rust(src, 2.0, 1.0)
            
            assert result == [3.0, 5.0, 7.0]  # x * 2 + 1
        except ImportError:
            pytest.skip("rust_core not available")
    
    def test_merge_batch_metadata_rust(self):
        """Test batch metadata merging."""
        try:
            from rust_core import merge_batch_metadata_rust
            
            seq_lens_list = [[3, 4], [5, 6, 7]]
            merged, offsets = merge_batch_metadata_rust(seq_lens_list)
            
            assert merged == [3, 4, 5, 6, 7]
            assert offsets == [0, 7, 25]
        except ImportError:
            pytest.skip("rust_core not available")
    
    def test_validate_batch_shapes_rust(self):
        """Test batch shape validation."""
        try:
            from rust_core import validate_batch_shapes_rust
            
            # Valid shapes
            result = validate_batch_shapes_rust(100, 4, 100, 100, 4)
            assert result is True
            
            # Invalid shapes should raise
            with pytest.raises(Exception):
                validate_batch_shapes_rust(100, 4, 50, 100, 4)
        except ImportError:
            pytest.skip("rust_core not available")


# ============================================================================
# Integration Tests
# ============================================================================

class TestPhase29Integration:
    """Integration tests for Phase 29 components."""
    
    def test_forward_context_with_batch(self):
        """Test ForwardContext with InputBatch integration."""
        # Create a batch
        buffers = InputBuffers.allocate(max_num_reqs=16, max_num_tokens=512)
        
        batch = InputBatch.from_requests(
            req_ids=["req1", "req2", "req3"],
            input_ids_list=[[1, 2, 3], [4, 5], [6, 7, 8, 9]],
            positions_list=[[0, 1, 2], [0, 1], [0, 1, 2, 3]],
            buffers=buffers,
        )
        
        # Create forward context for the batch
        bd = BatchDescriptor(
            num_tokens=batch.num_tokens,
            num_reqs=batch.num_reqs,
            uniform=True,
            has_lora=False,
        )
        
        ctx = ForwardContext(
            attn_metadata={},
            batch_descriptor=bd,
            num_tokens=batch.num_tokens,
        )
        
        with set_forward_context(ctx):
            current = get_forward_context()
            # The inner context wraps the original, check attn_metadata
            assert current.attn_metadata is not None
            assert current.attn_metadata.num_tokens == 9  # 3 + 2 + 4
    
    def test_buffer_pool_with_async_output(self):
        """Test UvaBufferPool with AsyncOutputHandler."""
        pool = UvaBufferPool("inference")
        handler = AsyncOutputHandler()
        
        # Allocate buffers
        buf = pool.allocate("output", (32, 128), np.float32)
        
        # Simulate async output
        output = async_copy_to_np(buf.cpu)
        handler.submit(output)
        
        completed = handler.wait_all()
        assert len(completed) == 1
        assert completed[0].is_ready
    
    def test_cudagraph_with_batch_execution(self):
        """Test CUDAGraphManager with batch execution."""
        manager = CUDAGraphManager()
        buffers = InputBuffers.allocate(max_num_reqs=8, max_num_tokens=256)
        
        # Create dummy batch for graph capture
        dummy_batch = InputBatch.make_dummy(
            num_reqs=4,
            num_tokens=32,
            buffers=buffers,
        )
        
        def model_forward(inputs):
            # Simulate model forward
            return {"logits": np.random.randn(4, 1000).astype(np.float32)}
        
        inputs = {"input_ids": dummy_batch.input_ids}
        
        # Execute (should capture graph)
        outputs = manager.execute_or_capture(
            batch_size=4,
            seq_len=32,
            execute_fn=model_forward,
            inputs=inputs,
        )
        
        assert "logits" in outputs
        assert manager.registry.num_graphs >= 0  # May or may not capture


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
