# Class Breakdown: PrefixCache

**File**: `src\infrastructure\cache\PrefixCache.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `EvictionPolicy`

**Line**: 28  
**Inherits**: str, Enum  
**Methods**: 0

Cache eviction policy.

[TIP] **Suggested split**: Move to `evictionpolicy.py`

---

### 2. `PrefixCacheConfig`

**Line**: 37  
**Methods**: 0

Configuration for prefix cache.

[TIP] **Suggested split**: Move to `prefixcacheconfig.py`

---

### 3. `CacheBlock`

**Line**: 49  
**Methods**: 4

A cached block of tokens.

[TIP] **Suggested split**: Move to `cacheblock.py`

---

### 4. `PrefixCacheStats`

**Line**: 81  
**Methods**: 4

Statistics for prefix cache performance.

[TIP] **Suggested split**: Move to `prefixcachestats.py`

---

### 5. `PrefixCacheManager`

**Line**: 143  
**Methods**: 18

Manages prefix cache with hash-based content addressing.

Supports block sharing across requests with same prefix.

[TIP] **Suggested split**: Move to `prefixcachemanager.py`

---

### 6. `BlockHasher`

**Line**: 418  
**Methods**: 3

Configurable block hasher.

[TIP] **Suggested split**: Move to `blockhasher.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
