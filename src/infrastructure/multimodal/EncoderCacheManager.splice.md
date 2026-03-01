# Class Breakdown: EncoderCacheManager

**File**: `src\infrastructure\multimodal\EncoderCacheManager.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CacheTier`

**Line**: 45  
**Inherits**: Enum  
**Methods**: 0

Cache storage tier.

[TIP] **Suggested split**: Move to `cachetier.py`

---

### 2. `EvictionPolicy`

**Line**: 52  
**Inherits**: Enum  
**Methods**: 0

Cache eviction policy.

[TIP] **Suggested split**: Move to `evictionpolicy.py`

---

### 3. `CacheConfig`

**Line**: 61  
**Methods**: 1

Configuration for encoder cache.

[TIP] **Suggested split**: Move to `cacheconfig.py`

---

### 4. `CacheEntry`

**Line**: 81  
**Methods**: 4

A single cache entry.

[TIP] **Suggested split**: Move to `cacheentry.py`

---

### 5. `CacheStats`

**Line**: 114  
**Methods**: 3

Cache statistics.

[TIP] **Suggested split**: Move to `cachestats.py`

---

### 6. `EncoderCacheManager`

**Line**: 146  
**Methods**: 17

Manages caching of encoder outputs for multimodal models.

Implements vLLM's EncoderCacheManager with extensions:
- Content-based deduplication
- Reference counting
- LRU/LFU/Priority eviction
- Prefe...

[TIP] **Suggested split**: Move to `encodercachemanager.py`

---

### 7. `MultiTierEncoderCache`

**Line**: 515  
**Methods**: 5

Multi-tier encoder cache with memory, disk, and remote tiers.

Beyond vLLM: Hierarchical caching with automatic tier migration
and consistent access patterns.

[TIP] **Suggested split**: Move to `multitierencodercache.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
