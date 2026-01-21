"""
Phase 45: Caching Metrics with Sliding Window
vLLM-inspired cache metrics with sliding window aggregation.

Beyond vLLM:
- Multi-level cache tracking (prefix, block, KV)
- Sliding window percentiles
- Cache efficiency scoring
- Predictive eviction metrics
- Memory pressure indicators
"""

from __future__ import annotations

import threading
import time
from collections import deque
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Deque, Dict, List, Optional, Tuple

# Try to import rust_core for acceleration
try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False
    rust_core = None


class CacheType(Enum):
    """Types of caches."""
    PREFIX = auto()
    BLOCK = auto()
    KV = auto()
    ENCODER = auto()


class EvictionReason(Enum):
    """Reasons for cache eviction."""
    LRU = auto()
    MEMORY_PRESSURE = auto()
    EXPLICIT = auto()
    TTL_EXPIRED = auto()
    PREEMPTION = auto()


@dataclass
class CacheEvent:
    """Single cache event for sliding window tracking."""
    timestamp: float
    is_hit: bool
    bytes_accessed: int = 0
    latency_ns: int = 0
    
    @classmethod
    def hit(cls, bytes_accessed: int = 0, latency_ns: int = 0) -> 'CacheEvent':
        return cls(time.time(), True, bytes_accessed, latency_ns)
    
    @classmethod
    def miss(cls, bytes_accessed: int = 0, latency_ns: int = 0) -> 'CacheEvent':
        return cls(time.time(), False, bytes_accessed, latency_ns)


@dataclass
class EvictionEvent:
    """Cache eviction event (vLLM KVCacheEvictionEvent equivalent)."""
    timestamp: float
    num_blocks: int
    reason: EvictionReason
    bytes_freed: int = 0
    latency_ns: int = 0


@dataclass
class CacheStats:
    """Aggregate cache statistics."""
    total_hits: int = 0
    total_misses: int = 0
    total_evictions: int = 0
    total_bytes_read: int = 0
    total_bytes_written: int = 0
    current_size_bytes: int = 0
    peak_size_bytes: int = 0
    
    @property
    def hit_rate(self) -> float:
        total = self.total_hits + self.total_misses
        if total == 0:
            return 0.0
        return self.total_hits / total


@dataclass
class SlidingWindowStats:
    """Statistics from a sliding window of events."""
    hits: int = 0
    misses: int = 0
    hit_rate: float = 0.0
    avg_latency_ns: float = 0.0
    p50_latency_ns: float = 0.0
    p99_latency_ns: float = 0.0
    bytes_per_second: float = 0.0
    window_duration: float = 0.0


