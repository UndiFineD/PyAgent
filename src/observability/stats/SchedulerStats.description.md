# SchedulerStats

**File**: `src\observability\stats\SchedulerStats.py`  
**Type**: Python Module  
**Summary**: 8 classes, 2 functions, 6 imports  
**Lines**: 502  
**Complexity**: 41 (complex)

## Overview

Scheduler Statistics.

Comprehensive metrics for LLM inference scheduling:
- Request queue and running state tracking
- Prefix cache hit/miss statistics
- Speculative decoding acceptance rates
- Performance timing breakdown

Inspired by vLLM's v1/metrics/stats.py architecture.

## Classes (8)

### `MetricExportFormat`

**Inherits from**: str, Enum

Format for metric export.

### `PrefixCacheStats`

Statistics for prefix cache performance.

**Methods** (5):
- `record(self, num_tokens, num_hits, preempted)`
- `hit_rate(self)`
- `reset(self)`
- `clone(self)`
- `as_dict(self)`

### `SpecDecodingStats`

Statistics for speculative decoding.

**Methods** (9):
- `__post_init__(self)`
- `new(cls, num_spec_tokens)`
- `observe_draft(self, num_draft_tokens, num_accepted_tokens, accepted_positions)`
- `acceptance_rate(self)`
- `avg_accepted_per_draft(self)`
- `position_acceptance_rates(self)`
- `reset(self)`
- `clone(self)`
- `as_dict(self)`

### `CUDAGraphStats`

Statistics for CUDA graph capture and replay.

**Methods** (5):
- `record_capture(self, time_ms, memory_mb)`
- `record_replay(self, time_ms)`
- `avg_capture_time_ms(self)`
- `avg_replay_time_ms(self)`
- `as_dict(self)`

### `PerfStats`

Performance timing breakdown.

**Methods** (5):
- `record_step(self, schedule_ms, forward_ms, sample_ms)`
- `total_time_ms(self)`
- `avg_step_time_ms(self)`
- `reset(self)`
- `as_dict(self)`

### `KVCacheEvictionEvent`

Event tracking KV cache eviction.

**Methods** (2):
- `now(cls, request_id, num_blocks, reason)`
- `as_dict(self)`

### `SchedulerStats`

Comprehensive scheduler statistics.

**Methods** (7):
- `record_step(self, num_running, num_waiting, kv_usage)`
- `record_eviction(self, event)`
- `total_requests(self)`
- `reset(self)`
- `clone(self)`
- `as_dict(self)`
- `to_prometheus(self)`

### `SchedulerStatsCollector`

Collects and aggregates scheduler statistics over time.

**Methods** (6):
- `__init__(self, window_size)`
- `current(self)`
- `record_step(self, num_running, num_waiting, kv_usage)`
- `commit(self)`
- `get_averages(self)`
- `drain_events(self)`

## Functions (2)

### `create_scheduler_stats(enable_spec_decoding, num_spec_tokens)`

Create scheduler stats with optional spec decoding.

### `create_stats_collector(window_size)`

Create a stats collector.

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `time`
- `typing.Any`

---
*Auto-generated documentation*
