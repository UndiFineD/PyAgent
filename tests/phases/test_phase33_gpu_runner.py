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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Phase 33 Tests: GPU Model Runner & Distributed Communication

Tests for Phase 33 vLLM patterns:
- InputBatchOrchestrator
- CUDAGraphManager
- BatchInvariantOps
- TensorParallelGroup
- NCCLCommunicator
- AttentionBackendRegistry
- Rust accelerations

Target: 60+ tests covering all Phase 33 functionality.
"""

import pytest
import numpy as np
from unittest.mock import MagicMock, patch

# Try to import torch
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

# Try to import rust_core
try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


# =============================================================================
# InputBatchOrchestrator Tests
# =============================================================================

class TestCachedRequestState:
    """Tests for CachedRequestState dataclass."""

    def test_create_cached_request_state(self):
        """Test creating a cached request state."""
        from src.infrastructure.services.execution.input_batch_orchestrator import CachedRequestState

        state = CachedRequestState(
            req_id="req-001",
            prompt_token_ids=[1, 2, 3, 4, 5],
            sampling_params={"temperature": 0.7},
        )

        assert state.req_id == "req-001"
        assert state.prompt_token_ids == [1, 2, 3, 4, 5]
        assert state.sampling_params == {"temperature": 0.7}
        assert state.output_token_ids == []
        assert state.num_computed_tokens == 0

    def test_cached_request_state_token_operations(self):
        """Test token operations on cached state."""
        from src.infrastructure.services.execution.input_batch_orchestrator import CachedRequestState

        state = CachedRequestState(
            req_id="req-002",
            prompt_token_ids=[10, 20, 30],
            sampling_params={},
        )

        # Add output tokens
        state.output_token_ids.extend([100, 200, 300])
        state.num_computed_tokens = 6

        assert len(state.output_token_ids) == 3
        assert state.num_computed_tokens == 6

    def test_cached_request_state_num_tokens(self):
        """Test num_tokens property."""
        from src.infrastructure.services.execution.input_batch_orchestrator import CachedRequestState

        state = CachedRequestState(
            req_id="req-003",
            prompt_token_ids=[1, 2, 3],
        )
        state.output_token_ids = [10, 20]

        assert state.num_tokens == 5  # 3 prompt + 2 output


class TestInputBuffers:
    """Tests for InputBuffers class."""

    @pytest.mark.skipif(not HAS_TORCH, reason="PyTorch not available")
    def test_create_input_buffers(self):
        """Test creating input buffers."""
        from src.infrastructure.services.execution.input_batch_orchestrator import InputBuffers

        buffers = InputBuffers(
            max_num_reqs=32,
            max_num_tokens=2048,
            inputs_embeds_size=0,
            vocab_size=32000,
            dtype=torch.float16,
            device="cpu",
        )

        assert buffers.max_num_reqs == 32
        assert buffers.max_num_tokens == 2048
        assert buffers.input_ids is not None
        assert buffers.positions is not None

    @pytest.mark.skipif(not HAS_TORCH, reason="PyTorch not available")
    def test_buffer_shapes(self):
        """Test buffer tensor shapes."""
        from src.infrastructure.services.execution.input_batch_orchestrator import InputBuffers

        buffers = InputBuffers(
            max_num_reqs=16,
            max_num_tokens=512,
            inputs_embeds_size=0,
            vocab_size=32000,
            dtype=torch.float16,
            device="cpu",
        )

        assert buffers.input_ids.shape[0] == 512
        assert buffers.positions.shape[0] == 512
        assert buffers.seq_lens.shape[0] == 16


class TestBatchUpdateBuilder:
    """Tests for BatchUpdateBuilder."""

    def test_batch_update_builder_record_swap(self):
        """Test recording swaps in batch builder."""
        from src.infrastructure.services.execution.input_batch_orchestrator import BatchUpdateBuilder

        builder = BatchUpdateBuilder()

        builder.record_swap(0, 1)
        builder.record_add("req-1", 2)

        assert len(builder.moved) == 1
        assert len(builder.added) == 1

    def test_batch_update_builder_reset(self):
        """Test resetting updates."""
        from src.infrastructure.services.execution.input_batch_orchestrator import BatchUpdateBuilder

        builder = BatchUpdateBuilder()
        builder.record_add("req-1", 0)
        builder.reset()

        assert len(builder.added) == 0


class TestInputBatchOrchestrator:
    """Tests for InputBatchOrchestrator."""

    @pytest.mark.skipif(not HAS_TORCH, reason="PyTorch not available")
    def test_create_orchestrator(self):
        """Test creating batch orchestrator."""
        from src.infrastructure.services.execution.input_batch_orchestrator import InputBatchOrchestrator

        orchestrator = InputBatchOrchestrator(
            max_num_reqs=32,
            max_model_len=2048,
            max_num_batched_tokens=4096,
            device="cpu",
        )

        assert orchestrator.max_num_reqs == 32
        assert orchestrator.max_model_len == 2048

    @pytest.mark.skipif(not HAS_TORCH, reason="PyTorch not available")
    def test_orchestrator_request_tracking(self):
        """Test request tracking in orchestrator."""
        from src.infrastructure.services.execution.input_batch_orchestrator import InputBatchOrchestrator

        orchestrator = InputBatchOrchestrator(
            max_num_reqs=8,
            max_model_len=512,
            max_num_batched_tokens=1024,
            device="cpu",
        )

        assert len(orchestrator.req_id_to_index) == 0


# =============================================================================
# CUDAGraphManager Tests
# =============================================================================

class TestBatchDescriptor:
    """Tests for BatchDescriptor."""

    def test_create_batch_descriptor(self):
        """Test creating a batch descriptor."""
        from src.infrastructure.services.execution.cuda_graph_manager import BatchDescriptor

        desc = BatchDescriptor(
            num_tokens=128,
            num_reqs=8,
            uniform=True,
            has_lora=False,
            has_multimodal=False,
        )

        assert desc.num_tokens == 128
        assert desc.num_reqs == 8
        assert desc.uniform is True

    def test_batch_descriptor_hash(self):
        """Test batch descriptor hashing."""
        from src.infrastructure.services.execution.cuda_graph_manager import BatchDescriptor

        desc1 = BatchDescriptor(8, 1, True, False, False)
        desc2 = BatchDescriptor(8, 1, True, False, False)
        desc3 = BatchDescriptor(16, 1, True, False, False)

        assert hash(desc1) == hash(desc2)
        assert hash(desc1) != hash(desc3)


class TestCUDAGraphRegistry:
    """Tests for CUDAGraphRegistry."""

    def test_create_registry(self):
        """Test creating graph registry."""
        from src.infrastructure.services.execution.cuda_graph_manager import CUDAGraphRegistry

        registry = CUDAGraphRegistry(max_graphs=10)

        assert registry.max_graphs == 10
        assert len(registry._graphs) == 0

    def test_registry_put_and_get(self):
        """Test put and get operations."""
        from src.infrastructure.services.execution.cuda_graph_manager import (
            CUDAGraphRegistry,
            CUDAGraphEntry,
        )

        registry = CUDAGraphRegistry(max_graphs=10)

        entry = CUDAGraphEntry(
            key="test_key",
            graph=None,
            input_buffers={},
            output_buffers={},
            num_tokens=128,
            num_reqs=8,
        )

        registry.put(entry)  # put takes only entry, key is in entry
        result = registry.get("test_key")

        assert result is not None
        assert result.num_tokens == 128

    def test_registry_lru_eviction(self):
        """Test LRU eviction in registry."""
        from src.infrastructure.services.execution.cuda_graph_manager import (
            CUDAGraphRegistry,
            CUDAGraphEntry,
        )

        registry = CUDAGraphRegistry(max_graphs=2)

        # Add entries - key is in the entry itself
        entry1 = CUDAGraphEntry(key="k1", graph=None, input_buffers={}, output_buffers={}, num_tokens=64, num_reqs=1)
        entry2 = CUDAGraphEntry(key="k2", graph=None, input_buffers={}, output_buffers={}, num_tokens=64, num_reqs=2)
        entry3 = CUDAGraphEntry(key="k3", graph=None, input_buffers={}, output_buffers={}, num_tokens=64, num_reqs=3)

        registry.put(entry1)
        registry.put(entry2)

        # Access k1 to make it more recent
        registry.get("k1")

        # Add third entry, should evict k2
        registry.put(entry3)

        assert registry.get("k1") is not None
        assert registry.get("k2") is None
        assert registry.get("k3") is not None


class TestCUDAGraphManager:
    """Tests for CUDAGraphManager."""

    def test_create_manager(self):
        """Test creating graph manager."""
        from src.infrastructure.services.execution.cuda_graph_manager import (
            CUDAGraphManager,
            CUDAGraphMode,
        )

        manager = CUDAGraphManager(
            mode=CUDAGraphMode.FULL,
            max_graphs=32,
        )

        assert manager.mode == CUDAGraphMode.FULL
        assert manager.registry.max_graphs == 32

    def test_compute_graph_key(self):
        """Test graph key computation."""
        from src.infrastructure.services.execution.cuda_graph_manager import (
            compute_graph_key,
            BatchDescriptor,
        )

        desc = BatchDescriptor(128, 8, True, False, False)
        key = compute_graph_key(desc)

        assert isinstance(key, str)
        assert len(key) > 0

    def test_graph_mode_enum(self):
        """Test CUDA graph mode enum."""
        from src.infrastructure.services.execution.cuda_graph_manager import CUDAGraphMode

        assert CUDAGraphMode.NONE is not None
        assert CUDAGraphMode.PIECEWISE is not None
        assert CUDAGraphMode.FULL is not None


# =============================================================================
# BatchInvariantOps Tests
# =============================================================================

class TestBatchInvariantOps:
    """Tests for batch invariant operations."""

    @pytest.mark.skipif(not HAS_TORCH, reason="PyTorch not available")
    def test_softmax_batch_invariant(self):
        """Test batch invariant softmax."""
        from src.core.base.logic.math.batch_invariant_ops import softmax_batch_invariant

        x = torch.randn(4, 8, 16)
        result = softmax_batch_invariant(x, dim=-1)

        assert result.shape == x.shape
        # Softmax should sum to 1 along dim
        sums = result.sum(dim=-1)
        assert torch.allclose(sums, torch.ones_like(sums), atol=1e-5)

    @pytest.mark.skipif(not HAS_TORCH, reason="PyTorch not available")
    def test_mean_batch_invariant(self):
        """Test batch invariant mean."""
        from src.core.base.logic.math.batch_invariant_ops import mean_batch_invariant

        x = torch.randn(4, 8, 16)
        result = mean_batch_invariant(x, dim=-1)

        assert result.shape == (4, 8)

    @pytest.mark.skipif(not HAS_TORCH, reason="PyTorch not available")
    def test_mm_batch_invariant(self):
        """Test batch invariant matrix multiply."""
        from src.core.base.logic.math.batch_invariant_ops import mm_batch_invariant

        a = torch.randn(32, 64)
        b = torch.randn(64, 16)

        result = mm_batch_invariant(a, b)
        expected = torch.mm(a, b)

        assert result.shape == expected.shape
        assert torch.allclose(result, expected, atol=1e-5)

    @pytest.mark.skipif(not HAS_TORCH, reason="PyTorch not available")
    def test_layer_norm_batch_invariant(self):
        """Test batch invariant layer norm."""
        from src.core.base.logic.math.batch_invariant_ops import layer_norm_batch_invariant

        x = torch.randn(4, 8, 64)
        weight = torch.ones(64)
        bias = torch.zeros(64)

        result = layer_norm_batch_invariant(x, [64], weight, bias)

        assert result.shape == x.shape

    @pytest.mark.skipif(not HAS_TORCH, reason="PyTorch not available")
    def test_gelu_batch_invariant(self):
        """Test batch invariant GELU."""
        from src.core.base.logic.math.batch_invariant_ops import gelu_batch_invariant

        x = torch.randn(16, 32)
        result = gelu_batch_invariant(x)
        expected = torch.nn.functional.gelu(x, approximate="tanh")

        assert result.shape == x.shape
        # Use larger tolerance for approximate GELU
        assert torch.allclose(result, expected, atol=1e-3)


# =============================================================================
# TensorParallelGroup Tests
# =============================================================================

class TestParallelConfig:
    """Tests for ParallelConfig."""

    def test_create_parallel_config(self):
        """Test creating parallel config."""
        from src.infrastructure.swarm.distributed.tensor_parallel_group import ParallelConfig

        config = ParallelConfig(
            tensor_parallel_size=4,
            pipeline_parallel_size=2,
            data_parallel_size=1,
        )

        assert config.tensor_parallel_size == 4
        assert config.pipeline_parallel_size == 2
        assert config.world_size == 8  # 4 * 2 * 1

    def test_parallel_config_from_env(self):
        """Test creating config from environment."""
        from src.infrastructure.swarm.distributed.tensor_parallel_group import ParallelConfig
        import os

        # Save original env
        orig_tp = os.environ.get("TENSOR_PARALLEL_SIZE")

        os.environ["TENSOR_PARALLEL_SIZE"] = "2"
        config = ParallelConfig.from_env()

        # Restore
        if orig_tp:
            os.environ["TENSOR_PARALLEL_SIZE"] = orig_tp
        else:
            os.environ.pop("TENSOR_PARALLEL_SIZE", None)

        assert config.tensor_parallel_size == 2


class TestRankInfo:
    """Tests for RankInfo."""

    def test_create_rank_info(self):
        """Test creating rank info."""
        from src.infrastructure.swarm.distributed.tensor_parallel_group import RankInfo

        info = RankInfo(
            global_rank=5,
            local_rank=1,
            tp_rank=1,
            pp_rank=1,
            dp_rank=0,
        )

        assert info.global_rank == 5
        assert info.tp_rank == 1


class TestGroupCoordinator:
    """Tests for GroupCoordinator."""

    def test_create_group_coordinator(self):
        """Test creating group coordinator."""
        from src.infrastructure.swarm.distributed.tensor_parallel_group import (
            GroupCoordinator,
            ParallelConfig,
            RankInfo,
        )

        config = ParallelConfig(tensor_parallel_size=2)
        rank_info = RankInfo(global_rank=0, local_rank=0, tp_rank=0, pp_rank=0, dp_rank=0)
        coord = GroupCoordinator(config, rank_info)

        assert coord.config.tensor_parallel_size == 2
        assert coord.rank_info.global_rank == 0


class TestTensorParallelGroup:
    """Tests for TensorParallelGroup."""

    def test_create_tp_group(self):
        """Test creating TP group."""
        from src.infrastructure.swarm.distributed.tensor_parallel_group import (
            TensorParallelGroup,
            GroupCoordinator,
            ParallelConfig,
            RankInfo,
        )

        config = ParallelConfig(tensor_parallel_size=4)
        rank_info = RankInfo(global_rank=0, local_rank=0, tp_rank=0, pp_rank=0, dp_rank=0)
        coord = GroupCoordinator(config, rank_info)
        group = TensorParallelGroup(coord)

        assert group.tp_size == 4
        assert group.tp_rank == 0

    @pytest.mark.skipif(not HAS_TORCH, reason="PyTorch not available")
    def test_shard_tensor(self):
        """Test tensor sharding."""
        from src.infrastructure.swarm.distributed.tensor_parallel_group import (
            TensorParallelGroup,
            GroupCoordinator,
            ParallelConfig,
            RankInfo,
        )

        config = ParallelConfig(tensor_parallel_size=4)
        rank_info = RankInfo(global_rank=1, local_rank=1, tp_rank=1, pp_rank=0, dp_rank=0)
        coord = GroupCoordinator(config, rank_info)
        group = TensorParallelGroup(coord)

        tensor = torch.randn(64, 128)
        shard = group.shard_tensor(tensor, dim=0)

        assert shard.shape[0] == 16  # 64 / 4
        assert shard.shape[1] == 128


# =============================================================================
# NCCLCommunicator Tests
# =============================================================================

class TestNCCLConfig:
    """Tests for NCCLConfig."""

    def test_create_nccl_config(self):
        """Test creating NCCL config."""
        from src.infrastructure.swarm.distributed.nccl_communicator import NCCLConfig

        config = NCCLConfig(
            timeout_seconds=600.0,
            max_retries=5,
        )

        assert config.timeout_seconds == 600.0
        assert config.max_retries == 5


class TestNCCLCommunicator:
    """Tests for NCCLCommunicator."""

    def test_create_communicator(self):
        """Test creating NCCL communicator."""
        from src.infrastructure.swarm.distributed.nccl_communicator import NCCLCommunicator

        comm = NCCLCommunicator()

        assert comm.world_size >= 1
        assert comm.rank >= 0

    def test_get_stats(self):
        """Test getting communicator stats."""
        from src.infrastructure.swarm.distributed.nccl_communicator import NCCLCommunicator

        comm = NCCLCommunicator()
        stats = comm.get_stats()

        assert "world_size" in stats
        assert "rank" in stats
        assert "all_reduce_count" in stats


class TestReduceOp:
    """Tests for ReduceOp enum."""

    def test_reduce_ops(self):
        """Test reduce operation enum values."""
        from src.infrastructure.swarm.distributed.nccl_communicator import ReduceOp

        assert ReduceOp.SUM is not None
        assert ReduceOp.PROD is not None
        assert ReduceOp.MAX is not None
        assert ReduceOp.MIN is not None
        assert ReduceOp.AVG is not None


# =============================================================================
# AttentionBackendRegistry Tests
# =============================================================================

class TestAttentionBackendEnum:
    """Tests for AttentionBackendEnum."""

    def test_backend_enum_values(self):
        """Test backend enum values."""
        from src.infrastructure.engine.attention.attention_backend_registry import AttentionBackendEnum

        assert AttentionBackendEnum.FLASH_ATTN.value == "flash_attn"
        assert AttentionBackendEnum.FLASHINFER.value == "flashinfer"
        assert AttentionBackendEnum.TORCH_SDPA.value == "torch_sdpa"


class TestAttentionCapabilities:
    """Tests for AttentionCapabilities."""

    def test_create_capabilities(self):
        """Test creating attention capabilities."""
        from src.infrastructure.engine.attention.attention_backend_registry import AttentionCapabilities

        caps = AttentionCapabilities(
            supports_prefill=True,
            supports_decode=True,
            supports_sliding_window=True,
            min_sm_version=80,
        )

        assert caps.supports_prefill is True
        assert caps.supports_sliding_window is True
        assert caps.min_sm_version == 80


class TestNaiveAttentionBackend:
    """Tests for NaiveAttentionBackend."""

    def test_naive_backend_name(self):
        """Test naive backend name."""
        from src.infrastructure.engine.attention.attention_backend_registry import NaiveAttentionBackend

        assert NaiveAttentionBackend.get_name() == "naive"

    def test_naive_backend_capabilities(self):
        """Test naive backend capabilities."""
        from src.infrastructure.engine.attention.attention_backend_registry import NaiveAttentionBackend

        caps = NaiveAttentionBackend.get_capabilities()

        assert caps.requires_cuda is False
        assert caps.supports_prefill is True


class TestAttentionBackendRegistry:
    """Tests for AttentionBackendRegistry."""

    def test_singleton_pattern(self):
        """Test registry singleton pattern."""
        from src.infrastructure.engine.attention.attention_backend_registry import AttentionBackendRegistry

        reg1 = AttentionBackendRegistry()
        reg2 = AttentionBackendRegistry()

        assert reg1 is reg2

    def test_list_backends(self):
        """Test listing registered backends."""
        from src.infrastructure.engine.attention.attention_backend_registry import get_attention_registry

        registry = get_attention_registry()
        backends = registry.list_backends()

        assert "naive" in backends
        assert "torch_sdpa" in backends

    def test_get_backend(self):
        """Test getting a backend."""
        from src.infrastructure.engine.attention.attention_backend_registry import get_attention_registry

        registry = get_attention_registry()
        backend = registry.get_backend("naive")

        assert backend is not None
        assert backend.get_name() == "naive"

    def test_select_backend(self):
        """Test selecting backend based on capabilities."""
        from src.infrastructure.engine.attention.attention_backend_registry import get_attention_registry

        registry = get_attention_registry()
        backend = registry.select_backend()

        assert backend is not None


# =============================================================================
# Rust Acceleration Tests
# =============================================================================

@pytest.mark.skipif(not HAS_RUST, reason="rust_core not available")
class TestRustPhase33:
    """Tests for Phase 33 Rust accelerations."""

    def test_prepare_positions_rust(self):
        """Test position preparation."""
        positions = rust_core.prepare_positions_rust([5, 8, 6], [0, 2, 1])

        assert len(positions) == 3
        assert positions[0] == [0, 1, 2, 3, 4]  # 0 to 5
        assert positions[1] == [2, 3, 4, 5, 6, 7]  # 2 to 8

    def test_compute_idx_mapping_rust(self):
        """Test index mapping computation."""
        valid_mask = [True, False, True, True, False]
        mapping, count = rust_core.compute_idx_mapping_rust(valid_mask, 5)

        assert count == 3
        assert mapping[0] == 0
        assert mapping[1] == -1
        assert mapping[2] == 1
        assert mapping[3] == 2

    def test_expand_idx_mapping_rust(self):
        """Test index mapping expansion."""
        idx_mapping = [0, -1, 1]
        elements = [2, 2, 2]

        expanded = rust_core.expand_idx_mapping_rust(idx_mapping, elements)

        assert len(expanded) == 6

    def test_cudagraph_key_hash_rust(self):
        """Test CUDA graph key hashing."""
        hash1 = rust_core.cudagraph_key_hash_rust(8, 128, 1, True)
        hash2 = rust_core.cudagraph_key_hash_rust(8, 128, 1, True)
        hash3 = rust_core.cudagraph_key_hash_rust(16, 128, 1, True)

        assert hash1 == hash2
        assert hash1 != hash3

    def test_warmup_sizes_rust(self):
        """Test warmup size generation."""
        sizes = rust_core.warmup_sizes_rust(32, 512, 1, 8)

        assert len(sizes) > 0
        assert all(isinstance(s, tuple) for s in sizes)

    def test_softmax_stable_rust(self):
        """Test numerically stable softmax."""
        logits = [1.0, 2.0, 3.0, 4.0, 5.0]
        probs = rust_core.softmax_stable_rust(logits)

        assert len(probs) == 5
        assert abs(sum(probs) - 1.0) < 1e-6

    def test_persistent_gemm_tile_rust(self):
        """Test persistent GEMM tile computation."""
        a = [[1.0, 2.0], [3.0, 4.0]]
        b = [[5.0, 6.0], [7.0, 8.0]]

        c = rust_core.persistent_gemm_tile_rust(a, b)

        assert len(c) == 2
        assert len(c[0]) == 2
        assert abs(c[0][0] - 19.0) < 1e-6  # 1*5 + 2*7

    def test_all_reduce_sum_rust(self):
        """Test all-reduce sum simulation."""
        local = [1.0, 2.0, 3.0]
        others = [[4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]

        result = rust_core.all_reduce_sum_rust(local, others)

        assert result == [12.0, 15.0, 18.0]

    def test_rank_assignment_rust(self):
        """Test rank assignment for sharding."""
        start, size = rust_core.rank_assignment_rust(100, 4, 0)

        assert start == 0
        assert size == 25

        start2, size2 = rust_core.rank_assignment_rust(100, 4, 1)
        assert start2 == 25

    def test_attention_dispatch_rust(self):
        """Test attention backend dispatch."""
        # With flash_attn available, long sequence
        backend = rust_core.attention_dispatch_rust(
            1024, 8, 32, 128, True, True, False, False
        )

        assert backend == 0  # flash_attn

        # Decode mode prefers flashinfer
        backend2 = rust_core.attention_dispatch_rust(
            1, 8, 32, 128, True, True, False, True
        )

        assert backend2 == 1  # flashinfer


# =============================================================================
# Integration Tests
# =============================================================================

class TestPhase33Integration:
    """Integration tests for Phase 33 components."""

    def test_input_batch_to_attention(self):
        """Test flow from input batch to attention."""
        from src.infrastructure.services.execution.input_batch_orchestrator import (
            CachedRequestState,
            BatchUpdateBuilder,
        )
        from src.infrastructure.engine.attention.attention_backend_registry import (
            get_attention_registry,
            AttentionMetadata,
            AttentionType,
        )

        # Create cached request state
        state = CachedRequestState(
            req_id="r1",
            prompt_token_ids=[1, 2, 3],
        )

        # Get attention backend
        registry = get_attention_registry()
        backend = registry.select_backend()

        assert backend is not None
        assert state.num_tokens == 3

    @pytest.mark.skipif(not HAS_TORCH, reason="PyTorch not available")
    def test_tensor_parallel_with_comm(self):
        """Test tensor parallel with communicator."""
        from src.infrastructure.swarm.distributed.tensor_parallel_group import (
            TensorParallelGroup,
            GroupCoordinator,
            ParallelConfig,
            RankInfo,
        )
        from src.infrastructure.swarm.distributed.nccl_communicator import NCCLCommunicator

        # Create TP group
        config = ParallelConfig(tensor_parallel_size=4)
        rank_info = RankInfo(global_rank=0, local_rank=0, tp_rank=0, pp_rank=0, dp_rank=0)
        coord = GroupCoordinator(config, rank_info)
        tp_group = TensorParallelGroup(coord)

        # Create communicator
        comm = NCCLCommunicator()

        # Shard tensor
        tensor = torch.randn(64, 128)
        shard = tp_group.shard_tensor(tensor, dim=0)

        assert shard.shape[0] == 16
        assert comm.world_size >= 1

    def test_cudagraph_with_batch(self):
        """Test CUDA graph manager with batch descriptor."""
        from src.infrastructure.services.execution.cuda_graph_manager import (
            CUDAGraphManager,
            CUDAGraphMode,
            BatchDescriptor,
            compute_graph_key,
        )

        manager = CUDAGraphManager(
            mode=CUDAGraphMode.FULL,
            max_graphs=32,
        )

        # Create batch descriptor
        desc = BatchDescriptor(
            num_tokens=128,
            num_reqs=8,
            uniform=True,
            has_lora=False,
            has_multimodal=False,
        )

        # Compute key using standalone function
        key = compute_graph_key(desc)

        # Check if graph exists (should be None initially)
        entry = manager.registry.get(key)

        # Should be None since no graph captured
        assert entry is None
        assert isinstance(key, str)


# =============================================================================
# Edge Cases and Error Handling Tests
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_empty_batch(self):
        """Test handling empty batch."""
        from src.infrastructure.services.execution.input_batch_orchestrator import BatchUpdateBuilder

        builder = BatchUpdateBuilder()

        # Empty builder should have no moves
        assert len(builder.moved) == 0
        assert len(builder.added) == 0

    def test_registry_unknown_backend(self):
        """Test getting unknown backend."""
        from src.infrastructure.engine.attention.attention_backend_registry import get_attention_registry

        registry = get_attention_registry()
        backend = registry.get_backend("nonexistent_backend")

        assert backend is None

    @pytest.mark.skipif(not HAS_RUST, reason="rust_core not available")
    def test_empty_softmax(self):
        """Test softmax with empty input."""
        result = rust_core.softmax_stable_rust([])
        assert result == []

    @pytest.mark.skipif(not HAS_RUST, reason="rust_core not available")
    def test_invalid_rank_assignment(self):
        """Test rank assignment with invalid params."""
        start, size = rust_core.rank_assignment_rust(100, 0, 0)
        assert start == 0
        assert size == 0

    def test_communicator_stats_reset(self):
        """Test resetting communicator stats."""
        from src.infrastructure.swarm.distributed.nccl_communicator import NCCLCommunicator

        comm = NCCLCommunicator()
        comm.reset_stats()

        stats = comm.get_stats()
        assert stats["all_reduce_count"] == 0

    def test_cached_request_state_defaults(self):
        """Test CachedRequestState with minimal args."""
        from src.infrastructure.services.execution.input_batch_orchestrator import CachedRequestState

        state = CachedRequestState(req_id="test")

        assert state.req_id == "test"
        assert state.prompt_token_ids is None
        assert state.output_token_ids == []

    def test_graph_registry_empty_get(self):
        """Test getting from empty registry."""
        from src.infrastructure.services.execution.cuda_graph_manager import CUDAGraphRegistry

        registry = CUDAGraphRegistry(max_graphs=10)

        result = registry.get("nonexistent")
        assert result is None
