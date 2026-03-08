# Class Breakdown: SchedulerStats

**File**: `src\observability\stats\SchedulerStats.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MetricExportFormat`

**Line**: 21  
**Inherits**: str, Enum  
**Methods**: 0

Format for metric export.

[TIP] **Suggested split**: Move to `metricexportformat.py`

---

### 2. `PrefixCacheStats`

**Line**: 29  
**Methods**: 5

Statistics for prefix cache performance.

[TIP] **Suggested split**: Move to `prefixcachestats.py`

---

### 3. `SpecDecodingStats`

**Line**: 82  
**Methods**: 9

Statistics for speculative decoding.

[TIP] **Suggested split**: Move to `specdecodingstats.py`

---

### 4. `CUDAGraphStats`

**Line**: 163  
**Methods**: 5

Statistics for CUDA graph capture and replay.

[TIP] **Suggested split**: Move to `cudagraphstats.py`

---

### 5. `PerfStats`

**Line**: 206  
**Methods**: 5

Performance timing breakdown.

[TIP] **Suggested split**: Move to `perfstats.py`

---

### 6. `KVCacheEvictionEvent`

**Line**: 277  
**Methods**: 2

Event tracking KV cache eviction.

[TIP] **Suggested split**: Move to `kvcacheevictionevent.py`

---

### 7. `SchedulerStats`

**Line**: 304  
**Methods**: 7

Comprehensive scheduler statistics.

[TIP] **Suggested split**: Move to `schedulerstats.py`

---

### 8. `SchedulerStatsCollector`

**Line**: 431  
**Methods**: 6

Collects and aggregates scheduler statistics over time.

[TIP] **Suggested split**: Move to `schedulerstatscollector.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
