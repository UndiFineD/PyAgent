# Class Breakdown: BlockPoolManager

**File**: `src\infrastructure\cache\BlockPoolManager.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BlockState`

**Line**: 28  
**Inherits**: IntEnum  
**Methods**: 0

Block allocation state with priority ordering.

[TIP] **Suggested split**: Move to `blockstate.py`

---

### 2. `Block`

**Line**: 37  
**Methods**: 1

A single KV cache block.

[TIP] **Suggested split**: Move to `block.py`

---

### 3. `BlockPoolConfig`

**Line**: 56  
**Methods**: 0

Configuration for block pool.

[TIP] **Suggested split**: Move to `blockpoolconfig.py`

---

### 4. `EvictionEvent`

**Line**: 68  
**Methods**: 0

Record of a block eviction.

[TIP] **Suggested split**: Move to `evictionevent.py`

---

### 5. `CacheMetrics`

**Line**: 79  
**Methods**: 1

KV cache metrics.

[TIP] **Suggested split**: Move to `cachemetrics.py`

---

### 6. `KVCacheMetricsCollector`

**Line**: 99  
**Methods**: 5

Collector for KV cache metrics.

vLLM Pattern: KVCacheMetricsCollector from block_pool.py

[TIP] **Suggested split**: Move to `kvcachemetricscollector.py`

---

### 7. `ARCPolicy`

**Line**: 137  
**Methods**: 6

Adaptive Replacement Cache eviction policy.

Beyond vLLM: ARC balances recency (LRU) and frequency (LFU).

T1: Recent items (LRU of items seen once)
T2: Frequent items (LRU of items seen more than onc...

[TIP] **Suggested split**: Move to `arcpolicy.py`

---

### 8. `BlockPool`

**Line**: 261  
**Methods**: 15

Block pool with LRU/ARC eviction and prefix caching.

vLLM Pattern: BlockPool from v1/core/block_pool.py

[TIP] **Suggested split**: Move to `blockpool.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
