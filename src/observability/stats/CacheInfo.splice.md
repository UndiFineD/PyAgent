# Class Breakdown: CacheInfo

**File**: `src\observability\stats\CacheInfo.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CacheStats`

**Line**: 20  
**Methods**: 5

Statistics for cache performance monitoring.

[TIP] **Suggested split**: Move to `cachestats.py`

---

### 2. `CacheEntry`

**Line**: 70  
**Inherits**: Unknown  
**Methods**: 1

A cache entry with value, timestamp, and pin status.

[TIP] **Suggested split**: Move to `cacheentry.py`

---

### 3. `LRUCache`

**Line**: 84  
**Inherits**: Unknown  
**Methods**: 23

Thread-safe LRU cache with hit statistics and pinned items.

Features:
- Hit/miss tracking with statistics
- Pinned items that won't be evicted
- Delta statistics (changes since last check)
- Touch op...

[TIP] **Suggested split**: Move to `lrucache.py`

---

### 4. `TTLLRUCache`

**Line**: 396  
**Inherits**: Unknown  
**Methods**: 1

LRU Cache with mandatory TTL.

Convenience class for caches that always need TTL.

[TIP] **Suggested split**: Move to `ttllrucache.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
