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
Phase 25: Speculative Decoding & Inference Acceleration Tests.

Tests for:
- SpeculativeDecoder
- PrefixCache
- KVCacheManager
- SchedulerStats
"""

from __future__ import annotations

import time

import numpy as np
import pytest


# =============================================================================
# SpeculativeDecoder Tests
# =============================================================================

class TestSpeculativeDecoder:
    """Tests for SpeculativeDecoder module."""

    def test_speculative_config_defaults(self):
        """Test SpeculativeConfig default values."""
        from src.infrastructure.engine.inference.speculative_decoder import SpeculativeConfig

        config = SpeculativeConfig()
        assert config.num_speculative_tokens == 5
        assert config.prompt_lookup_min == 3
        assert config.prompt_lookup_max == 5

    def test_speculative_config_custom(self):
        """Test SpeculativeConfig custom values."""
        from src.infrastructure.engine.inference.speculative_decoder import (
            SpeculativeConfig,
            SpecMethod,
        )

        config = SpeculativeConfig(
            method=SpecMethod.SUFFIX,
            num_speculative_tokens=8,
            prompt_lookup_min=4,
            prompt_lookup_max=8,
            max_tree_depth=32,
        )
        assert config.num_speculative_tokens == 8
        assert config.method == SpecMethod.SUFFIX
        assert config.max_tree_depth == 32

    def test_speculative_config_should_disable(self):
        """Test SpeculativeConfig batch size disabling."""
        from src.infrastructure.engine.inference.speculative_decoder import SpeculativeConfig

        config = SpeculativeConfig(disable_by_batch_size=32)
        assert config.should_disable(16) is False
        assert config.should_disable(32) is True
        assert config.should_disable(64) is True

    def test_draft_proposal_dataclass(self):
        """Test DraftProposal dataclass."""
        from src.infrastructure.engine.inference.speculative_decoder import DraftProposal

        proposal = DraftProposal(
            request_id="req-123",
            token_ids=[1, 2, 3],
            logprobs=[-0.1, -0.2, -0.3],
        )
        assert proposal.num_tokens == 3
        assert proposal.request_id == "req-123"
        assert proposal.is_empty() is False

    def test_draft_proposal_empty(self):
        """Test DraftProposal empty check."""
        from src.infrastructure.engine.inference.speculative_decoder import DraftProposal

        proposal = DraftProposal(request_id="req-456", token_ids=[])
        assert proposal.is_empty() is True
        assert proposal.num_tokens == 0

    def test_verification_result_dataclass(self):
        """Test VerificationResult dataclass."""
        from src.infrastructure.engine.inference.speculative_decoder import VerificationResult

        result = VerificationResult(
            request_id="req-123",
            num_draft_tokens=5,
            num_accepted_tokens=3,
            accepted_token_ids=[1, 2, 3],
            rejected_at_position=3,
            bonus_token_id=4,
        )
        assert result.num_accepted_tokens == 3
        assert result.acceptance_rate == 0.6
        assert result.all_accepted is False
        assert result.bonus_token_id == 4

    def test_verification_result_all_accepted(self):
        """Test VerificationResult all accepted case."""
        from src.infrastructure.engine.inference.speculative_decoder import VerificationResult

        result = VerificationResult(
            request_id="req-123",
            num_draft_tokens=5,
            num_accepted_tokens=5,
            accepted_token_ids=[1, 2, 3, 4, 5],
        )
        assert result.all_accepted is True
        assert result.acceptance_rate == 1.0

    def test_spec_decoding_metrics(self):
        """Test SpecDecodingMetrics tracking."""
        from src.infrastructure.engine.inference.speculative_decoder import SpecDecodingMetrics

        metrics = SpecDecodingMetrics.new(num_spec_tokens=5)
        metrics.observe_draft(
            num_draft_tokens=5,
            num_accepted_tokens=3,
            accepted_positions=[0, 1, 2],
        )

        assert metrics.num_drafts == 1
        assert metrics.num_draft_tokens == 5
        assert metrics.num_accepted_tokens == 3
        assert metrics.acceptance_rate == 0.6
        assert metrics.accepted_per_position[0] == 1
        assert metrics.accepted_per_position[2] == 1

    def test_spec_method_enum(self):
        """Test SpecMethod enumeration."""
        from src.infrastructure.engine.inference.speculative_decoder import SpecMethod

        assert SpecMethod.NGRAM.value == "ngram"
        assert SpecMethod.SUFFIX.value == "suffix"
        assert SpecMethod.DRAFT_MODEL.value == "draft_model"
        assert SpecMethod.EAGLE.value == "eagle"
        assert SpecMethod.MEDUSA.value == "medusa"


# =============================================================================
# PrefixCache Tests
# =============================================================================

class TestPrefixCache:
    """Tests for PrefixCache module."""

    def test_prefix_cache_config_defaults(self):
        """Test PrefixCacheConfig default values."""
        from src.infrastructure.storage.cache.prefix_cache import PrefixCacheConfig

        config = PrefixCacheConfig()
        assert config.block_size == 16
        assert config.max_blocks == 10000
        assert config.eviction_policy.value == "lru"

    def test_prefix_cache_config_custom(self):
        """Test PrefixCacheConfig custom values."""
        from src.infrastructure.storage.cache.prefix_cache import (
            PrefixCacheConfig,
            EvictionPolicy,
        )

        config = PrefixCacheConfig(
            block_size=32,
            max_blocks=5000,
            eviction_policy=EvictionPolicy.LFU,
            enable_sharing=False,
        )
        assert config.block_size == 32
        assert config.max_blocks == 5000
        assert config.eviction_policy == EvictionPolicy.LFU
        assert config.enable_sharing is False

    def test_cache_block_creation(self):
        """Test CacheBlock creation."""
        from src.infrastructure.storage.cache.prefix_cache import CacheBlock

        block = CacheBlock(
            block_id=1,
            token_ids=(1, 2, 3, 4),
            block_hash="abc123",
        )
        assert block.block_id == 1
        assert block.token_ids == (1, 2, 3, 4)
        assert block.ref_count == 1
        assert block.is_pinned is False

    def test_cache_block_touch(self):
        """Test CacheBlock touch updates access time."""
        from src.infrastructure.storage.cache.prefix_cache import CacheBlock

        block = CacheBlock(block_id=1, token_ids=(1, 2, 3, 4), block_hash="abc123")
        old_time = block.last_access
        time.sleep(0.01)
        block.touch()

        assert block.last_access > old_time
        assert block.access_count == 1

    def test_cache_block_acquire_release(self):
        """Test CacheBlock reference counting."""
        from src.infrastructure.storage.cache.prefix_cache import CacheBlock

        block = CacheBlock(block_id=1, token_ids=(1, 2, 3, 4), block_hash="abc123")
        assert block.ref_count == 1

        block.acquire()
        assert block.ref_count == 2

        can_free = block.release()
        assert can_free is False
        assert block.ref_count == 1

        can_free = block.release()
        assert can_free is True
        assert block.ref_count == 0

    def test_prefix_cache_stats(self):
        """Test PrefixCacheStats tracking."""
        from src.infrastructure.storage.cache.prefix_cache import PrefixCacheStats

        stats = PrefixCacheStats()
        stats.record(num_tokens=100, num_hits=75)

        assert stats.num_tokens == 100
        assert stats.num_hits == 75
        assert stats.num_misses == 25
        assert stats.hit_rate == 0.75

    def test_prefix_cache_stats_reset(self):
        """Test PrefixCacheStats reset."""
        from src.infrastructure.storage.cache.prefix_cache import PrefixCacheStats

        stats = PrefixCacheStats()
        stats.record(num_tokens=100, num_hits=75)
        stats.reset()

        assert stats.num_tokens == 0
        assert stats.num_hits == 0
        assert stats.hit_rate == 0.0

    def test_compute_block_hash(self):
        """Test compute_block_hash function."""
        from src.infrastructure.storage.cache.prefix_cache import compute_block_hash

        tokens = (1, 2, 3, 4)
        hash1 = compute_block_hash(tokens)
        hash2 = compute_block_hash(tokens)

        assert hash1 == hash2
        assert len(hash1) > 0

    def test_compute_block_hash_different_tokens(self):
        """Test compute_block_hash with different tokens."""
        from src.infrastructure.storage.cache.prefix_cache import compute_block_hash

        hash1 = compute_block_hash((1, 2, 3, 4))
        hash2 = compute_block_hash((1, 2, 3, 5))

        assert hash1 != hash2

    def test_eviction_policy_enum(self):
        """Test EvictionPolicy enumeration."""
        from src.infrastructure.storage.cache.prefix_cache import EvictionPolicy

        assert EvictionPolicy.LRU.value == "lru"
        assert EvictionPolicy.LFU.value == "lfu"
        assert EvictionPolicy.ARC.value == "arc"
        assert EvictionPolicy.FIFO.value == "fifo"


# =============================================================================
# KVCacheManager Tests
# =============================================================================

class TestKVCacheManager:
    """Tests for KVCacheManager module."""

    def test_kv_cache_config_creation(self):
        """Test KVCacheConfig creation with required args."""
        from src.infrastructure.storage.cache.kv_cache_manager import KVCacheConfig

        config = KVCacheConfig(
            num_layers=32,
            num_heads=32,
            head_dim=128,
        )
        assert config.num_layers == 32
        assert config.num_heads == 32
        assert config.head_dim == 128
        assert config.block_size == 16

    def test_kv_cache_config_kv_size(self):
        """Test KVCacheConfig KV size calculation."""
        from src.infrastructure.storage.cache.kv_cache_manager import KVCacheConfig, DType

        config = KVCacheConfig(
            num_layers=2,
            num_heads=4,
            head_dim=64,
            dtype=DType.FLOAT16,
        )
        # K + V for all layers and heads: 2 * 2 * 4 * 64 * 2 = 2048 bytes
        assert config.kv_size_per_token == 2048

    def test_device_type_enum(self):
        """Test DeviceType enumeration."""
        from src.infrastructure.storage.cache.kv_cache_manager import DeviceType

        assert DeviceType.CPU.value == "cpu"
        assert DeviceType.CUDA.value == "cuda"
        assert DeviceType.MPS.value == "mps"

    def test_dtype_enum(self):
        """Test DType enumeration."""
        from src.infrastructure.storage.cache.kv_cache_manager import DType

        assert DType.FLOAT16.value == "float16"
        assert DType.FLOAT32.value == "float32"
        assert DType.BFLOAT16.value == "bfloat16"
        assert DType.INT8.value == "int8"

    def test_kv_cache_block_creation(self):
        """Test KVCacheBlock creation."""
        from src.infrastructure.storage.cache.kv_cache_manager import KVCacheBlock, DeviceType

        block = KVCacheBlock(
            block_id=0,
            layer_idx=0,
            device=DeviceType.CPU,
        )

        assert block.block_id == 0
        assert block.layer_idx == 0
        assert block.is_allocated is False
        assert block.ref_count == 0

    def test_kv_cache_block_allocate(self):
        """Test KVCacheBlock allocation."""
        from src.infrastructure.storage.cache.kv_cache_manager import KVCacheBlock, DeviceType

        block = KVCacheBlock(
            block_id=0,
            layer_idx=0,
            device=DeviceType.CPU,
        )

        block.allocate(
            num_heads=4,
            head_dim=64,
            block_size=16,
            dtype=np.float16,
        )

        assert block.is_allocated is True
        assert block.key_cache.shape == (16, 4, 64)
        assert block.value_cache.shape == (16, 4, 64)

    def test_kv_cache_block_acquire_release(self):
        """Test KVCacheBlock reference counting."""
        from src.infrastructure.storage.cache.kv_cache_manager import KVCacheBlock, DeviceType

        block = KVCacheBlock(block_id=0, layer_idx=0, device=DeviceType.CPU)
        assert block.ref_count == 0

        block.acquire()
        assert block.ref_count == 1

        can_free = block.release()
        assert can_free is True
        assert block.ref_count == 0

    def test_kv_cache_block_free(self):
        """Test KVCacheBlock free."""
        from src.infrastructure.storage.cache.kv_cache_manager import KVCacheBlock, DeviceType

        block = KVCacheBlock(block_id=0, layer_idx=0, device=DeviceType.CPU)
        block.allocate(num_heads=4, head_dim=64, block_size=16, dtype=np.float16)

        assert block.is_allocated is True

        block.free()

        assert block.is_allocated is False
        assert block.key_cache is None
        assert block.value_cache is None

    def test_kv_cache_blocks_collection(self):
        """Test KVCacheBlocks collection."""
        from src.infrastructure.storage.cache.kv_cache_manager import KVCacheBlocks

        blocks = KVCacheBlocks()
        assert blocks.num_blocks == 0

        blocks.append_gpu(0)
        blocks.append_gpu(1)
        blocks.append_cpu(10)

        assert blocks.num_blocks == 3
        assert len(blocks.gpu_blocks) == 2
        assert len(blocks.cpu_blocks) == 1


# =============================================================================
# SchedulerStats Tests
# =============================================================================

class TestSchedulerStats:
    """Tests for SchedulerStats module."""

    def test_prefix_cache_stats_init(self):
        """Test PrefixCacheStats initialization."""
        from src.observability.stats.scheduler_stats import PrefixCacheStats

        stats = PrefixCacheStats()
        assert stats.num_tokens == 0
        assert stats.num_hits == 0
        assert stats.hit_rate == 0.0

    def test_prefix_cache_stats_record(self):
        """Test PrefixCacheStats recording."""
        from src.observability.stats.scheduler_stats import PrefixCacheStats

        stats = PrefixCacheStats()
        stats.record(num_tokens=100, num_hits=75)

        assert stats.num_tokens == 100
        assert stats.num_hits == 75
        assert stats.num_misses == 25
        assert stats.hit_rate == 0.75

    def test_spec_decoding_stats_init(self):
        """Test SpecDecodingStats initialization."""
        from src.observability.stats.scheduler_stats import SpecDecodingStats

        stats = SpecDecodingStats.new(num_spec_tokens=5)

        assert stats.num_spec_tokens == 5
        assert len(stats.num_accepted_tokens_per_pos) == 5

    def test_spec_decoding_stats_observe(self):
        """Test SpecDecodingStats observing drafts."""
        from src.observability.stats.scheduler_stats import SpecDecodingStats

        stats = SpecDecodingStats.new(num_spec_tokens=5)
        stats.observe_draft(
            num_draft_tokens=5,
            num_accepted_tokens=3,
            accepted_positions=[0, 1, 2],
        )

        assert stats.num_drafts == 1
        assert stats.num_draft_tokens == 5
        assert stats.num_accepted_tokens == 3
        assert stats.acceptance_rate == 0.6
        assert stats.num_accepted_tokens_per_pos[0] == 1
        assert stats.num_accepted_tokens_per_pos[2] == 1
        assert stats.num_accepted_tokens_per_pos[3] == 0

    def test_cuda_graph_stats(self):
        """Test CUDAGraphStats tracking."""
        from src.observability.stats.scheduler_stats import CUDAGraphStats

        stats = CUDAGraphStats()
        stats.record_capture(time_ms=10.0, memory_mb=100.0)
        stats.record_replay(time_ms=0.5)
        stats.record_replay(time_ms=0.5)

        assert stats.num_captures == 1
        assert stats.num_replays == 2
        assert stats.avg_capture_time_ms == 10.0
        assert stats.avg_replay_time_ms == 0.5

    def test_perf_stats(self):
        """Test PerfStats timing breakdown."""
        from src.observability.stats.scheduler_stats import PerfStats

        stats = PerfStats()
        stats.record_step(schedule_ms=1.0, forward_ms=10.0, sample_ms=0.5)
        stats.record_step(schedule_ms=1.0, forward_ms=10.0, sample_ms=0.5)

        assert stats.num_steps == 2
        assert stats.total_time_ms == pytest.approx(23.0)
        assert stats.avg_step_time_ms == pytest.approx(11.5)

    def test_kv_cache_eviction_event(self):
        """Test KVCacheEvictionEvent creation."""
        from src.observability.stats.scheduler_stats import KVCacheEvictionEvent

        event = KVCacheEvictionEvent.now(
            request_id="req-123",
            num_blocks=5,
            reason="memory_pressure",
        )

        assert event.request_id == "req-123"
        assert event.num_blocks == 5
        assert event.reason == "memory_pressure"
        assert event.timestamp > 0

    def test_scheduler_stats_init(self):
        """Test SchedulerStats initialization."""
        from src.observability.stats.scheduler_stats import SchedulerStats

        stats = SchedulerStats()

        assert stats.num_running_reqs == 0
        assert stats.num_waiting_reqs == 0
        assert stats.kv_cache_usage == 0.0

    def test_scheduler_stats_record_step(self):
        """Test SchedulerStats recording steps."""
        from src.observability.stats.scheduler_stats import SchedulerStats

        stats = SchedulerStats()
        stats.record_step(num_running=10, num_waiting=5, kv_usage=0.75)

        assert stats.step_counter == 1
        assert stats.num_running_reqs == 10
        assert stats.num_waiting_reqs == 5
        assert stats.kv_cache_usage == 0.75

    def test_scheduler_stats_as_dict(self):
        """Test SchedulerStats serialization."""
        from src.observability.stats.scheduler_stats import create_scheduler_stats

        stats = create_scheduler_stats(enable_spec_decoding=True, num_spec_tokens=5)
        stats.record_step(num_running=10, num_waiting=5, kv_usage=0.75)

        d = stats.as_dict()

        assert d["num_running_reqs"] == 10
        assert d["total_requests"] == 15
        assert "spec_decoding" in d
        assert "performance" in d

    def test_scheduler_stats_to_prometheus(self):
        """Test SchedulerStats Prometheus export."""
        from src.observability.stats.scheduler_stats import SchedulerStats

        stats = SchedulerStats()
        stats.record_step(num_running=10, num_waiting=5, kv_usage=0.75)

        prometheus = stats.to_prometheus()

        assert "scheduler_running_requests" in prometheus
        assert "scheduler_waiting_requests" in prometheus
        assert "kv_cache_usage" in prometheus

    def test_scheduler_stats_collector(self):
        """Test SchedulerStatsCollector aggregation."""
        from src.observability.stats.scheduler_stats import create_stats_collector

        collector = create_stats_collector(window_size=10)

        for i in range(5):
            collector.record_step(num_running=i + 1, num_waiting=i, kv_usage=0.1 * (i + 1))
            collector.commit()

        averages = collector.get_averages()

        assert averages["avg_running_reqs"] == 3.0  # (1+2+3+4+5)/5
        assert averages["avg_waiting_reqs"] == 2.0  # (0+1+2+3+4)/5


# =============================================================================
# Integration Tests
# =============================================================================

class TestPhase25Integration:
    """Integration tests for Phase 25 components."""

    def test_speculative_decoder_with_stats(self):
        """Test SpeculativeDecoder with stats tracking."""
        from src.infrastructure.engine.inference.speculative_decoder import (
            SpeculativeConfig,
            SpecDecodingMetrics,
            DraftProposal,
            VerificationResult,
        )

        SpeculativeConfig(num_speculative_tokens=5)
        metrics = SpecDecodingMetrics.new(5)

        # Simulate a draft and verification
        DraftProposal(
            request_id="req-1",
            token_ids=[1, 2, 3, 4, 5],
        )

        result = VerificationResult(
            request_id="req-1",
            num_draft_tokens=5,
            num_accepted_tokens=3,
            accepted_token_ids=[1, 2, 3],
            rejected_at_position=3,
        )

        metrics.observe_draft(
            num_draft_tokens=result.num_draft_tokens,
            num_accepted_tokens=result.num_accepted_tokens,
            accepted_positions=[0, 1, 2],
        )

        assert metrics.num_drafts == 1
        assert metrics.acceptance_rate == 0.6

    def test_prefix_cache_stats_tracking(self):
        """Test PrefixCache with stats tracking."""
        from src.infrastructure.storage.cache.prefix_cache import (
            PrefixCacheConfig,
            PrefixCacheStats,
            compute_block_hash,
        )

        PrefixCacheConfig(max_blocks=100, block_size=16)
        stats = PrefixCacheStats()

        # Simulate cache accesses
        tokens1 = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
        compute_block_hash(tokens1)

        # First access - miss
        stats.record(num_tokens=16, num_hits=0)

        # Second access - hit
        stats.record(num_tokens=16, num_hits=16)

        assert stats.num_tokens == 32
        assert stats.num_hits == 16
        assert stats.num_misses == 16
        assert stats.hit_rate == 0.5

    def test_kv_cache_block_lifecycle(self):
        """Test KVCacheBlock complete lifecycle."""
        from src.infrastructure.storage.cache.kv_cache_manager import (
            KVCacheBlock,
            DeviceType,
        )

        # Create
        block = KVCacheBlock(block_id=0, layer_idx=0, device=DeviceType.CPU)
        assert block.is_allocated is False

        # Allocate
        block.allocate(num_heads=4, head_dim=64, block_size=16, dtype=np.float16)
        assert block.is_allocated is True

        # Acquire
        block.acquire()
        assert block.ref_count == 1

        # Release
        can_free = block.release()
        assert can_free is True

        # Free
        block.free()
        assert block.is_allocated is False

    def test_full_inference_pipeline_stats(self):
        """Test full inference pipeline with comprehensive stats."""
        from src.observability.stats.scheduler_stats import (
            SchedulerStats,
            SpecDecodingStats,
            PerfStats,
        )

        # Create comprehensive stats
        stats = SchedulerStats()
        stats.spec_decoding_stats = SpecDecodingStats.new(5)
        stats.perf_stats = PerfStats()

        # Simulate inference steps
        for step in range(10):
            # Record scheduler state
            stats.record_step(
                num_running=5 + step % 3,
                num_waiting=2 + step % 2,
                kv_usage=0.5 + step * 0.03,
            )

            # Record prefix cache access
            stats.prefix_cache_stats.record(
                num_tokens=16,
                num_hits=12 if step > 0 else 0,
            )

            # Record spec decoding
            if stats.spec_decoding_stats:
                stats.spec_decoding_stats.observe_draft(
                    num_draft_tokens=5,
                    num_accepted_tokens=3,
                    accepted_positions=[0, 1, 2],
                )

            # Record perf
            if stats.perf_stats:
                stats.perf_stats.record_step(
                    schedule_ms=0.5,
                    forward_ms=8.0,
                    sample_ms=0.3,
                )

        # Verify comprehensive stats
        d = stats.as_dict()

        assert d["step_counter"] == 10
        assert d["prefix_cache"]["hit_rate"] > 0
        assert d["spec_decoding"]["acceptance_rate"] == 0.6
        assert d["performance"]["num_steps"] == 10
