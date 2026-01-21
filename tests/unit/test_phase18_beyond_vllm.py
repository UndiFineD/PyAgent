"""
Phase 18 Tests: Beyond vLLM - Resilience and Advanced Structures.

Tests for:
- CircuitBreaker - Resilient failure handling
- RetryStrategy - Exponential backoff with jitter
- AdaptiveRateLimiter - Token bucket and sliding window
- BloomFilter - Probabilistic set membership
- RingBuffer - Circular buffer and time series
- Histogram - Percentile tracking

Phase 18: Beyond vLLM
"""
import pytest
import time
import threading


class TestCircuitBreaker:
    """Tests for CircuitBreaker."""
    
    def test_circuit_starts_closed(self):
        """Test circuit starts in closed state."""
        from src.infrastructure.resilience.circuit_breaker import (
            CircuitBreaker, CircuitState
        )
        
        cb = CircuitBreaker(failure_threshold=3)
        assert cb.state == CircuitState.CLOSED
        assert cb.is_closed
    
    def test_circuit_opens_after_failures(self):
        """Test circuit opens after threshold failures."""
        from src.infrastructure.resilience.circuit_breaker import (
            CircuitBreaker, CircuitState, CircuitBreakerError
        )
        
        cb = CircuitBreaker(failure_threshold=3, recovery_timeout=1.0)
        
        def failing_func():
            raise ValueError("Simulated failure")
        
        # Fail 3 times
        for _ in range(3):
            with pytest.raises(ValueError):
                cb.call(failing_func)
        
        # Circuit should be open
        assert cb.state == CircuitState.OPEN
        assert cb.is_open
        
        # Next call should be rejected
        with pytest.raises(CircuitBreakerError):
            cb.call(failing_func)
    
    def test_circuit_half_open_after_timeout(self):
        """Test circuit transitions to half-open after timeout."""
        from src.infrastructure.resilience.circuit_breaker import (
            CircuitBreaker, CircuitState
        )
        
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)
        
        def failing_func():
            raise ValueError("Simulated failure")
        
        # Open the circuit
        for _ in range(2):
            with pytest.raises(ValueError):
                cb.call(failing_func)
        
        assert cb.state == CircuitState.OPEN
        
        # Wait for recovery timeout
        time.sleep(0.15)
        
        # Should be half-open now
        assert cb.state == CircuitState.HALF_OPEN
    
    def test_circuit_closes_after_success(self):
        """Test circuit closes after successful calls in half-open."""
        from src.infrastructure.resilience.circuit_breaker import (
            CircuitBreaker, CircuitState
        )
        
        cb = CircuitBreaker(
            failure_threshold=2,
            recovery_timeout=0.05,
            success_threshold=2,
        )
        
        call_count = [0]
        
        def sometimes_fails():
            call_count[0] += 1
            if call_count[0] <= 2:
                raise ValueError("Simulated failure")
            return "success"
        
        # Open the circuit
        for _ in range(2):
            with pytest.raises(ValueError):
                cb.call(sometimes_fails)
        
        assert cb.state == CircuitState.OPEN
        
        # Wait for recovery
        time.sleep(0.1)
        
        # Successful calls should close circuit
        assert cb.call(sometimes_fails) == "success"
        assert cb.call(sometimes_fails) == "success"
        
        assert cb.state == CircuitState.CLOSED
    
    def test_circuit_stats(self):
        """Test circuit breaker statistics."""
        from src.infrastructure.resilience.circuit_breaker import CircuitBreaker
        
        cb = CircuitBreaker(failure_threshold=5)
        
        def success_func():
            return 42
        
        for _ in range(10):
            cb.call(success_func)
        
        stats = cb.stats.to_dict()
        assert stats['total_calls'] == 10
        assert stats['successful_calls'] == 10
        assert stats['failed_calls'] == 0
        assert stats['success_rate'] == 1.0
    
    def test_circuit_decorator(self):
        """Test circuit breaker as decorator."""
        from src.infrastructure.resilience.circuit_breaker import CircuitBreaker
        
        cb = CircuitBreaker(failure_threshold=3)
        
        @cb
        def my_function(x):
            return x * 2
        
        result = my_function(21)
        assert result == 42


