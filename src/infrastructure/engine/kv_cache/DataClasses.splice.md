# Class Breakdown: DataClasses

**File**: `src\infrastructure\engine\kv_cache\DataClasses.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BlockHash`

**Line**: 8  
**Methods**: 3

Immutable block hash for prefix caching.

[TIP] **Suggested split**: Move to `blockhash.py`

---

### 2. `BlockHashWithGroupId`

**Line**: 27  
**Methods**: 1

Block hash combined with group ID for multi-group caching.

[TIP] **Suggested split**: Move to `blockhashwithgroupid.py`

---

### 3. `KVCacheBlock`

**Line**: 37  
**Methods**: 2

KV cache block metadata.

[TIP] **Suggested split**: Move to `kvcacheblock.py`

---

### 4. `KVCacheBlocks`

**Line**: 66  
**Methods**: 4

Allocation result for multi-group KV cache.

[TIP] **Suggested split**: Move to `kvcacheblocks.py`

---

### 5. `CacheGroupSpec`

**Line**: 96  
**Methods**: 2

Specification for a KV cache group.

[TIP] **Suggested split**: Move to `cachegroupspec.py`

---

### 6. `CacheConfig`

**Line**: 119  
**Methods**: 0

Configuration for KV cache.

[TIP] **Suggested split**: Move to `cacheconfig.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
