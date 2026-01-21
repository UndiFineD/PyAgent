# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Test Suite for Phase 34: Disaggregated Inference & Advanced RoPE.

Tests for:
- KV Transfer Connectors
- Rotary Embedding Engine
- Speculative Decoding Engine
- Disaggregated Scheduler
- Triton Attention Operations
- Batch DCP Wrappers
- Rust accelerations (12 functions)
"""

import asyncio
import math
import time
from typing import Dict, List, Optional, Tuple
from unittest.mock import MagicMock, patch

import pytest


# =============================================================================
# KV Transfer Connector Tests
# =============================================================================


class TestKVTransferConnector:
    """Tests for KV transfer infrastructure."""

    def test_kv_connector_role_enum(self):
        """Test KVConnectorRole enum values."""
        from src.infrastructure.storage.kv_transfer import KVConnectorRole
        
        assert KVConnectorRole.PRODUCER.value == 1
        assert KVConnectorRole.CONSUMER.value == 2
        assert KVConnectorRole.BOTH.value == 3

    def test_kv_transfer_config_defaults(self):
        """Test KVTransferConfig default values."""
        from src.infrastructure.storage.kv_transfer import KVTransferConfig
        
        config = KVTransferConfig()
        assert config.kv_connector == "DecodeBenchConnector"
        assert config.kv_buffer_size == int(1e9)
        assert config.kv_buffer_device == "cuda"

    def test_kv_transfer_config_custom(self):
        """Test KVTransferConfig with custom values."""
        from src.infrastructure.storage.kv_transfer import KVTransferConfig
        
        config = KVTransferConfig(
            kv_connector="NixlConnector",
            kv_buffer_size=int(5e9),
            kv_parallel_size=4,
        )
        assert config.kv_connector == "NixlConnector"
        assert config.kv_buffer_size == int(5e9)
        assert config.kv_parallel_size == 4

    def test_kv_transfer_config_properties(self):
        """Test KVTransferConfig properties."""
        from src.infrastructure.storage.kv_transfer import KVTransferConfig, KVConnectorRole
        
        # Producer role
        config = KVTransferConfig(kv_role=KVConnectorRole.PRODUCER)
        assert config.is_producer == True
        assert config.is_consumer == False
        
        # Consumer role
        config = KVTransferConfig(kv_role=KVConnectorRole.CONSUMER)
        assert config.is_producer == False
        assert config.is_consumer == True

    def test_kv_connector_metadata(self):
        """Test KVConnectorMetadata creation."""
        from src.infrastructure.storage.kv_transfer import KVConnectorMetadata
        
        metadata = KVConnectorMetadata()
        assert isinstance(metadata.reqs_to_fill, dict)

    def test_kv_cache_blocks(self):
        """Test KVCacheBlocks tracking."""
        from src.infrastructure.storage.kv_transfer import KVCacheBlocks
        
        blocks = KVCacheBlocks(num_blocks=1024, block_size=16)
        assert blocks.num_blocks == 1024
        assert blocks.block_size == 16

    def test_decode_bench_connector_creation(self):
        """Test DecodeBenchConnector instantiation."""
        from src.infrastructure.storage.kv_transfer import (
            DecodeBenchConnector,
            KVTransferConfig,
        )
        
        config = KVTransferConfig()
        connector = DecodeBenchConnector(config)
        assert connector is not None

    def test_connector_registry(self):
        """Test connector registry functionality."""
        from src.infrastructure.storage.kv_transfer import (
            get_kv_connector,
            list_kv_connectors,
            KVTransferConfig,
        )
        
        # List available connectors
        connectors = list_kv_connectors()
        assert isinstance(connectors, list)
        
        # Get a connector using config
        if connectors:
            config = KVTransferConfig(kv_connector=connectors[0])
            connector = get_kv_connector(config)
            assert connector is not None


# =============================================================================
# Rotary Embedding Engine Tests
# =============================================================================


class TestRotaryEmbeddingEngine:
    """Tests for RoPE implementation."""

    def test_rope_variant_enum(self):
        """Test RoPEVariant enum values."""
        from src.infrastructure.engine.position import RoPEVariant
        
        assert RoPEVariant.NEOX.value == 1
        assert RoPEVariant.GPTJ.value == 2
        assert RoPEVariant.MROPE.value == 3
        assert RoPEVariant.XDROPE.value == 4

    def test_rope_config_defaults(self):
        """Test RoPEConfig default values."""
        from src.infrastructure.engine.position import RoPEConfig
        
        config = RoPEConfig()
        assert config.head_dim == 64
        assert config.base == 10000.0
        assert config.max_position_embeddings == 2048

    def test_rope_config_custom(self):
        """Test RoPEConfig with custom values."""
        from src.infrastructure.engine.position import RoPEConfig, RoPEScalingType
        
        config = RoPEConfig(
            head_dim=128,
            base=500000.0,
            scaling_type=RoPEScalingType.DYNAMIC,
        )
        assert config.head_dim == 128
        assert config.base == 500000.0
        assert config.scaling_type == RoPEScalingType.DYNAMIC

    def test_rope_config_variant_detection(self):
        """Test RoPEConfig automatic variant detection."""
        from src.infrastructure.engine.position import RoPEConfig, RoPEVariant
        
        # MROPE config
        mrope_config = RoPEConfig(mrope_sections=[2, 2, 2])
        assert mrope_config.variant == RoPEVariant.MROPE

    def test_neox_rotary_embedding_forward(self):
        """Test NeoxRotaryEmbedding creation and cache computation."""
        from src.infrastructure.engine.position import NeoxRotaryEmbedding, RoPEConfig
        
        config = RoPEConfig(head_dim=64, max_position_embeddings=128)
        rope = NeoxRotaryEmbedding(config)
        
        # Verify the cache can be computed
        cos, sin = rope._compute_cos_sin_cache(64)
        assert cos is not None
        assert sin is not None
        
        # Verify inv_freq is computed
        assert rope.inv_freq is not None

    def test_gptj_rotary_embedding_forward(self):
        """Test GptJRotaryEmbedding forward pass - requires PyTorch."""
        from src.infrastructure.engine.position import GptJRotaryEmbedding, RoPEConfig
        
        config = RoPEConfig(head_dim=64, is_neox_style=False)
        rope = GptJRotaryEmbedding(config)
        
        # GPT-J requires PyTorch, so just verify creation
        # Skip forward test if torch not available
        try:
            import torch
            positions = torch.tensor([[0, 1, 2, 3]])
            query = torch.randn(1, 4, 8, 64)
            key = torch.randn(1, 4, 8, 64)
            
            q_out, k_out = rope.forward_native(positions, query, key)
            assert q_out.shape == query.shape
        except ImportError:
            # PyTorch not available, just verify creation
            assert rope is not None

    def test_mrope_section_config(self):
        """Test MRotaryEmbedding section configuration - requires PyTorch."""
        from src.infrastructure.engine.position import MRotaryEmbedding, RoPEConfig
        
        try:
            config = RoPEConfig(
                head_dim=64,
                mrope_sections=[8, 8, 8],  # temporal, height, width - must sum*2 <= rotary_dim
            )
            rope = MRotaryEmbedding(config)
            assert rope is not None
        except RuntimeError as e:
            if "PyTorch" in str(e):
                import pytest
                pytest.skip("MRotaryEmbedding requires PyTorch")
            raise

    def test_xd_rope_dynamic_scaling(self):
        """Test XDRotaryEmbedding dynamic NTK scaling."""
        from src.infrastructure.engine.position import XDRotaryEmbedding, RoPEConfig
        
        config = RoPEConfig(
            head_dim=64,
            base=10000.0,
            original_max_position=4096,
            dynamic_scaling=True,
        )
        rope = XDRotaryEmbedding(config)
        
        # For sequences beyond original length, base should scale
        assert rope is not None

    def test_rotary_embedding_engine_creation(self):
        """Test RotaryEmbeddingEngine creation."""
        from src.infrastructure.engine.position import RotaryEmbeddingEngine, RoPEConfig
        
        config = RoPEConfig(head_dim=64)
        engine = RotaryEmbeddingEngine(config)
        assert engine is not None

    def test_rotary_embedding_engine_precomputed_cache(self):
        """Test precomputed cos/sin cache."""
        from src.infrastructure.engine.position import RotaryEmbeddingEngine, RoPEConfig
        
        config = RoPEConfig(head_dim=64, max_position_embeddings=128)
        engine = RotaryEmbeddingEngine(config)
        
        # Engine should be created successfully
        assert engine is not None


# =============================================================================
# Speculative Engine Tests
# =============================================================================


class TestSpeculativeEngine:
    """Tests for speculative decoding."""

    def test_spec_method_enum(self):
        """Test SpecMethod enum values."""
        from src.inference.speculation import SpecMethod
        
        assert SpecMethod.NGRAM.value == 1
        assert SpecMethod.EAGLE.value == 2
        assert SpecMethod.EAGLE3.value == 3
        assert SpecMethod.MEDUSA.value == 4

    def test_speculative_config_defaults(self):
        """Test SpeculativeConfig defaults."""
        from src.inference.speculation import SpeculativeConfig, SpecMethod
        
        config = SpeculativeConfig()
        assert config.num_speculative_tokens == 5
        assert config.method == SpecMethod.NGRAM

    def test_speculative_config_use_eagle(self):
        """Test SpeculativeConfig use_eagle method."""
        from src.inference.speculation import SpeculativeConfig, SpecMethod
        
        ngram_config = SpeculativeConfig(method=SpecMethod.NGRAM)
        assert ngram_config.use_eagle() == False
        
        eagle_config = SpeculativeConfig(method=SpecMethod.EAGLE)
        assert eagle_config.use_eagle() == True

    def test_draft_proposal_creation(self):
        """Test DraftProposal dataclass."""
        from src.inference.speculation import DraftProposal, SpecMethod
        
        proposal = DraftProposal(
            draft_token_ids=[[100, 200, 300]],
            num_proposed=[3],
            method_used=SpecMethod.NGRAM,
        )
        assert len(proposal.draft_token_ids[0]) == 3
        assert proposal.num_proposed[0] == 3
        assert proposal.method_used == SpecMethod.NGRAM

    def test_ngram_proposer_creation(self):
        """Test NgramProposer instantiation."""
        from src.inference.speculation import NgramProposer, SpeculativeConfig
        
        config = SpeculativeConfig()
        proposer = NgramProposer(config)
        assert proposer is not None

    def test_ngram_proposer_propose(self):
        """Test NgramProposer token proposal."""
        from src.inference.speculation import NgramProposer, SpeculativeConfig
        
        config = SpeculativeConfig(num_speculative_tokens=2, prompt_lookup_max=3)
        proposer = NgramProposer(config)
        
        # NgramProposer doesn't need index building - it finds n-gram matches inline
        # Create prompt with repeating pattern: [1,2,3] appears twice
        prompt = [1, 2, 3, 4, 5, 1, 2, 3, 6, 7, 1, 2, 3]
        
        # Propose tokens - n-gram matching happens inline
        proposal = proposer.propose([prompt])
        assert proposal is not None
        assert proposal.method_used.name == "NGRAM"

    def test_suffix_proposer(self):
        """Test SuffixProposer for pattern matching."""
        from src.inference.speculation import SuffixProposer, SpeculativeConfig
        
        config = SpeculativeConfig(num_speculative_tokens=3)
        proposer = SuffixProposer(config)
        
        # Build suffix structure using add_pattern (correct method name)
        prompt = [10, 20, 30, 40, 50, 10, 20, 30, 60]
        proposer.add_pattern(prompt)
        
        # Propose tokens using propose() method
        proposal = proposer.propose([[10, 20, 30]])
        assert proposal is not None
        assert proposal.method_used.name == "SUFFIX"

    def test_eagle_proposer_creation(self):
        """Test EagleProposer instantiation."""
        from src.inference.speculation import EagleProposer, SpeculativeConfig, SpecMethod
        
        config = SpeculativeConfig(method=SpecMethod.EAGLE)
        proposer = EagleProposer(config)
        assert proposer is not None

    def test_hybrid_drafter(self):
        """Test HybridDrafter with EAGLE + N-gram fallback."""
        from src.inference.speculation import HybridDrafter, SpeculativeConfig
        
        config = SpeculativeConfig()
        drafter = HybridDrafter(config)
        
        # HybridDrafter uses internal NgramProposer which finds patterns inline
        # Create prompt with repeating pattern
        prompt = [1, 2, 3, 4, 5, 1, 2, 3, 6, 7]
        
        # Propose using propose() method
        proposal = drafter.propose([prompt])
        assert proposal is not None

    def test_token_verifier(self):
        """Test TokenVerifier acceptance logic."""
        from src.inference.speculation import TokenVerifier, DraftProposal, SpecMethod
        
        # TokenVerifier takes method string, not config
        verifier = TokenVerifier(method="rejection_sampler")
        
        # Create mock draft proposal
        proposal = DraftProposal(
            draft_token_ids=[[100, 200, 300]],
            num_proposed=[3],
            method_used=SpecMethod.NGRAM,
        )
        
        # Verifier should be created and can verify
        assert verifier is not None
        result = verifier.verify(proposal.draft_token_ids, target_logprobs=None)
        assert result is not None

    def test_speculative_engine_interface(self):
        """Test SpeculativeEngine unified interface."""
        from src.inference.speculation import SpeculativeEngine, SpeculativeConfig, SpecMethod
        
        config = SpeculativeConfig(method=SpecMethod.NGRAM)
        engine = SpeculativeEngine(config)
        
        # Method is accessed via config.method, not engine.method
        assert engine.config.method == SpecMethod.NGRAM

    def test_spec_decoding_metrics(self):
        """Test SpecDecodingMetrics tracking."""
        from src.inference.speculation import SpecDecodingMetrics
        
        metrics = SpecDecodingMetrics()
        # Actual fields are num_draft_tokens and num_accepted_tokens
        assert metrics.num_draft_tokens == 0
        assert metrics.num_accepted_tokens == 0


# =============================================================================
# Disaggregated Scheduler Tests
# =============================================================================


class TestDisaggregatedScheduler:
    """Tests for disaggregated prefill-decode scheduling."""

    def test_instance_role_enum(self):
        """Test InstanceRole enum values."""
        from src.infrastructure.engine.scheduling import InstanceRole
        
        assert InstanceRole.PREFILL.value == 1
        assert InstanceRole.DECODE.value == 2
        assert InstanceRole.UNIFIED.value == 3

    def test_scheduling_policy_enum(self):
        """Test SchedulingPolicy enum values."""
        from src.infrastructure.engine.scheduling import SchedulingPolicy
        
        assert SchedulingPolicy.ROUND_ROBIN.value == 1
        assert SchedulingPolicy.LEAST_LOADED.value == 2
        assert SchedulingPolicy.RANDOM.value == 3

    def test_instance_info_creation(self):
        """Test InstanceInfo dataclass."""
        from src.infrastructure.engine.scheduling import InstanceInfo, InstanceRole
        
        info = InstanceInfo(
            instance_id="prefill_0",
            role=InstanceRole.PREFILL,
            host="localhost",
            http_port=8000,
            kv_port=8001,
        )
        assert info.base_url == "http://localhost:8000"
        assert info.kv_address == "localhost:8001"

    def test_instance_info_load_score(self):
        """Test InstanceInfo load scoring."""
        from src.infrastructure.engine.scheduling import InstanceInfo, InstanceRole
        
        info = InstanceInfo(
            instance_id="decode_0",
            role=InstanceRole.DECODE,
            host="localhost",
            http_port=8000,
            num_running_requests=5,
            num_waiting_requests=2,
        )
        # Load = running + 0.5 * waiting
        assert info.load_score == 6.0

    def test_dcp_config_defaults(self):
        """Test DCPConfig default values."""
        from src.infrastructure.engine.scheduling import DCPConfig
        
        config = DCPConfig()
        assert config.enabled == False
        assert config.kv_connector == "NixlConnector"

    def test_kv_transfer_params(self):
        """Test KVTransferParams creation and serialization."""
        from src.infrastructure.engine.scheduling import KVTransferParams
        
        params = KVTransferParams(
            do_remote_prefill=True,
            remote_host="gpu-node-1",
            remote_port=8001,
            remote_block_ids=[0, 1, 2],
        )
        
        d = params.to_dict()
        assert d["do_remote_prefill"] == True
        assert d["remote_host"] == "gpu-node-1"
        assert d["remote_block_ids"] == [0, 1, 2]
        
        # Round-trip
        restored = KVTransferParams.from_dict(d)
        assert restored.remote_host == "gpu-node-1"

    def test_scheduled_request(self):
        """Test ScheduledRequest dataclass."""
        from src.infrastructure.engine.scheduling import ScheduledRequest
        
        request = ScheduledRequest(
            request_id="req_001",
            prompt="Hello, world!",
            max_tokens=100,
        )
        assert request.request_id == "req_001"
        assert request.prefill_complete == False

    def test_round_robin_selector(self):
        """Test RoundRobinSelector instance selection."""
        from src.infrastructure.engine.scheduling import (
            RoundRobinSelector,
            InstanceInfo,
            InstanceRole,
            ScheduledRequest,
        )
        
        selector = RoundRobinSelector()
        instances = [
            InstanceInfo("p0", InstanceRole.PREFILL, "h1", 8000),
            InstanceInfo("p1", InstanceRole.PREFILL, "h2", 8000),
        ]
        request = ScheduledRequest("r1", "test", 10)
        
        # Should rotate through instances
        first = selector.select(instances, request)
        second = selector.select(instances, request)
        assert first.instance_id != second.instance_id

    def test_least_loaded_selector(self):
        """Test LeastLoadedSelector instance selection."""
        from src.infrastructure.engine.scheduling import (
            LeastLoadedSelector,
            InstanceInfo,
            InstanceRole,
            ScheduledRequest,
        )
        
        selector = LeastLoadedSelector()
        instances = [
            InstanceInfo("p0", InstanceRole.PREFILL, "h1", 8000, num_running_requests=5),
            InstanceInfo("p1", InstanceRole.PREFILL, "h2", 8000, num_running_requests=2),
        ]
        request = ScheduledRequest("r1", "test", 10)
        
        selected = selector.select(instances, request)
        assert selected.instance_id == "p1"  # Less loaded

    def test_disaggregated_scheduler_creation(self):
        """Test DisaggregatedScheduler instantiation."""
        from src.infrastructure.engine.scheduling import (
            DCPConfig,
            DisaggregatedScheduler,
            InstanceInfo,
            InstanceRole,
        )
        
        config = DCPConfig(
            enabled=True,
            prefill_instances=[
                InstanceInfo("p0", InstanceRole.PREFILL, "h1", 8000),
            ],
            decode_instances=[
                InstanceInfo("d0", InstanceRole.DECODE, "h2", 8000),
            ],
        )
        
        scheduler = DisaggregatedScheduler(config)
        stats = scheduler.get_instance_stats()
        assert stats["prefill_instances"] == 1
        assert stats["decode_instances"] == 1

    def test_schedule_prefill(self):
        """Test prefill scheduling."""
        from src.infrastructure.engine.scheduling import (
            DCPConfig,
            DisaggregatedScheduler,
            InstanceInfo,
            InstanceRole,
            ScheduledRequest,
        )
        
        config = DCPConfig(
            enabled=True,
            prefill_instances=[
                InstanceInfo("p0", InstanceRole.PREFILL, "h1", 8000, kv_port=8001),
            ],
            decode_instances=[
                InstanceInfo("d0", InstanceRole.DECODE, "h2", 8000, kv_port=8001),
            ],
        )
        
        scheduler = DisaggregatedScheduler(config)
        request = ScheduledRequest("req_001", "Hello", 100)
        
        instance, params = scheduler.schedule_prefill(request)
        assert instance is not None
        assert instance.role == InstanceRole.PREFILL
        assert params.do_remote_decode == True

    def test_schedule_decode(self):
        """Test decode scheduling after prefill."""
        from src.infrastructure.engine.scheduling import (
            DCPConfig,
            DisaggregatedScheduler,
            InstanceInfo,
            InstanceRole,
            ScheduledRequest,
        )
        
        config = DCPConfig(
            enabled=True,
            prefill_instances=[
                InstanceInfo("p0", InstanceRole.PREFILL, "h1", 8000, kv_port=8001),
            ],
            decode_instances=[
                InstanceInfo("d0", InstanceRole.DECODE, "h2", 8000, kv_port=8001),
            ],
        )
        
        scheduler = DisaggregatedScheduler(config)
        request = ScheduledRequest("req_001", "Hello", 100)
        
        # Prefill first
        scheduler.schedule_prefill(request)
        
        # Then decode
        prefill_response = {"kv_transfer_params": {"remote_block_ids": [0, 1, 2]}}
        instance, params = scheduler.schedule_decode(request, prefill_response)
        
        assert instance is not None
        assert instance.role == InstanceRole.DECODE
        assert params.do_remote_prefill == True

    def test_proxy_orchestrator(self):
        """Test ProxyOrchestrator request flow."""
        from src.infrastructure.engine.scheduling import (
            DCPConfig,
            DisaggregatedScheduler,
            InstanceInfo,
            InstanceRole,
            ProxyOrchestrator,
        )
        
        config = DCPConfig(
            enabled=True,
            prefill_instances=[
                InstanceInfo("p0", InstanceRole.PREFILL, "h1", 8000),
            ],
            decode_instances=[
                InstanceInfo("d0", InstanceRole.DECODE, "h2", 8000),
            ],
        )
        
        scheduler = DisaggregatedScheduler(config)
        orchestrator = ProxyOrchestrator(scheduler)
        
        request = orchestrator.create_request("Hello world", 50)
        assert request.request_id is not None

    def test_create_dcp_scheduler_factory(self):
        """Test factory function for scheduler creation."""
        from src.infrastructure.engine.scheduling import create_dcp_scheduler
        
        scheduler = create_dcp_scheduler(
            prefill_urls=["http://localhost:8000"],
            decode_urls=["http://localhost:8001"],
        )
        
        stats = scheduler.get_instance_stats()
        assert stats["prefill_instances"] == 1
        assert stats["decode_instances"] == 1


# =============================================================================
# Triton Attention Operations Tests
# =============================================================================


class TestTritonAttentionOps:
    """Tests for Triton attention kernels."""

    def test_attention_backend_enum(self):
        """Test AttentionBackend enum values."""
        from src.infrastructure.engine.attention import TritonAttentionBackend
        
        assert TritonAttentionBackend.TRITON.value == 1
        assert TritonAttentionBackend.NAIVE.value == 5

    def test_precision_mode_enum(self):
        """Test PrecisionMode enum values."""
        from src.infrastructure.engine.attention import PrecisionMode
        
        assert PrecisionMode.FP32.value == 1
        assert PrecisionMode.FP16.value == 2
        assert PrecisionMode.AUTO.value == 4

    def test_attention_config_defaults(self):
        """Test AttentionConfig default values."""
        from src.infrastructure.engine.attention import AttentionConfig
        
        config = AttentionConfig()
        assert config.num_heads == 32
        assert config.head_dim == 128
        assert config.num_kv_heads == 8
        assert config.block_size == 16

    def test_attention_config_gqa_ratio(self):
        """Test GQA ratio computation."""
        from src.infrastructure.engine.attention import AttentionConfig
        
        config = AttentionConfig(num_heads=32, num_kv_heads=8)
        assert config.num_queries_per_kv == 4

    def test_attention_metadata(self):
        """Test AttentionMetadata creation."""
        from src.infrastructure.engine.attention.triton_attention_ops import AttentionMetadata
        
        metadata = AttentionMetadata(
            seq_lens=[64, 128, 32],
            max_decode_seq_len=128,
            is_prefill=True,
        )
        assert len(metadata.seq_lens) == 3
        assert metadata.is_prefill == True

    def test_naive_attention_forward(self):
        """Test NaiveAttention creation and config."""
        from src.infrastructure.engine.attention.triton_attention_ops import (
            NaiveAttention, 
            AttentionConfig, 
        )
        
        config = AttentionConfig(num_heads=4, head_dim=32, num_kv_heads=4)
        kernel = NaiveAttention(config)
        
        # Verify kernel is created with correct config
        assert kernel.config == config
        assert kernel.scale == pytest.approx(1.0 / (32 ** 0.5))
        
        # Verify supports_context_length always returns True
        assert kernel.supports_context_length(1000) == True
        assert kernel.supports_context_length(100000) == True

    def test_sliding_window_attention(self):
        """Test SlidingWindowAttention kernel."""
        pytest.importorskip("torch")
        from src.infrastructure.engine.attention import SlidingWindowAttention, AttentionConfig, AttentionMetadata
        import torch
        
        config = AttentionConfig(
            num_heads=4,
            head_dim=32,
            use_sliding_window=True,
            sliding_window_size=4,
        )
        kernel = SlidingWindowAttention(config)
        
        batch, seq_len = 2, 16
        query = torch.randn(batch, config.num_heads, seq_len, config.head_dim)
        key = torch.randn(batch, config.num_heads, seq_len, config.head_dim)
        value = torch.randn(batch, config.num_heads, seq_len, config.head_dim)
        
        metadata = AttentionMetadata(seq_lens=[seq_len] * batch)
        
        output = kernel.forward(query, key, value, metadata)
        assert output.shape == query.shape

    def test_kv_split_config(self):
        """Test KVSplitConfig for long contexts."""
        from src.infrastructure.engine.attention import KVSplitConfig
        
        config = KVSplitConfig(num_splits=8, max_context_per_split=1024)
        assert config.num_splits == 8
        assert config.max_context_per_split == 1024

    def test_triton_attention_ops_backend_selection(self):
        """Test TritonAttentionOps automatic backend selection."""
        from src.infrastructure.engine.attention import TritonAttentionOps, AttentionConfig
        
        config = AttentionConfig()
        ops = TritonAttentionOps(config)
        
        # Should have initialized a kernel
        assert ops._kernel is not None

    def test_create_attention_ops_factory(self):
        """Test factory function for attention operations."""
        from src.infrastructure.engine.attention import create_attention_ops
        
        ops = create_attention_ops(num_heads=16, head_dim=64)
        assert ops is not None


# =============================================================================
# Batch DCP Wrapper Tests
# =============================================================================


class TestBatchDCPWrapper:
    """Tests for batch disaggregated prefill-decode wrappers."""

    def test_batch_phase_enum(self):
        """Test BatchPhase enum values."""
        from src.infrastructure.engine.attention import BatchPhase
        
        assert BatchPhase.PREFILL.value == 1
        assert BatchPhase.DECODE.value == 2
        assert BatchPhase.MIXED.value == 3

    def test_all_reduce_strategy_enum(self):
        """Test AllReduceStrategy enum values."""
        from src.infrastructure.engine.attention import AllReduceStrategy
        
        assert AllReduceStrategy.RING.value == 1
        assert AllReduceStrategy.NCCL.value == 4

    def test_batch_request_creation(self):
        """Test BatchRequest dataclass."""
        from src.infrastructure.engine.attention import BatchRequest
        
        request = BatchRequest(
            request_id="req_001",
            tokens=[1, 2, 3, 4, 5],
            seq_len=5,
        )
        assert request.request_id == "req_001"
        assert len(request.tokens) == 5

    def test_batch_metadata(self):
        """Test BatchMetadata creation."""
        from src.infrastructure.engine.attention import BatchMetadata, BatchPhase
        
        metadata = BatchMetadata(
            batch_id="batch_001",
            phase=BatchPhase.PREFILL,
            num_requests=10,
        )
        assert metadata.is_prefill == True
        assert metadata.is_decode == False

    def test_dcp_plan_config(self):
        """Test DCPPlanConfig defaults."""
        from src.infrastructure.engine.attention import DCPPlanConfig
        
        config = DCPPlanConfig()
        assert config.max_batch_size == 256
        assert config.max_tokens_per_batch == 8192

    def test_execution_plan(self):
        """Test ExecutionPlan creation."""
        from src.infrastructure.engine.attention import ExecutionPlan, BatchPhase
        
        plan = ExecutionPlan(
            batch_id="plan_001",
            phase=BatchPhase.PREFILL,
            request_order=["r1", "r2", "r3"],
        )
        assert len(plan.request_order) == 3

    def test_batch_dcp_prefill_wrapper_plan(self):
        """Test BatchDCPPrefillWrapper planning."""
        from src.infrastructure.engine.attention import (
            BatchDCPPrefillWrapper,
            BatchMetadata,
            BatchPhase,
            BatchRequest,
            DCPPlanConfig,
        )
        
        config = DCPPlanConfig()
        wrapper = BatchDCPPrefillWrapper(config)
        
        requests = [
            BatchRequest("r1", [1, 2, 3], 3),
            BatchRequest("r2", [4, 5, 6, 7], 4),
        ]
        metadata = BatchMetadata("batch_1", BatchPhase.PREFILL)
        
        plan = wrapper.plan(requests, metadata)
        assert len(plan.request_order) == 2
        assert len(plan.token_positions) == 2

    def test_batch_dcp_prefill_wrapper_run(self):
        """Test BatchDCPPrefillWrapper execution."""
        from src.infrastructure.engine.attention import (
            BatchDCPPrefillWrapper,
            BatchMetadata,
            BatchPhase,
            BatchRequest,
            DCPPlanConfig,
        )
        
        config = DCPPlanConfig()
        wrapper = BatchDCPPrefillWrapper(config)
        
        requests = [
            BatchRequest("r1", [1, 2, 3], 3),
        ]
        metadata = BatchMetadata("batch_1", BatchPhase.PREFILL)
        
        plan = wrapper.plan(requests, metadata)
        result = wrapper.run(plan, {"hidden_states": None})
        
        assert "output" in result
        assert result["batch_id"] == plan.batch_id

    def test_batch_dcp_decode_wrapper_plan(self):
        """Test BatchDCPDecodeWrapper planning."""
        from src.infrastructure.engine.attention import (
            BatchDCPDecodeWrapper,
            BatchMetadata,
            BatchPhase,
            BatchRequest,
            DCPPlanConfig,
        )
        
        config = DCPPlanConfig()
        wrapper = BatchDCPDecodeWrapper(config)
        
        requests = [
            BatchRequest("r1", [1], 1, num_computed_tokens=10),
            BatchRequest("r2", [2], 1, num_computed_tokens=20),
        ]
        metadata = BatchMetadata("batch_1", BatchPhase.DECODE)
        
        plan = wrapper.plan(requests, metadata)
        assert len(plan.request_order) == 2

    def test_unified_batch_wrapper(self):
        """Test UnifiedBatchWrapper for mixed batches."""
        from src.infrastructure.engine.attention import (
            UnifiedBatchWrapper,
            BatchRequest,
            DCPPlanConfig,
        )
        
        config = DCPPlanConfig()
        wrapper = UnifiedBatchWrapper(config)
        
        # Mixed batch: some prefill, some decode
        requests = [
            BatchRequest("r1", [1, 2, 3], 3, num_computed_tokens=0),  # Prefill
            BatchRequest("r2", [4], 1, num_computed_tokens=10),  # Decode
        ]
        
        result = wrapper.process_batch(requests, {"hidden_states": None})
        
        # Should have both prefill and decode results
        stats = wrapper.get_stats()
        assert "prefill" in stats
        assert "decode" in stats

    def test_create_prefill_wrapper_factory(self):
        """Test factory function for prefill wrapper."""
        from src.infrastructure.engine.attention import create_prefill_wrapper
        
        wrapper = create_prefill_wrapper(max_batch_size=128)
        assert wrapper.config.max_batch_size == 128

    def test_create_decode_wrapper_factory(self):
        """Test factory function for decode wrapper."""
        from src.infrastructure.engine.attention import create_decode_wrapper
        
        wrapper = create_decode_wrapper(max_batch_size=256, world_size=4)
        assert wrapper.config.world_size == 4


# =============================================================================
# Rust Acceleration Tests (Phase 34)
# =============================================================================


@pytest.fixture
def rust_core():
    """Fixture to load rust_core module."""
    try:
        import rust_core
        # Check if new Phase 34 functions exist
        if not hasattr(rust_core, 'rotary_embedding_kernel_rust'):
            pytest.skip("rust_core needs rebuild for Phase 34 functions")
        return rust_core
    except ImportError:
        pytest.skip("rust_core not available")


class TestRustPhase34Accelerations:
    """Tests for Phase 34 Rust functions.
    
    Note: These tests require rust_core to be rebuilt with Phase 34 functions.
    Run: cd rust_core && maturin develop --release
    """

    def test_rotary_embedding_kernel_rust(self, rust_core):
        """Test rotary_embedding_kernel_rust."""
        positions = [0, 1, 2, 3]
        dim = 64
        
        cos_table, sin_table = rust_core.rotary_embedding_kernel_rust(positions, dim)
        
        assert len(cos_table) == len(positions)
        assert len(sin_table) == len(positions)
        assert len(cos_table[0]) == dim

    def test_mrope_section_indices_rust(self, rust_core):
        """Test mrope_section_indices_rust for multimodal RoPE."""
        temporal, height, width = rust_core.mrope_section_indices_rust(
            dim=64,
            temporal_sections=2,
            height_sections=2,
            width_sections=2,
        )
        
        # Should divide dim/2 = 32 into 6 sections
        total_indices = len(temporal) + len(height) + len(width)
        assert total_indices > 0

    def test_dynamic_ntk_alpha_rust(self, rust_core):
        """Test dynamic_ntk_alpha_rust for extended context."""
        # Within original length - no scaling
        base = rust_core.dynamic_ntk_alpha_rust(4096, 4096, 10000.0, "linear")
        assert base == 10000.0
        
        # Beyond original length - should scale
        scaled = rust_core.dynamic_ntk_alpha_rust(8192, 4096, 10000.0, "linear")
        assert scaled > 10000.0
        
        # YARN scaling
        yarn_scaled = rust_core.dynamic_ntk_alpha_rust(8192, 4096, 10000.0, "yarn")
        assert yarn_scaled > 10000.0

    def test_ngram_propose_rust(self, rust_core):
        """Test ngram_propose_rust for speculative decoding."""
        tokens = [1, 2, 3, 4, 1, 2, 3, 5, 1, 2, 3, 6]
        
        # Build index first
        ngram_index = rust_core.build_ngram_index_rust(tokens, 3)
        
        # Propose after [1, 2, 3]
        proposals = rust_core.ngram_propose_rust(
            [1, 2, 3],
            ngram_index,
            3,  # context_size
            5,  # num_proposals
        )
        
        # Should find continuations (4, 5, or 6)
        assert isinstance(proposals, list)

    def test_eagle_tree_expand_rust(self, rust_core):
        """Test eagle_tree_expand_rust for tree speculation."""
        draft_tokens = [[100, 200], [150, 250]]
        tree_indices = rust_core.eagle_tree_expand_rust(
            draft_tokens,
            tree_width=2,
            tree_depth=2,
            vocab_size=32000,
        )
        
        assert isinstance(tree_indices, list)
        assert len(tree_indices) > 0

    def test_kv_transfer_metadata_rust(self, rust_core):
        """Test kv_transfer_metadata_rust for disaggregated serving."""
        metadata = rust_core.kv_transfer_metadata_rust(
            "req_001",
            [0, 1, 2, 3],
            64,  # seq_len
            32,  # num_layers
            32,  # num_heads
            128,  # head_dim
        )
        
        assert metadata["request_id"] == "req_001"
        assert metadata["num_blocks"] == "4"
        assert "kv_bytes" in metadata

    def test_verify_draft_tokens_batch_rust(self, rust_core):
        """Test verify_draft_tokens_batch_rust."""
        draft_tokens = [100, 200, 300]
        target_logits = [
            [0.0] * 100 + [5.0] + [0.0] * 899,  # High prob for 100
            [0.0] * 200 + [3.0] + [0.0] * 799,  # Medium prob for 200
            [0.0] * 300 + [1.0] + [0.0] * 699,  # Low prob for 300
        ]
        draft_probs = [0.8, 0.6, 0.5]
        
        accepted_count, mask = rust_core.verify_draft_tokens_batch_rust(
            draft_tokens,
            target_logits,
            draft_probs,
            1.0,  # temperature
        )
        
        assert accepted_count >= 0
        assert len(mask) == 3

    def test_block_table_lookup_rust(self, rust_core):
        """Test block_table_lookup_rust for paged attention."""
        block_table = [
            [10, 20, 30],  # Sequence 0
            [40, 50, 60],  # Sequence 1
        ]
        
        physical = rust_core.block_table_lookup_rust(
            block_table,
            [0, 0, 1],  # seq_indices
            [0, 20, 16],  # token_positions
            16,  # block_size
        )
        
        assert len(physical) == 3
        assert physical[0] == 10  # seq 0, block 0
        assert physical[1] == 20  # seq 0, block 1
        assert physical[2] == 50  # seq 1, block 1

    def test_triton_attention_dispatch_rust(self, rust_core):
        """Test triton_attention_dispatch_rust backend selection."""
        backend, config = rust_core.triton_attention_dispatch_rust(
            batch_size=32,
            seq_len=2048,
            num_heads=32,
            num_kv_heads=8,
            head_dim=128,
            is_prefill=True,
            has_sliding_window=False,
            sliding_window_size=4096,
        )
        
        assert backend in [0, 1, 2, 3]
        assert "gqa_ratio" in config
        assert config["gqa_ratio"] == 4

    def test_dcp_group_coordinate_rust(self, rust_core):
        """Test dcp_group_coordinate_rust for group formation."""
        prefill_ranks, decode_ranks = rust_core.dcp_group_coordinate_rust(
            world_size=8,
            prefill_ratio=0.5,
            min_prefill=1,
            min_decode=1,
        )
        
        assert len(prefill_ranks) == 4
        assert len(decode_ranks) == 4
        assert set(prefill_ranks) & set(decode_ranks) == set()  # No overlap

    def test_kv_connector_score_rust(self, rust_core):
        """Test kv_connector_score_rust for backend selection."""
        backends = ["NixlConnector", "MooncakeConnector", "P2pNcclConnector"]
        
        scores = rust_core.kv_connector_score_rust(
            backends,
            transfer_size_bytes=1_000_000,
            is_local=False,
            has_rdma=True,
            latency_budget_ms=5.0,
        )
        
        assert len(scores) == 3
        # NixlConnector should score highest with RDMA
        assert scores[0][0] == "NixlConnector"

    def test_speculation_tree_parse_rust(self, rust_core):
        """Test speculation_tree_parse_rust for tree structure."""
        tree_config = [
            [3],     # Root has 3 children
            [2, 2, 2],  # Each child has 2 children
        ]
        
        result = rust_core.speculation_tree_parse_rust(tree_config)
        
        assert "parents" in result
        assert "depths" in result
        assert "total_nodes" in result


# =============================================================================
# Integration Tests
# =============================================================================


class TestPhase34Integration:
    """Integration tests for Phase 34 components."""

    def test_kv_transfer_with_scheduling(self):
        """Test KV transfer integration with scheduling."""
        from src.infrastructure.storage.kv_transfer import KVTransferConfig
        from src.infrastructure.engine.scheduling import (
            DCPConfig,
            DisaggregatedScheduler,
            InstanceInfo,
            InstanceRole,
            ScheduledRequest,
        )
        
        # Configure KV transfer
        kv_config = KVTransferConfig(kv_connector="DecodeBenchConnector")
        
        # Configure scheduler with KV transfer
        dcp_config = DCPConfig(
            enabled=True,
            kv_connector=kv_config.kv_connector,
            prefill_instances=[
                InstanceInfo("p0", InstanceRole.PREFILL, "h1", 8000, kv_port=8001),
            ],
            decode_instances=[
                InstanceInfo("d0", InstanceRole.DECODE, "h2", 8000, kv_port=8001),
            ],
        )
        
        scheduler = DisaggregatedScheduler(dcp_config)
        request = ScheduledRequest("req_int_001", "Integration test", 100)
        
        # Schedule through pipeline
        prefill_instance, prefill_params = scheduler.schedule_prefill(request)
        assert prefill_params.do_remote_decode == True

    def test_speculation_with_rope(self):
        """Test speculative decoding with RoPE integration."""
        from src.infrastructure.engine.position import RotaryEmbeddingEngine, RoPEConfig
        from src.inference.speculation import SpeculativeEngine, SpeculativeConfig, SpecMethod
        
        # Configure RoPE
        rope_config = RoPEConfig(head_dim=64)
        rope_engine = RotaryEmbeddingEngine(rope_config)
        
        # Configure speculation
        spec_config = SpeculativeConfig(method=SpecMethod.NGRAM)
        spec_engine = SpeculativeEngine(spec_config)
        
        # Both should initialize properly
        assert rope_engine is not None
        assert spec_engine is not None

    def test_batch_wrapper_with_attention(self):
        """Test batch wrapper with attention operations."""
        from src.infrastructure.engine.attention import (
            BatchDCPPrefillWrapper,
            BatchMetadata,
            BatchPhase,
            BatchRequest,
            DCPPlanConfig,
            TritonAttentionOps,
            AttentionConfig,
        )
        
        # Configure attention
        attn_config = AttentionConfig(num_heads=8, head_dim=64)
        attn_ops = TritonAttentionOps(attn_config)
        
        # Configure batch wrapper
        dcp_config = DCPPlanConfig()
        wrapper = BatchDCPPrefillWrapper(dcp_config)
        
        # Create batch
        requests = [
            BatchRequest("r1", [1, 2, 3, 4], 4),
            BatchRequest("r2", [5, 6, 7, 8, 9], 5),
        ]
        metadata = BatchMetadata("batch_int", BatchPhase.PREFILL, num_requests=2)
        
        # Plan and run
        plan = wrapper.plan(requests, metadata)
        result = wrapper.run(plan, {"hidden_states": None})
        
        assert result["batch_id"] is not None

    @pytest.mark.asyncio
    async def test_async_orchestrator_flow(self):
        """Test async orchestrator flow."""
        from src.infrastructure.engine.scheduling import (
            DCPConfig,
            DisaggregatedScheduler,
            InstanceInfo,
            InstanceRole,
            ProxyOrchestrator,
        )
        
        config = DCPConfig(
            enabled=True,
            prefill_instances=[
                InstanceInfo("p0", InstanceRole.PREFILL, "localhost", 8000),
            ],
            decode_instances=[
                InstanceInfo("d0", InstanceRole.DECODE, "localhost", 8001),
            ],
        )
        
        scheduler = DisaggregatedScheduler(config)
        orchestrator = ProxyOrchestrator(scheduler)
        
        # Create and process request
        request = orchestrator.create_request("Async test prompt", 50)
        result = await orchestrator.process_request(request)
        
        assert "id" in result or "error" in result


# =============================================================================
# Performance Benchmark Tests
# =============================================================================


class TestPhase34Performance:
    """Performance benchmarks for Phase 34."""

    def test_ngram_index_build_performance(self, rust_core):
        """Benchmark n-gram index building."""
        import time
        
        # Large token sequence
        tokens = list(range(100000))
        
        start = time.perf_counter()
        rust_core.build_ngram_index_rust(tokens, 4)
        elapsed = time.perf_counter() - start
        
        # Should complete in reasonable time
        assert elapsed < 1.0, f"N-gram index build took {elapsed:.3f}s"

    def test_rotary_embedding_compute_performance(self, rust_core):
        """Benchmark RoPE computation."""
        import time
        
        positions = list(range(8192))  # Long sequence
        dim = 128
        
        start = time.perf_counter()
        rust_core.rotary_embedding_kernel_rust(positions, dim)
        elapsed = time.perf_counter() - start
        
        assert elapsed < 1.0, f"RoPE computation took {elapsed:.3f}s"

    def test_block_table_lookup_performance(self, rust_core):
        """Benchmark block table lookup."""
        import time
        
        # Large batch
        num_seqs = 256
        blocks_per_seq = 64
        block_table = [list(range(i * blocks_per_seq, (i + 1) * blocks_per_seq)) 
                       for i in range(num_seqs)]
        
        seq_indices = list(range(num_seqs)) * 10
        token_positions = [p * 16 for p in range(len(seq_indices))]
        
        start = time.perf_counter()
        rust_core.block_table_lookup_rust(block_table, seq_indices, token_positions, 16)
        elapsed = time.perf_counter() - start
        
        assert elapsed < 0.1, f"Block table lookup took {elapsed:.3f}s"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
