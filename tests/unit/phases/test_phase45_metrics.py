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
Phase 45 Tests: Prometheus Metrics, LoRA Stats, Caching, Pooling, Logprobs, Executor
Tests vLLM-inspired infrastructure with Rust acceleration verification.
"""

import pytest
import time
import numpy as np


class TestPrometheusRegistry:
    """Tests for PrometheusRegistry and metric types."""

    def test_counter_basic(self):
        """Test basic counter operations."""
        from src.infrastructure.services.metrics.prometheus_registry import (
            Counter, MetricSpec, MetricType
        )

        spec = MetricSpec(
            name="test_counter",
            description="Test counter",
            metric_type=MetricType.COUNTER,
        )
        counter = Counter(spec)

        counter.increment(1.0)
        counter.increment(2.0)
        counter.increment(3.0)

        assert counter.get() == 6.0

    def test_counter_with_labels(self):
        """Test counter with labels."""
        from src.infrastructure.services.metrics.prometheus_registry import (
            Counter, MetricSpec, MetricType
        )

        spec = MetricSpec(
            name="test_counter",
            description="Test counter",
            metric_type=MetricType.COUNTER,
            labels=("method", "status"),
        )
        counter = Counter(spec)

        counter.increment(1.0, {"method": "GET", "status": "200"})
        counter.increment(2.0, {"method": "GET", "status": "200"})
        counter.increment(1.0, {"method": "POST", "status": "201"})

        assert counter.get({"method": "GET", "status": "200"}) == 3.0
        assert counter.get({"method": "POST", "status": "201"}) == 1.0

    def test_gauge_basic(self):
        """Test basic gauge operations."""
        from src.infrastructure.services.metrics.prometheus_registry import (
            Gauge, MetricSpec, MetricType
        )

        spec = MetricSpec(
            name="test_gauge",
            description="Test gauge",
            metric_type=MetricType.GAUGE,
        )
        gauge = Gauge(spec)

        gauge.set(10.0)
        assert gauge.get() == 10.0

        gauge.increment(5.0)
        assert gauge.get() == 15.0

        gauge.decrement(3.0)
        assert gauge.get() == 12.0

    def test_histogram_basic(self):
        """Test histogram operations."""
        from src.infrastructure.services.metrics.prometheus_registry import (
            Histogram, MetricSpec, MetricType
        )

        spec = MetricSpec(
            name="test_histogram",
            description="Test histogram",
            metric_type=MetricType.HISTOGRAM,
            buckets=(0.1, 0.5, 1.0, 5.0, 10.0, float('inf')),
        )
        histogram = Histogram(spec)

        # Observe some values
        histogram.observe(0.05)  # bucket 0.1
        histogram.observe(0.3)   # bucket 0.5
        histogram.observe(0.8)   # bucket 1.0
        histogram.observe(3.0)   # bucket 5.0
        histogram.observe(15.0)  # bucket inf

        assert histogram.get() == 5

        buckets = histogram.get_buckets()
        assert buckets[0.1] == 1
        assert buckets[0.5] == 2
        assert buckets[1.0] == 3
        assert buckets[5.0] == 4
        assert buckets[float('inf')] == 5

    def test_summary_basic(self):
        """Test summary operations."""
        from src.infrastructure.services.metrics.prometheus_registry import (
            Summary, MetricSpec, MetricType
        )

        spec = MetricSpec(
            name="test_summary",
            description="Test summary",
            metric_type=MetricType.SUMMARY,
        )
        summary = Summary(spec, max_age_seconds=60.0)

        # Observe some values
        for i in range(100):
            summary.observe(float(i))

        assert summary.get() == 100

        # Check quantiles
        p50 = summary.get_quantile(0.5)
        assert 40 <= p50 <= 60

        p99 = summary.get_quantile(0.99)
        assert p99 >= 90

    def test_registry_singleton(self):
        """Test registry singleton pattern."""
        from src.infrastructure.services.metrics.prometheus_registry import MetricsRegistry

        reg1 = MetricsRegistry.get_instance()
        reg2 = MetricsRegistry.get_instance()

        assert reg1 is reg2

    def test_registry_metric_creation(self):
        """Test creating metrics through registry."""
        from src.infrastructure.services.metrics.prometheus_registry import (
            MetricsRegistry, MetricsBackend
        )

        registry = MetricsRegistry(backend=MetricsBackend.PROMETHEUS)

        counter = registry.counter("requests_total", "Total requests")
        gauge = registry.gauge("active_connections", "Active connections")
        histogram = registry.histogram("latency", "Request latency")

        counter.increment()
        gauge.set(10)
        histogram.observe(0.5)

        assert counter.get() == 1.0
        assert gauge.get() == 10.0
        assert histogram.get() == 1

    def test_vllm_metrics(self):
        """Test VLLMMetrics collection."""
        from src.infrastructure.services.metrics.prometheus_registry import VLLMMetrics

        metrics = VLLMMetrics()

        # Record some metrics
        metrics.num_requests_running.set(5)
        metrics.num_requests_waiting.set(10)
        metrics.num_prompt_tokens.increment(100)
        metrics.num_generation_tokens.increment(50)
        metrics.request_latency.observe(1.5)
        metrics.time_to_first_token.observe(0.1)

        assert metrics.num_requests_running.get() == 5
        assert metrics.num_requests_waiting.get() == 10
        assert metrics.num_prompt_tokens.get() == 100
        assert metrics.num_generation_tokens.get() == 50

    def test_sampled_counter(self):
        """Test sampled counter for high-frequency ops."""
        from src.infrastructure.services.metrics.prometheus_registry import (
            SampledCounter, MetricSpec, MetricType
        )

        spec = MetricSpec(
            name="sampled_counter",
            description="Sampled counter",
            metric_type=MetricType.COUNTER,
        )
        counter = SampledCounter(spec, sample_rate=0.1)

        # Increment 100 times, should only count ~10 * (1/0.1) = 100 total
        for _ in range(100):
            counter.increment(1.0)

        # Should be approximately 100 (10 samples * 10 adjustment)
        assert 80 <= counter.get() <= 120


class TestLoRAStatsManager:
    """Tests for LoRA statistics tracking."""

    def test_adapter_registration(self):
        """Test registering LoRA adapters."""
        from src.infrastructure.services.metrics.lo_ra_stats_manager import (
            LoRAStatsManager, LoRALoadState
        )

        manager = LoRAStatsManager(max_loaded_adapters=4)

        info = manager.register_adapter(
            adapter_id="lora-1",
            rank=16,
            alpha=32.0,
            target_modules=("q_proj", "v_proj"),
            memory_bytes=1024 * 1024,
        )

        assert info.adapter_id == "lora-1"
        assert info.rank == 16
        assert info.alpha == 32.0
        assert info.load_state == LoRALoadState.NOT_LOADED

    def test_adapter_loading(self):
        """Test adapter loading lifecycle."""
        from src.infrastructure.services.metrics.lo_ra_stats_manager import (
            LoRAStatsManager, LoRALoadState
        )

        manager = LoRAStatsManager(max_loaded_adapters=4)

        manager.register_adapter(
            adapter_id="lora-1",
            rank=16,
            alpha=32.0,
            target_modules=("q_proj",),
            memory_bytes=1024 * 1024,
        )

        manager.start_loading("lora-1")
        info = manager.get_adapter_info("lora-1")
        assert info.load_state == LoRALoadState.LOADING

        manager.finish_loading("lora-1", success=True)
        info = manager.get_adapter_info("lora-1")
        assert info.load_state == LoRALoadState.LOADED

        stats = manager.get_stats()
        assert stats.loaded_adapters == 1

    def test_request_lifecycle(self):
        """Test LoRA request lifecycle."""
        from src.infrastructure.services.metrics.lo_ra_stats_manager import LoRAStatsManager

        manager = LoRAStatsManager()

        manager.register_adapter(
            adapter_id="lora-1",
            rank=16,
            alpha=32.0,
            target_modules=("q_proj",),
        )
        manager.finish_loading("lora-1", success=True)

        # Create request
        state = manager.create_request("req-1", "lora-1")
        assert state.request_id == "req-1"
        assert state.adapter_id == "lora-1"

        # Start execution
        manager.start_execution("req-1")

        # Finish execution
        time.sleep(0.01)
        manager.finish_execution("req-1", tokens=50)

        state = manager.get_request_state("req-1")
        assert state.tokens_processed == 50
        assert state.execution_latency is not None

    def test_lora_stats_aggregation(self):
        """Test LoRA stats aggregation."""
        from src.infrastructure.services.metrics.lo_ra_stats_manager import LoRAStatsManager

        manager = LoRAStatsManager()

        manager.register_adapter("lora-1", 16, 32.0, ("q_proj",))
        manager.finish_loading("lora-1", success=True)

        # Create and complete multiple requests
        for i in range(10):
            manager.create_request(f"req-{i}", "lora-1")
            manager.start_execution(f"req-{i}")
            manager.finish_execution(f"req-{i}", tokens=10 + i)

        stats = manager.get_stats()
        assert stats.total_requests == 10
        assert stats.completed_requests == 10
        assert stats.active_requests == 0
        assert stats.adapter_use_counts["lora-1"] == 10

    def test_request_lifecycle_manager(self):
        """Test RequestLifecycleManager."""
        from src.infrastructure.services.metrics.lo_ra_stats_manager import (
            RequestLifecycleManager, RequestStatus
        )

        manager = RequestLifecycleManager()

        lifecycle = manager.create("req-1", prompt_tokens=100, max_tokens=50)
        lifecycle.transition_to(RequestStatus.RUNNING)

        # Generate some tokens
        for _ in range(10):
            lifecycle.record_token()
            time.sleep(0.001)

        manager.finish("req-1", reason="stopped")

        assert manager.get_active_count() == 0
        assert manager.get_completed_count() == 1

        stats = manager.get_aggregate_stats()
        assert 'avg_ttft' in stats


class TestCachingMetrics:
    """Tests for caching metrics."""

    def test_sliding_window_metrics(self):
        """Test sliding window hit rate."""
        from src.infrastructure.services.metrics.caching_metrics import SlidingWindowMetrics

        window = SlidingWindowMetrics(window_seconds=60.0)

        # Record hits and misses
        for i in range(80):
            window.record_hit(bytes_accessed=100)
        for i in range(20):
            window.record_miss(bytes_accessed=100)

        stats = window.get_stats()
        assert 0.75 <= stats.hit_rate <= 0.85

    def test_caching_metrics_observe(self):
        """Test CachingMetrics observation."""
        from src.infrastructure.services.metrics.caching_metrics import (
            CachingMetrics, CacheType
        )

        metrics = CachingMetrics(CacheType.PREFIX)

        metrics.observe_hit(bytes_accessed=1024)
        metrics.observe_hit(bytes_accessed=1024)
        metrics.observe_miss(bytes_accessed=512)

        assert metrics.get_hit_rate() == pytest.approx(2/3, rel=0.1)

        stats = metrics.get_stats()
        assert stats.total_hits == 2
        assert stats.total_misses == 1

    def test_eviction_tracking(self):
        """Test eviction tracking."""
        from src.infrastructure.services.metrics.caching_metrics import (
            CachingMetrics, CacheType, EvictionReason
        )

        metrics = CachingMetrics(CacheType.KV)

        metrics.observe_eviction(5, EvictionReason.LRU, bytes_freed=5120)
        metrics.observe_eviction(3, EvictionReason.MEMORY_PRESSURE, bytes_freed=3072)
        metrics.observe_eviction(2, EvictionReason.LRU, bytes_freed=2048)

        breakdown = metrics.get_eviction_breakdown()
        assert breakdown[EvictionReason.LRU] == 2
        assert breakdown[EvictionReason.MEMORY_PRESSURE] == 1

    def test_prefix_cache_stats(self):
        """Test PrefixCacheStats."""
        from src.infrastructure.services.metrics.caching_metrics import PrefixCacheStats

        stats = PrefixCacheStats()

        # Record some prefix hits/misses
        for i in range(50):
            stats.observe_prefix_hit(f"hash_{i % 10}", prefix_length=100 + i)
        for i in range(25):
            stats.observe_prefix_miss(prefix_length=50 + i)

        assert 0.6 <= stats.get_hit_rate() <= 0.7
        assert stats.get_avg_prefix_length() > 0

    def test_multi_level_cache(self):
        """Test multi-level cache metrics."""
        from src.infrastructure.services.metrics.caching_metrics import (
            MultiLevelCacheMetrics, CacheType
        )

        multi = MultiLevelCacheMetrics()

        # Record to different cache levels
        multi.observe_hit(CacheType.PREFIX, bytes_accessed=100)
        multi.observe_miss(CacheType.PREFIX, bytes_accessed=100)
        multi.observe_hit(CacheType.BLOCK, bytes_accessed=200)
        multi.observe_hit(CacheType.KV, bytes_accessed=300)

        combined = multi.get_combined_hit_rate()
        assert 0.7 <= combined <= 0.8


class TestPoolingMetadata:
    """Tests for pooling infrastructure."""

    def test_pooling_cursor(self):
        """Test PoolingCursor operations."""
        from src.infrastructure.engine.pooling.pooling_metadata import PoolingCursor

        cursor = PoolingCursor(seq_start_idx=10, seq_len=100)

        assert cursor.remaining == 100
        assert not cursor.is_complete

        cursor.advance(30)
        assert cursor.current_pos == 30
        assert cursor.remaining == 70

        cursor.advance(70)
        assert cursor.is_complete

    def test_pooling_states_mean(self):
        """Test PoolingStates mean strategy."""
        from src.infrastructure.engine.pooling.pooling_metadata import (
            PoolingStates, PoolingStrategy
        )

        states = PoolingStates()
        states.initialize(hidden_dim=4, strategy=PoolingStrategy.MEAN)

        # Update with some hidden states
        hidden1 = np.array([[1.0, 2.0, 3.0, 4.0], [2.0, 3.0, 4.0, 5.0]])
        hidden2 = np.array([[3.0, 4.0, 5.0, 6.0]])

        states.update(hidden1)
        states.update(hidden2)

        result = states.finalize()
        # Mean should be (1+2+3)/3=2, (2+3+4)/3=3, etc.
        assert result[0] == pytest.approx(2.0, rel=0.1)

    def test_pooling_metadata_create(self):
        """Test PoolingMetadata creation."""
        from src.infrastructure.engine.pooling.pooling_metadata import (
            PoolingMetadata, PoolingStrategy
        )

        metadata = PoolingMetadata.create(
            seq_starts=[0, 100, 200],
            seq_lens=[50, 60, 70],
            hidden_dim=768,
            strategy=PoolingStrategy.MEAN,
        )

        assert metadata.batch_size == 3
        assert len(metadata.cursors) == 3
        assert len(metadata.states) == 3

    def test_mean_pooler(self):
        """Test MeanPooler."""
        from src.infrastructure.engine.pooling.pooling_metadata import (
            MeanPooler, PoolingMetadata, PoolingStrategy
        )

        hidden_states = np.array([
            [1.0, 2.0],
            [3.0, 4.0],
            [5.0, 6.0],
            [7.0, 8.0],
        ])

        metadata = PoolingMetadata.create(
            seq_starts=[0, 2],
            seq_lens=[2, 2],
            hidden_dim=2,
            strategy=PoolingStrategy.MEAN,
        )

        pooler = MeanPooler()
        results = pooler.pool(hidden_states, metadata)

        assert len(results) == 2
        np.testing.assert_array_almost_equal(results[0], [2.0, 3.0])
        np.testing.assert_array_almost_equal(results[1], [6.0, 7.0])

    def test_pooler_factory(self):
        """Test PoolerFactory."""
        from src.infrastructure.engine.pooling.pooling_metadata import (
            PoolerFactory, PoolingStrategy, MeanPooler, MaxPooler
        )

        mean_pooler = PoolerFactory.create(PoolingStrategy.MEAN)
        assert isinstance(mean_pooler, MeanPooler)

        max_pooler = PoolerFactory.create(PoolingStrategy.MAX)
        assert isinstance(max_pooler, MaxPooler)

    def test_chunked_pooling_manager(self):
        """Test ChunkedPoolingManager."""
        from src.infrastructure.engine.pooling.pooling_metadata import (
            ChunkedPoolingManager, PoolingStrategy
        )

        manager = ChunkedPoolingManager(
            hidden_dim=4,
            max_chunk_size=10,
            strategy=PoolingStrategy.MEAN,
        )

        metadata = manager.start_sequence("seq-1", seq_len=25)
        assert metadata.chunk_sizes == [10, 10, 5]

        # Process chunks
        chunk1 = np.random.randn(10, 4)
        is_complete = manager.process_chunk("seq-1", chunk1)
        assert not is_complete

        chunk2 = np.random.randn(10, 4)
        is_complete = manager.process_chunk("seq-1", chunk2)
        assert not is_complete

        chunk3 = np.random.randn(5, 4)
        is_complete = manager.process_chunk("seq-1", chunk3)
        assert is_complete

        result = manager.finalize("seq-1")
        assert result.shape == (4,)


class TestLogprobsProcessor:
    """Tests for logprobs processing."""

    def test_token_logprob(self):
        """Test TokenLogprob dataclass."""
        from src.infrastructure.engine.outputs.logprobs_processor import TokenLogprob

        lp1 = TokenLogprob(token_id=100, token="hello", logprob=-0.5)
        lp2 = TokenLogprob(token_id=200, token="world", logprob=-1.0)

        # Higher logprob should sort first (less negative)
        assert lp1 < lp2

    def test_logprobs_lists(self):
        """Test LogprobsLists."""
        from src.infrastructure.engine.outputs.logprobs_processor import (
            LogprobsLists, TopLogprobs, TokenLogprob
        )

        lists = LogprobsLists(num_sequences=2)

        entry1 = TopLogprobs(
            position=0,
            token_id=100,
            token="hello",
            logprob=-0.5,
            top_k=[
                TokenLogprob(100, "hello", -0.5),
                TokenLogprob(101, "hi", -1.0),
            ],
        )

        lists.append(0, entry1)

        seq0 = lists.get_sequence(0)
        assert len(seq0) == 1
        assert seq0[0].token_id == 100

    def test_logprobs_tensors_sparse(self):
        """Test LogprobsTensors sparse storage."""
        from src.infrastructure.engine.outputs.logprobs_processor import LogprobsTensors

        tensors = LogprobsTensors.create_empty(
            batch_size=2,
            max_seq_len=10,
            vocab_size=1000,
            top_k=5,
            sparse=True,
        )

        # Set position
        logprobs = np.random.randn(1000)
        logprobs[100] = 0.0  # Highest
        tensors.set_position(0, 0, logprobs, 100)

        assert tensors.seq_lens[0] == 1

    def test_sampler_output(self):
        """Test SamplerOutput."""
        from src.infrastructure.engine.outputs.logprobs_processor import SamplerOutput

        output = SamplerOutput(
            sampled_token_ids=np.array([100, 200, 300]),
            num_samples=1,
            temperature=0.8,
        )

        assert output.batch_size == 3
        np.testing.assert_array_equal(output.get_token_ids(0), [100])

    def test_model_runner_output(self):
        """Test ModelRunnerOutput."""
        from src.infrastructure.engine.outputs.logprobs_processor import ModelRunnerOutput

        output = ModelRunnerOutput.create(
            sampled_token_ids=np.array([100, 200]),
            req_ids=["req-1", "req-2"],
        )

        assert output.req_id_to_index["req-1"] == 0
        assert output.req_id_to_index["req-2"] == 1

        result = output.get_output_for_request("req-1")
        assert result is not None
        np.testing.assert_array_equal(result[0], [100])

    def test_streaming_logprobs_collector(self):
        """Test StreamingLogprobsCollector."""
        from src.infrastructure.engine.outputs.logprobs_processor import (
            StreamingLogprobsCollector, TopLogprobs
        )

        collector = StreamingLogprobsCollector(buffer_size=5)
        received = []

        def callback(data):
            received.extend(data)

        collector.register_callback("req-1", callback)

        for i in range(10):
            collector.add("req-1", TopLogprobs(
                position=i,
                token_id=i,
                token=f"tok_{i}",
                logprob=-0.1 * i,
            ))

        # Should have flushed twice (at 5 and 10)
        assert len(received) >= 5


class TestMultiprocExecutor:
    """Tests for multiprocess executor."""

    def test_future_wrapper(self):
        """Test FutureWrapper."""
        from src.infrastructure.services.executor.multiproc_executor import FutureWrapper

        future: FutureWrapper[int] = FutureWrapper("task-1")

        assert not future.done()

        future.set_result(42)
        assert future.done()
        assert future.result() == 42

    def test_future_wrapper_exception(self):
        """Test FutureWrapper with exception."""
        from src.infrastructure.services.executor.multiproc_executor import FutureWrapper

        future: FutureWrapper[int] = FutureWrapper("task-1")
        future.set_exception(ValueError("test error"))

        assert future.done()
        with pytest.raises(ValueError):
            future.result()

    def test_future_wrapper_timeout(self):
        """Test FutureWrapper timeout."""
        from src.infrastructure.services.executor.multiproc_executor import FutureWrapper

        future: FutureWrapper[int] = FutureWrapper("task-1")

        with pytest.raises(TimeoutError):
            future.result(timeout=0.1)

    def test_uniproc_executor(self):
        """Test UniprocExecutor."""
        from src.infrastructure.services.executor.multiproc_executor import UniprocExecutor

        def add(a: int, b: int) -> int:
            return a + b

        executor = UniprocExecutor(functions={"add": add})
        executor.start()

        future = executor.submit("add", 1, 2)
        assert future.result() == 3

        executor.shutdown()

    def test_executor_factory(self):
        """Test ExecutorFactory."""
        from src.infrastructure.services.executor.multiproc_executor import (
            ExecutorFactory, ExecutorBackend, UniprocExecutor
        )

        executor = ExecutorFactory.create(
            ExecutorBackend.UNIPROC,
            functions={"test": lambda: 42},
        )

        assert isinstance(executor, UniprocExecutor)

    def test_executor_get_class(self):
        """Test Executor.get_class factory method."""
        from src.infrastructure.services.executor.multiproc_executor import (
            Executor, ExecutorBackend, MultiprocExecutor, UniprocExecutor
        )

        mp_class = Executor.get_class(ExecutorBackend.MULTIPROC)
        assert mp_class == MultiprocExecutor

        uni_class = Executor.get_class(ExecutorBackend.UNIPROC)
        assert uni_class == UniprocExecutor


# Handle rust_core import
try:
    import rust_core
    RUST_AVAILABLE = True
except ImportError:
    rust_core = None  # type: ignore[assignment]
    RUST_AVAILABLE = False


class TestRustAcceleration:
    """Tests for Rust acceleration functions."""

    @pytest.fixture
    def rust_core(self):
        """Get rust_core module."""
        if not RUST_AVAILABLE:
            pytest.skip("rust_core not available")
        return rust_core

    def test_cache_observe_rust(self, rust_core):
        """Test cache observation Rust function."""
        hits, misses, rate = rust_core.cache_observe_rust(
            True, 100, 1000, 10, 5
        )
        assert hits == 11
        assert misses == 5
        assert rate == pytest.approx(11 / 16, rel=0.01)

    def test_histogram_observe_rust(self, rust_core):
        """Test histogram observation Rust function."""
        buckets = [0.1, 0.5, 1.0, 5.0]
        counts = [0, 0, 0, 0]

        new_counts, new_sum, total = rust_core.histogram_observe_rust(
            0.3, buckets, counts, 0.0
        )

        assert new_sum == 0.3
        # 0.3 should increment buckets >= 0.5
        assert new_counts[1] == 1  # 0.5 bucket

    def test_sliding_window_hit_rate_rust(self, rust_core):
        """Test sliding window hit rate Rust function."""
        current_time = 100.0
        events = [
            (99.0, True, 100, 1000),
            (98.0, True, 100, 1000),
            (97.0, False, 100, 1000),
            (96.0, True, 100, 1000),
        ]

        hits, misses, rate, avg_lat, total_bytes = rust_core.sliding_window_hit_rate_rust(
            events, 60.0, current_time
        )

        assert hits == 3
        assert misses == 1
        assert rate == pytest.approx(0.75, rel=0.01)

    def test_lora_latency_percentile_rust(self, rust_core):
        """Test LoRA latency percentile Rust function."""
        latencies = [float(i) for i in range(100)]

        p50 = rust_core.lora_latency_percentile_rust(latencies, 50.0)
        assert 45 <= p50 <= 55

        p99 = rust_core.lora_latency_percentile_rust(latencies, 99.0)
        assert p99 >= 95

    def test_pool_sequences_rust(self, rust_core):
        """Test sequence pooling Rust function."""
        hidden = [
            [1.0, 2.0],
            [3.0, 4.0],
            [5.0, 6.0],
            [7.0, 8.0],
        ]

        # Mean pooling (strategy=1)
        results = rust_core.pool_sequences_rust(
            hidden, [0, 2], [2, 2], 1
        )

        assert len(results) == 2
        assert results[0][0] == pytest.approx(2.0)
        assert results[0][1] == pytest.approx(3.0)

    def test_extract_top_k_batch_rust(self, rust_core):
        """Test top-k logprobs extraction."""
        logprobs = [
            [0.1, 0.5, 0.2, 0.8, 0.3],
            [0.9, 0.1, 0.4, 0.2, 0.7],
        ]

        results = rust_core.extract_top_k_batch_rust(logprobs, 3)

        assert len(results) == 2
        # First sequence: 0.8, 0.5, 0.3 are top 3
        assert results[0][0][0] == pytest.approx(0.8)

    def test_task_priority_sort_rust(self, rust_core):
        """Test task priority sorting."""
        tasks = [
            ("task-1", 1, 100.0),
            ("task-2", 3, 99.0),
            ("task-3", 2, 98.0),
            ("task-4", 3, 101.0),
        ]

        sorted_ids = rust_core.task_priority_sort_rust(tasks)

        # task-2 should be first (priority 3, earlier timestamp)
        assert sorted_ids[0] == "task-2"
        # task-4 second (priority 3, later timestamp)
        assert sorted_ids[1] == "task-4"

    def test_worker_health_check_rust(self, rust_core):
        """Test worker health check."""
        current_time = 100.0
        # Worker 0: 99.0, diff=1.0 < 10.0 → healthy
        # Worker 1: 90.0, diff=10.0 <= 10.0 → healthy (borderline)
        # Worker 2: 98.0, diff=2.0 < 10.0 → healthy
        # Worker 3: 85.0, diff=15.0 > 10.0 → unhealthy
        last_heartbeats = [99.0, 90.0, 98.0, 85.0]
        timeout = 10.0

        healthy, unhealthy = rust_core.worker_health_check_rust(
            last_heartbeats, current_time, timeout
        )

        # Using <= semantics, 3 workers are healthy
        assert healthy == 3
        assert 3 in unhealthy  # Only worker 3 is unhealthy


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
