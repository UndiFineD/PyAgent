# Class Breakdown: prefix_cache_manager

**File**: `src\infrastructure\engine\prefix_cache_manager.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `HashAlgorithm`

**Line**: 35  
**Inherits**: Enum  
**Methods**: 0

Supported hash algorithms dedicated to prefix caching.

[TIP] **Suggested split**: Move to `hashalgorithm.py`

---

### 2. `BlockHash`

**Line**: 44  
**Methods**: 2

Hash of a block's contents.

Includes the hash value and the token IDs supporting verification.

[TIP] **Suggested split**: Move to `blockhash.py`

---

### 3. `CacheBlock`

**Line**: 65  
**Methods**: 1

A cached KV block.

[TIP] **Suggested split**: Move to `cacheblock.py`

---

### 4. `PrefixCacheManager`

**Line**: 174  
**Methods**: 10

Manager dedicated to prefix caching with block-level granularity.

Implements content-addressable caching where blocks with the same
content (token IDs) share the same cached KV values.

[TIP] **Suggested split**: Move to `prefixcachemanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