class TestRetryStrategy:
    """Tests for RetryStrategy."""
    
    def test_retry_succeeds_first_try(self):
        """Test no retry needed on success."""
        from src.infrastructure.resilience.retry_strategy import RetryStrategy
        
        retry = RetryStrategy(max_attempts=3)
        
        def success_func():
            return "success"
        
        result = retry.execute(success_func)
        assert result == "success"
        assert retry.stats.total_retries == 0
    
    def test_retry_after_failures(self):
        """Test retry succeeds after initial failures."""
        from src.infrastructure.resilience.retry_strategy import RetryStrategy
        
        retry = RetryStrategy(max_attempts=3, base_delay=0.01)
        
        call_count = [0]
        
        def eventually_succeeds():
            call_count[0] += 1
            if call_count[0] < 3:
                raise ValueError("Not yet")
            return "success"
        
        result = retry.execute(eventually_succeeds)
        assert result == "success"
        assert call_count[0] == 3
        assert retry.stats.total_retries == 2
    
    def test_retry_exhausted(self):
        """Test RetryExhaustedError after max attempts."""
        from src.infrastructure.resilience.retry_strategy import (
            RetryStrategy, RetryExhaustedError
        )
        
        retry = RetryStrategy(max_attempts=2, base_delay=0.01)
        
        def always_fails():
            raise ValueError("Always fails")
        
        with pytest.raises(RetryExhaustedError) as exc_info:
            retry.execute(always_fails)
        
        assert exc_info.value.attempts == 2
        assert isinstance(exc_info.value.last_exception, ValueError)
    
    def test_retry_decorator(self):
        """Test retry as decorator."""
        from src.infrastructure.resilience.retry_strategy import retry
        
        call_count = [0]
        
        @retry(max_attempts=3, base_delay=0.01)
        def flaky_func():
            call_count[0] += 1
            if call_count[0] < 2:
                raise ConnectionError("Flaky")
            return "ok"
        
        result = flaky_func()
        assert result == "ok"
        assert call_count[0] == 2
    
    def test_non_retryable_exception(self):
        """Test exceptions that should not be retried."""
        from src.infrastructure.resilience.retry_strategy import RetryStrategy
        
        retry = RetryStrategy(
            max_attempts=3,
            retryable_exceptions=(ConnectionError,),
            non_retryable_exceptions=(ValueError,),
        )
        
        def raises_value_error():
            raise ValueError("Non-retryable")
        
        with pytest.raises(ValueError):
            retry.execute(raises_value_error)
        
        # Should not have retried
        assert retry.stats.total_retries == 0


class TestRateLimiter:
    """Tests for rate limiting components."""
    
    def test_token_bucket_allows_burst(self):
        """Test token bucket allows burst up to capacity."""
        from src.infrastructure.resilience.adaptive_rate_limiter import TokenBucket
        
        bucket = TokenBucket(rate=10.0, capacity=20)
        
        # Should allow burst of 20
        for _ in range(20):
            assert bucket.acquire()
        
        # 21st should fail
        assert not bucket.acquire()
    
    def test_token_bucket_refills(self):
        """Test token bucket refills over time."""
        from src.infrastructure.resilience.adaptive_rate_limiter import TokenBucket
        
        bucket = TokenBucket(rate=100.0, capacity=10)
        
        # Drain bucket
        for _ in range(10):
            bucket.acquire()
        
        assert not bucket.acquire()
        
        # Wait for refill
        time.sleep(0.05)  # 5 tokens at 100/s
        
        # Should have some tokens now
        assert bucket.acquire()
    
    def test_sliding_window_counter(self):
        """Test sliding window rate limiting."""
        from src.infrastructure.resilience.adaptive_rate_limiter import SlidingWindowCounter
        
        limiter = SlidingWindowCounter(limit=10, window_seconds=1.0)
        
        # Should allow 10 requests
        for _ in range(10):
            assert limiter.is_allowed()
        
        # 11th should be rejected
        assert not limiter.is_allowed()
        
        # Check remaining
        assert limiter.get_remaining() == 0
    
    def test_rate_limit_decorator(self):
        """Test rate_limit decorator."""
        from src.infrastructure.resilience.adaptive_rate_limiter import (
            rate_limit, RateLimitExceededError
        )
        
        @rate_limit(rate=5.0, capacity=2, block=False)
        def limited_func():
            return "ok"
        
        # First 2 should succeed (burst capacity)
        assert limited_func() == "ok"
        assert limited_func() == "ok"
        
        # 3rd should fail
        with pytest.raises(RateLimitExceededError):
            limited_func()
    
    def test_per_key_rate_limiter(self):
        """Test per-key rate limiting."""
        from src.infrastructure.resilience.adaptive_rate_limiter import PerKeyRateLimiter
        
        limiter = PerKeyRateLimiter[str](rate=5.0, capacity=2)
        
        # Each key has its own limit
        assert limiter.acquire("user1")
        assert limiter.acquire("user1")
        assert not limiter.acquire("user1")  # User1 exhausted
        
        # User2 still has tokens
        assert limiter.acquire("user2")
        assert limiter.acquire("user2")


