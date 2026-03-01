# Class Breakdown: lru_offload_manager

**File**: `src\infrastructure\storage\kv_transfer\lru_offload_manager.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LRUEntry`

**Line**: 61  
**Methods**: 1

Entry in LRU cache with metadata.

[TIP] **Suggested split**: Move to `lruentry.py`

---

### 2. `LRUOffloadManager`

**Line**: 77  
**Inherits**: OffloadingManager  
**Methods**: 9

LRU-based offloading manager.

Simple but effective LRU eviction policy for KV cache offloading.
Evicts least recently used blocks when space is needed.

[TIP] **Suggested split**: Move to `lruoffloadmanager.py`

---

### 3. `WeightedLRUManager`

**Line**: 224  
**Inherits**: LRUOffloadManager  
**Methods**: 3

Weighted LRU with access frequency consideration.

Combines recency with access frequency for smarter eviction.

[TIP] **Suggested split**: Move to `weightedlrumanager.py`

---

### 4. `TieredLRUManager`

**Line**: 310  
**Methods**: 6

Multi-tier LRU manager with hot/warm/cold tiers.

Blocks are promoted through tiers based on access patterns.

[TIP] **Suggested split**: Move to `tieredlrumanager.py`

---

### 5. `PrefetchingLRUManager`

**Line**: 409  
**Inherits**: LRUOffloadManager  
**Methods**: 4

LRU manager with prefetching support.

Maintains prefetch hints to proactively load blocks.

[TIP] **Suggested split**: Move to `prefetchinglrumanager.py`

---

### 6. `AsyncLRUManager`

**Line**: 450  
**Methods**: 1

Async wrapper for LRU offloading manager.

[TIP] **Suggested split**: Move to `asynclrumanager.py`

---

### 7. `LRUManagerFactory`

**Line**: 485  
**Methods**: 4

Factory for creating LRU managers.

[TIP] **Suggested split**: Move to `lrumanagerfactory.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
