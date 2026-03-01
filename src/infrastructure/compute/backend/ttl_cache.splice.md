# Class Breakdown: ttl_cache

**File**: `src\infrastructure\compute\backend\ttl_cache.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CachedResponse`

**Line**: 31  
**Methods**: 0

Structure for a cached response with metadata.

[TIP] **Suggested split**: Move to `cachedresponse.py`

---

### 2. `TTLCache`

**Line**: 40  
**Inherits**: StandardCacheCore  
**Methods**: 7

Caches responses with configurable TTL, automatically expiring stale entries.

Example:
    cache = TTLCache(default_ttl_seconds=300)
    cache.set("key", "value")
    result = cache.get("key")  # Ret...

[TIP] **Suggested split**: Move to `ttlcache.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
