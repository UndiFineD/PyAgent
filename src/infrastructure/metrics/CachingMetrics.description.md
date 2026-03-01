# CachingMetrics

**File**: `src\infrastructure\metrics\CachingMetrics.py`  
**Type**: Python Module  
**Summary**: 10 classes, 1 functions, 15 imports  
**Lines**: 512  
**Complexity**: 37 (complex)

## Overview

Phase 45: Caching Metrics with Sliding Window
vLLM-inspired cache metrics with sliding window aggregation.

Beyond vLLM:
- Multi-level cache tracking (prefix, block, KV)
- Sliding window percentiles
- Cache efficiency scoring
- Predictive eviction metrics
- Memory pressure indicators

## Classes (10)

### `CacheType`

**Inherits from**: Enum

Types of caches.

### `EvictionReason`

**Inherits from**: Enum

Reasons for cache eviction.

### `CacheEvent`

Single cache event for sliding window tracking.

**Methods** (2):
- `hit(cls, bytes_accessed, latency_ns)`
- `miss(cls, bytes_accessed, latency_ns)`

### `EvictionEvent`

Cache eviction event (vLLM KVCacheEvictionEvent equivalent).

### `CacheStats`

Aggregate cache statistics.

**Methods** (1):
- `hit_rate(self)`

### `SlidingWindowStats`

Statistics from a sliding window of events.

### `SlidingWindowMetrics`

Sliding window metrics collector.

Features:
- Time-based sliding window
- Configurable window size
- Efficient percentile calculation
- Thread-safe updates

**Methods** (7):
- `__init__(self, window_seconds, max_events)`
- `record(self, event)`
- `record_hit(self, bytes_accessed, latency_ns)`
- `record_miss(self, bytes_accessed, latency_ns)`
- `_prune_old_events(self, now)`
- `get_stats(self)`
- `get_hit_rate(self)`

### `CachingMetrics`

Comprehensive cache metrics (vLLM CachingMetrics equivalent).

Features:
- Sliding window hit rate calculation
- Per-type cache tracking
- Eviction tracking
- Memory efficiency metrics

**Methods** (11):
- `__init__(self, cache_type, window_seconds, max_recent_requests)`
- `observe_hit(self, bytes_accessed, latency_ns)`
- `observe_miss(self, bytes_accessed, latency_ns)`
- `observe_write(self, bytes_written)`
- `observe_eviction(self, num_blocks, reason, bytes_freed, latency_ns)`
- `get_hit_rate(self)`
- `get_total_hit_rate(self)`
- `get_stats(self)`
- `get_window_stats(self)`
- `get_eviction_rate(self, window_seconds)`
- ... and 1 more methods

### `PrefixCacheStats`

Prefix cache statistics (vLLM PrefixCacheStats equivalent).

Beyond vLLM:
- Per-prefix tracking
- Prefix length distributions
- Sharing efficiency metrics

**Methods** (8):
- `__init__(self, window_seconds)`
- `observe_prefix_hit(self, prefix_hash, prefix_length, bytes_accessed, latency_ns)`
- `observe_prefix_miss(self, prefix_length, bytes_accessed, latency_ns)`
- `observe_preemption(self, num_blocks, bytes_freed)`
- `get_hit_rate(self)`
- `get_avg_prefix_length(self)`
- `get_sharing_factor(self)`
- `get_stats(self)`

### `MultiLevelCacheMetrics`

Multi-level cache metrics tracking.

Beyond vLLM: Unified view across all cache levels.

**Methods** (7):
- `__init__(self, window_seconds)`
- `get_or_create(self, cache_type)`
- `observe_hit(self, cache_type, bytes_accessed, latency_ns)`
- `observe_miss(self, cache_type, bytes_accessed, latency_ns)`
- `get_combined_hit_rate(self)`
- `get_all_stats(self)`
- `get_memory_pressure(self)`

## Functions (1)

### `observe_with_rust(is_hit, bytes_accessed, latency_ns)`

Optimized observation with Rust.

Returns (hits, misses, hit_rate) if Rust is available.

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `collections.deque`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `rust_core`
- `threading`
- `time`
- `typing.Any`
- `typing.Deque`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