class TestBloomFilter:
    """Tests for BloomFilter."""
    
    def test_bloom_add_and_contains(self):
        """Test basic add and contains operations."""
        from src.core.base.structures.bloom_filter import BloomFilter
        
        bf = BloomFilter(expected_items=1000, fp_rate=0.01)
        
        bf.add("hello")
        bf.add("world")
        
        assert "hello" in bf
        assert "world" in bf
        assert bf.contains("hello")
    
    def test_bloom_no_false_negatives(self):
        """Test that added items are always found."""
        from src.core.base.structures.bloom_filter import BloomFilter
        
        bf = BloomFilter(expected_items=1000, fp_rate=0.01)
        
        items = [f"item_{i}" for i in range(500)]
        
        for item in items:
            bf.add(item)
        
        # All items must be found
        for item in items:
            assert item in bf
    
    def test_bloom_false_positive_rate(self):
        """Test false positive rate is within bounds."""
        from src.core.base.structures.bloom_filter import BloomFilter
        
        bf = BloomFilter(expected_items=1000, fp_rate=0.01)
        
        # Add items
        for i in range(1000):
            bf.add(f"added_{i}")
        
        # Check false positive rate
        false_positives = 0
        test_count = 10000
        
        for i in range(test_count):
            if f"not_added_{i}" in bf:
                false_positives += 1
        
        actual_fp_rate = false_positives / test_count
        
        # Allow some margin (should be around 0.01)
        assert actual_fp_rate < 0.05
    
    def test_bloom_stats(self):
        """Test Bloom filter statistics."""
        from src.core.base.structures.bloom_filter import BloomFilter
        
        bf = BloomFilter(expected_items=100, fp_rate=0.01)
        
        for i in range(50):
            bf.add(f"item_{i}")
        
        stats = bf.get_stats()
        assert stats['items_added'] == 50
        assert stats['expected_items'] == 100
        assert stats['fill_ratio'] > 0
    
    def test_counting_bloom_remove(self):
        """Test counting Bloom filter with removal."""
        from src.core.base.structures.bloom_filter import CountingBloomFilter
        
        cbf = CountingBloomFilter(expected_items=100)
        
        cbf.add("hello")
        assert "hello" in cbf
        
        cbf.remove("hello")
        assert "hello" not in cbf
    
    def test_scalable_bloom(self):
        """Test scalable Bloom filter grows automatically."""
        from src.core.base.structures.bloom_filter import ScalableBloomFilter
        
        sbf = ScalableBloomFilter(initial_capacity=100, fp_rate=0.01)
        
        # Add many items (more than initial capacity)
        for i in range(500):
            sbf.add(f"item_{i}")
        
        # All should be found
        for i in range(500):
            assert f"item_{i}" in sbf
        
        stats = sbf.get_stats()
        assert stats['num_filters'] >= 1
        assert stats['total_items'] == 500