class SlidingWindowMetrics:
    """
    Sliding window metrics collector.
    
    Features:
    - Time-based sliding window
    - Configurable window size
    - Efficient percentile calculation
    - Thread-safe updates
    """
    
    def __init__(
        self,
        window_seconds: float = 60.0,
        max_events: int = 10000,
    ):
        self._window_seconds = window_seconds
        self._max_events = max_events
        self._events: Deque[CacheEvent] = deque(maxlen=max_events)
        self._lock = threading.Lock()
    
    def record(self, event: CacheEvent) -> None:
        """Record a cache event."""
        with self._lock:
            self._events.append(event)
    
    def record_hit(self, bytes_accessed: int = 0, latency_ns: int = 0) -> None:
        """Record a cache hit."""
        self.record(CacheEvent.hit(bytes_accessed, latency_ns))
    
    def record_miss(self, bytes_accessed: int = 0, latency_ns: int = 0) -> None:
        """Record a cache miss."""
        self.record(CacheEvent.miss(bytes_accessed, latency_ns))
    
    def _prune_old_events(self, now: float) -> List[CacheEvent]:
        """Get events within the window."""
        cutoff = now - self._window_seconds
        return [e for e in self._events if e.timestamp > cutoff]
    
    def get_stats(self) -> SlidingWindowStats:
        """Get statistics from the sliding window."""
        now = time.time()
        with self._lock:
            events = self._prune_old_events(now)
        
        if not events:
            return SlidingWindowStats()
        
        hits = sum(1 for e in events if e.is_hit)
        misses = len(events) - hits
        total = len(events)
        
        latencies = [e.latency_ns for e in events if e.latency_ns > 0]
        total_bytes = sum(e.bytes_accessed for e in events)
        
        # Calculate duration
        if len(events) > 1:
            duration = events[-1].timestamp - events[0].timestamp
        else:
            duration = 0.0
        
        # Latency percentiles
        avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
        sorted_latencies = sorted(latencies) if latencies else []
        p50 = sorted_latencies[len(sorted_latencies) // 2] if sorted_latencies else 0.0
        p99 = sorted_latencies[int(len(sorted_latencies) * 0.99)] if sorted_latencies else 0.0
        
        # Throughput
        bytes_per_second = total_bytes / duration if duration > 0 else 0.0
        
        return SlidingWindowStats(
            hits=hits,
            misses=misses,
            hit_rate=hits / total if total > 0 else 0.0,
            avg_latency_ns=avg_latency,
            p50_latency_ns=p50,
            p99_latency_ns=p99,
            bytes_per_second=bytes_per_second,
            window_duration=duration,
        )
    
    def get_hit_rate(self) -> float:
        """Get current hit rate."""
        return self.get_stats().hit_rate


class CachingMetrics:
    """
    Comprehensive cache metrics (vLLM CachingMetrics equivalent).
    
    Features:
    - Sliding window hit rate calculation
    - Per-type cache tracking
    - Eviction tracking
    - Memory efficiency metrics
    """
    
    def __init__(
        self,
        cache_type: CacheType = CacheType.PREFIX,
        window_seconds: float = 60.0,
        max_recent_requests: int = 10000,
    ):
        self.cache_type = cache_type
        self._window = SlidingWindowMetrics(window_seconds, max_recent_requests)
        self._evictions: Deque[EvictionEvent] = deque(maxlen=1000)
        self._stats = CacheStats()
        self._lock = threading.Lock()
    
    def observe_hit(
        self,
        bytes_accessed: int = 0,
        latency_ns: int = 0,
    ) -> None:
        """Record a cache hit."""
        with self._lock:
            self._stats.total_hits += 1
            self._stats.total_bytes_read += bytes_accessed
        self._window.record_hit(bytes_accessed, latency_ns)
    
    def observe_miss(
        self,
        bytes_accessed: int = 0,
        latency_ns: int = 0,
    ) -> None:
        """Record a cache miss."""
        with self._lock:
            self._stats.total_misses += 1
        self._window.record_miss(bytes_accessed, latency_ns)
    
    def observe_write(
        self,
        bytes_written: int,
    ) -> None:
        """Record bytes written to cache."""
        with self._lock:
            self._stats.total_bytes_written += bytes_written
            self._stats.current_size_bytes += bytes_written
            self._stats.peak_size_bytes = max(
                self._stats.peak_size_bytes,
                self._stats.current_size_bytes,
            )
    
    def observe_eviction(
        self,
        num_blocks: int,
        reason: EvictionReason,
        bytes_freed: int = 0,
        latency_ns: int = 0,
    ) -> None:
        """Record a cache eviction."""
        event = EvictionEvent(
            timestamp=time.time(),
            num_blocks=num_blocks,
            reason=reason,
            bytes_freed=bytes_freed,
            latency_ns=latency_ns,
        )
        with self._lock:
            self._evictions.append(event)
            self._stats.total_evictions += 1
            self._stats.current_size_bytes -= bytes_freed
    
    def get_hit_rate(self) -> float:
        """Get sliding window hit rate."""
        return self._window.get_hit_rate()
    
    def get_total_hit_rate(self) -> float:
        """Get overall hit rate."""
        with self._lock:
            return self._stats.hit_rate
    
    def get_stats(self) -> CacheStats:
        """Get aggregate statistics."""
        with self._lock:
            return CacheStats(
                total_hits=self._stats.total_hits,
                total_misses=self._stats.total_misses,
                total_evictions=self._stats.total_evictions,
                total_bytes_read=self._stats.total_bytes_read,
                total_bytes_written=self._stats.total_bytes_written,
                current_size_bytes=self._stats.current_size_bytes,
                peak_size_bytes=self._stats.peak_size_bytes,
            )
    
    def get_window_stats(self) -> SlidingWindowStats:
        """Get sliding window statistics."""
        return self._window.get_stats()
    
    def get_eviction_rate(self, window_seconds: float = 60.0) -> float:
        """Get evictions per second in the window."""
        now = time.time()
        cutoff = now - window_seconds
        with self._lock:
            recent = [e for e in self._evictions if e.timestamp > cutoff]
        if not recent:
            return 0.0
        return len(recent) / window_seconds
    
    def get_eviction_breakdown(self) -> Dict[EvictionReason, int]:
        """Get evictions by reason."""
        with self._lock:
            breakdown: Dict[EvictionReason, int] = {}
            for event in self._evictions:
                breakdown[event.reason] = breakdown.get(event.reason, 0) + 1
            return breakdown


class PrefixCacheStats:
    """
    Prefix cache statistics (vLLM PrefixCacheStats equivalent).
    
    Beyond vLLM:
    - Per-prefix tracking
    - Prefix length distributions
    - Sharing efficiency metrics
    """
    
    def __init__(self, window_seconds: float = 60.0):
        self._metrics = CachingMetrics(CacheType.PREFIX, window_seconds)
        self._prefix_lengths: Deque[int] = deque(maxlen=1000)
        self._shared_prefixes: Dict[str, int] = {}  # hash -> share count
        self._lock = threading.Lock()
    
    def observe_prefix_hit(
        self,
        prefix_hash: str,
        prefix_length: int,
        bytes_accessed: int = 0,
        latency_ns: int = 0,
    ) -> None:
        """Record a prefix cache hit."""
        self._metrics.observe_hit(bytes_accessed, latency_ns)
        with self._lock:
            self._prefix_lengths.append(prefix_length)
            self._shared_prefixes[prefix_hash] = (
                self._shared_prefixes.get(prefix_hash, 0) + 1
            )
    
    def observe_prefix_miss(
        self,
        prefix_length: int,
        bytes_accessed: int = 0,
        latency_ns: int = 0,
    ) -> None:
        """Record a prefix cache miss."""
        self._metrics.observe_miss(bytes_accessed, latency_ns)
        with self._lock:
            self._prefix_lengths.append(prefix_length)
    
    def observe_preemption(
        self,
        num_blocks: int,
        bytes_freed: int = 0,
    ) -> None:
        """Record a preemption eviction."""
        self._metrics.observe_eviction(
            num_blocks,
            EvictionReason.PREEMPTION,
            bytes_freed,
        )
    
    def get_hit_rate(self) -> float:
        """Get sliding window hit rate."""
        return self._metrics.get_hit_rate()
    
    def get_avg_prefix_length(self) -> float:
        """Get average prefix length."""
        with self._lock:
            if not self._prefix_lengths:
                return 0.0
            return sum(self._prefix_lengths) / len(self._prefix_lengths)
    
    def get_sharing_factor(self) -> float:
        """Get average prefix sharing factor."""
        with self._lock:
            if not self._shared_prefixes:
                return 1.0
            return sum(self._shared_prefixes.values()) / len(self._shared_prefixes)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics."""
        return {
            'hit_rate': self.get_hit_rate(),
            'total_hit_rate': self._metrics.get_total_hit_rate(),
            'avg_prefix_length': self.get_avg_prefix_length(),
            'sharing_factor': self.get_sharing_factor(),
            'eviction_rate': self._metrics.get_eviction_rate(),
            'cache_stats': self._metrics.get_stats(),
            'window_stats': self._metrics.get_window_stats(),
        }


class MultiLevelCacheMetrics:
    """
    Multi-level cache metrics tracking.
    
    Beyond vLLM: Unified view across all cache levels.
    """
    
    def __init__(self, window_seconds: float = 60.0):
        self._caches: Dict[CacheType, CachingMetrics] = {}
        self._window_seconds = window_seconds
        self._lock = threading.Lock()
    
    def get_or_create(self, cache_type: CacheType) -> CachingMetrics:
        """Get or create metrics for a cache type."""
        with self._lock:
            if cache_type not in self._caches:
                self._caches[cache_type] = CachingMetrics(
                    cache_type, self._window_seconds
                )
            return self._caches[cache_type]
    
    def observe_hit(
        self,
        cache_type: CacheType,
        bytes_accessed: int = 0,
        latency_ns: int = 0,
    ) -> None:
        """Record a hit on a specific cache."""
        self.get_or_create(cache_type).observe_hit(bytes_accessed, latency_ns)
    
    def observe_miss(
        self,
        cache_type: CacheType,
        bytes_accessed: int = 0,
        latency_ns: int = 0,
    ) -> None:
        """Record a miss on a specific cache."""
        self.get_or_create(cache_type).observe_miss(bytes_accessed, latency_ns)
    
    def get_combined_hit_rate(self) -> float:
        """Get combined hit rate across all caches."""
        with self._lock:
            total_hits = 0
            total_accesses = 0
            for metrics in self._caches.values():
                stats = metrics.get_stats()
                total_hits += stats.total_hits
                total_accesses += stats.total_hits + stats.total_misses
            
            if total_accesses == 0:
                return 0.0
            return total_hits / total_accesses
    
    def get_all_stats(self) -> Dict[CacheType, CacheStats]:
        """Get statistics for all caches."""
        with self._lock:
            return {
                cache_type: metrics.get_stats()
                for cache_type, metrics in self._caches.items()
            }
    
    def get_memory_pressure(self) -> float:
        """
        Calculate memory pressure indicator (0-1).
        
        Beyond vLLM: Predictive memory pressure based on eviction rate.
        """
        with self._lock:
            total_eviction_rate = sum(
                m.get_eviction_rate() for m in self._caches.values()
            )
            total_peak = sum(
                m.get_stats().peak_size_bytes for m in self._caches.values()
            )
            total_current = sum(
                m.get_stats().current_size_bytes for m in self._caches.values()
            )
            
            # Combine utilization and eviction rate
            utilization = total_current / total_peak if total_peak > 0 else 0.0
            eviction_pressure = min(1.0, total_eviction_rate / 100)  # Normalize
            
            return (utilization * 0.7) + (eviction_pressure * 0.3)


def observe_with_rust(
    is_hit: bool,
    bytes_accessed: int,
    latency_ns: int,
) -> Optional[Tuple[int, int, float]]:
    """
    Optimized observation with Rust.
    
    Returns (hits, misses, hit_rate) if Rust is available.
    """
    if HAS_RUST and hasattr(rust_core, 'cache_observe'):
        return rust_core.cache_observe(is_hit, bytes_accessed, latency_ns)
    return None


__all__ = [
    'CacheType',
    'EvictionReason',
    'CacheEvent',
    'EvictionEvent',
    'CacheStats',
    'SlidingWindowStats',
    'SlidingWindowMetrics',
    'CachingMetrics',
    'PrefixCacheStats',
    'MultiLevelCacheMetrics',
    'observe_with_rust',
]
