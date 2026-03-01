# Class Breakdown: CachingMetrics

**File**: `src\infrastructure\metrics\CachingMetrics.py`  
**Classes**: 10

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CacheType`

**Line**: 31  
**Inherits**: Enum  
**Methods**: 0

Types of caches.

[TIP] **Suggested split**: Move to `cachetype.py`

---

### 2. `EvictionReason`

**Line**: 39  
**Inherits**: Enum  
**Methods**: 0

Reasons for cache eviction.

[TIP] **Suggested split**: Move to `evictionreason.py`

---

### 3. `CacheEvent`

**Line**: 49  
**Methods**: 2

Single cache event for sliding window tracking.

[TIP] **Suggested split**: Move to `cacheevent.py`

---

### 4. `EvictionEvent`

**Line**: 66  
**Methods**: 0

Cache eviction event (vLLM KVCacheEvictionEvent equivalent).

[TIP] **Suggested split**: Move to `evictionevent.py`

---

### 5. `CacheStats`

**Line**: 76  
**Methods**: 1

Aggregate cache statistics.

[TIP] **Suggested split**: Move to `cachestats.py`

---

### 6. `SlidingWindowStats`

**Line**: 95  
**Methods**: 0

Statistics from a sliding window of events.

[TIP] **Suggested split**: Move to `slidingwindowstats.py`

---

### 7. `SlidingWindowMetrics`

**Line**: 107  
**Methods**: 7

Sliding window metrics collector.

Features:
- Time-based sliding window
- Configurable window size
- Efficient percentile calculation
- Thread-safe updates

[TIP] **Suggested split**: Move to `slidingwindowmetrics.py`

---

### 8. `CachingMetrics`

**Line**: 193  
**Methods**: 11

Comprehensive cache metrics (vLLM CachingMetrics equivalent).

Features:
- Sliding window hit rate calculation
- Per-type cache tracking
- Eviction tracking
- Memory efficiency metrics

[TIP] **Suggested split**: Move to `cachingmetrics.py`

---

### 9. `PrefixCacheStats`

**Line**: 315  
**Methods**: 8

Prefix cache statistics (vLLM PrefixCacheStats equivalent).

Beyond vLLM:
- Per-prefix tracking
- Prefix length distributions
- Sharing efficiency metrics

[TIP] **Suggested split**: Move to `prefixcachestats.py`

---

### 10. `MultiLevelCacheMetrics`

**Line**: 400  
**Methods**: 7

Multi-level cache metrics tracking.

Beyond vLLM: Unified view across all cache levels.

[TIP] **Suggested split**: Move to `multilevelcachemetrics.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