class TestRingBuffer:
    """Tests for RingBuffer."""
    
    def test_ring_buffer_basic(self):
        """Test basic ring buffer operations."""
        from src.core.base.structures.ring_buffer import RingBuffer
        
        rb = RingBuffer[int](capacity=5)
        
        for i in range(5):
            rb.append(i)
        
        assert rb.size == 5
        assert rb.is_full
        assert list(rb) == [0, 1, 2, 3, 4]
    
    def test_ring_buffer_overflow(self):
        """Test ring buffer overwrites oldest."""
        from src.core.base.structures.ring_buffer import RingBuffer
        
        rb = RingBuffer[int](capacity=3)
        
        for i in range(5):
            rb.append(i)
        
        assert rb.size == 3
        assert list(rb) == [2, 3, 4]  # Oldest (0, 1) overwritten
    
    def test_ring_buffer_pop(self):
        """Test pop operation."""
        from src.core.base.structures.ring_buffer import RingBuffer
        
        rb = RingBuffer[int](capacity=5)
        rb.append(1)
        rb.append(2)
        rb.append(3)
        
        assert rb.pop() == 1
        assert rb.pop() == 2
        assert rb.size == 1
    
    def test_ring_buffer_peek(self):
        """Test peek operations."""
        from src.core.base.structures.ring_buffer import RingBuffer
        
        rb = RingBuffer[int](capacity=5)
        rb.append(1)
        rb.append(2)
        rb.append(3)
        
        assert rb.peek() == 1  # Oldest
        assert rb.peek_newest() == 3  # Newest
        assert rb.size == 3  # No change
    
    def test_thread_safe_ring_buffer(self):
        """Test thread-safe ring buffer."""
        from src.core.base.structures.ring_buffer import ThreadSafeRingBuffer
        
        rb = ThreadSafeRingBuffer[int](capacity=100)
        
        def writer():
            for i in range(50):
                rb.append(i)
        
        threads = [threading.Thread(target=writer) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert rb.size == 100  # Limited by capacity
    
    def test_time_series_buffer(self):
        """Test time series buffer."""
        from src.core.base.structures.ring_buffer import TimeSeriesBuffer
        
        ts = TimeSeriesBuffer[float](capacity=100)
        
        for i in range(10):
            ts.append(float(i))
        
        values = ts.get_values_in_window(window_seconds=10.0)
        assert len(values) == 10
    
    def test_sliding_window_aggregator(self):
        """Test sliding window aggregator."""
        from src.core.base.structures.ring_buffer import SlidingWindowAggregator
        
        agg = SlidingWindowAggregator(window_seconds=1.0, bucket_seconds=0.1)
        
        for i in range(100):
            agg.add(float(i))
        
        assert agg.count() == 100
        assert agg.mean() == 49.5
        assert agg.min() == 0.0
        assert agg.max() == 99.0


class TestHistogram:
    """Tests for Histogram."""
    
    def test_histogram_basic(self):
        """Test basic histogram operations."""
        from src.observability.stats.histogram import Histogram
        
        h = Histogram(min_value=0.0, max_value=100.0, num_buckets=10)
        
        for i in range(100):
            h.add(float(i))
        
        assert h.count == 100
        assert h.mean() == 49.5
    
    def test_histogram_percentiles(self):
        """Test percentile calculations."""
        from src.observability.stats.histogram import Histogram
        
        h = Histogram(min_value=1.0, max_value=1000.0, num_buckets=100)
        
        # Add values 1-100
        for i in range(1, 101):
            h.add(float(i))
        
        # Median should be around 50
        p50 = h.percentile(50)
        assert 40 < p50 < 60
        
        # P99 should be high
        p99 = h.percentile(99)
        assert p99 > 90
    
    def test_histogram_stats(self):
        """Test histogram statistics."""
        from src.observability.stats.histogram import Histogram
        
        h = Histogram(min_value=1.0, max_value=100.0, num_buckets=50)
        
        for i in range(1, 51):
            h.add(float(i))
        
        stats = h.get_stats()
        assert stats['count'] == 50
        assert 'p50' in stats
        assert 'p99' in stats
        assert stats['min'] == 1.0
        assert stats['max'] == 50.0
    
    def test_latency_histogram(self):
        """Test pre-configured latency histogram."""
        from src.observability.stats.histogram import LatencyHistogram
        
        h = LatencyHistogram()
        
        # Simulate latencies in ms
        latencies = [10, 20, 30, 50, 100, 200, 500, 1000]
        
        for lat in latencies:
            h.add(float(lat))
        
        stats = h.get_stats()
        assert stats['count'] == 8
        assert stats['min'] == 10.0
        assert stats['max'] == 1000.0
    
    def test_exponential_histogram(self):
        """Test exponential histogram."""
        from src.observability.stats.histogram import ExponentialHistogram
        
        h = ExponentialHistogram(scale=2)
        
        for i in range(1, 101):
            h.add(float(i))
        
        stats = h.get_stats()
        assert stats['count'] == 100
        assert stats['positive_buckets'] > 0


class TestIntegration:
    """Integration tests combining multiple Phase 18 components."""
    
    def test_circuit_breaker_with_retry(self):
        """Test circuit breaker combined with retry."""
        from src.infrastructure.resilience.circuit_breaker import CircuitBreaker
        from src.infrastructure.resilience.retry_strategy import RetryStrategy
        
        cb = CircuitBreaker(failure_threshold=5, recovery_timeout=0.1)
        retry = RetryStrategy(max_attempts=5, base_delay=0.01)
        
        call_count = [0]
        
        @cb
        def external_call():
            call_count[0] += 1
            if call_count[0] < 3:
                raise ConnectionError("Simulated")
            return "success"
        
        # Retry wraps circuit breaker
        result = retry.execute(external_call)
        assert result == "success"
        assert call_count[0] == 3
    
    def test_bloom_with_ring_buffer(self):
        """Test Bloom filter for deduplication with ring buffer."""
        from src.core.base.structures.bloom_filter import BloomFilter
        from src.core.base.structures.ring_buffer import RingBuffer
        
        seen = BloomFilter(expected_items=1000, fp_rate=0.01)
        recent = RingBuffer[str](capacity=100)
        
        items = ["a", "b", "c", "a", "d", "b", "e"]
        unique = []
        
        for item in items:
            if item not in seen:
                seen.add(item)
                recent.append(item)
                unique.append(item)
        
        assert unique == ["a", "b", "c", "d", "e"]
        assert recent.size == 5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
