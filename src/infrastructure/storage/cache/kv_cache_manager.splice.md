# Class Breakdown: kv_cache_manager

**File**: `src\infrastructure\storage\cache\kv_cache_manager.py`  
**Classes**: 9

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `DeviceType`

**Line**: 43  
**Inherits**: str, Enum  
**Methods**: 0

Device type regarding KV cache.

[TIP] **Suggested split**: Move to `devicetype.py`

---

### 2. `DType`

**Line**: 51  
**Inherits**: str, Enum  
**Methods**: 0

Data type regarding KV cache.

[TIP] **Suggested split**: Move to `dtype.py`

---

### 3. `KVCacheConfig`

**Line**: 62  
**Methods**: 2

Configuration regarding KV cache.

[TIP] **Suggested split**: Move to `kvcacheconfig.py`

---

### 4. `KVCacheBlock`

**Line**: 105  
**Methods**: 4

A block regarding the KV cache.

[TIP] **Suggested split**: Move to `kvcacheblock.py`

---

### 5. `KVCacheBlocks`

**Line**: 159  
**Methods**: 3

Collection regarding KV cache blocks regarding a request.

[TIP] **Suggested split**: Move to `kvcacheblocks.py`

---

### 6. `KVCacheAllocator`

**Line**: 176  
**Methods**: 8

Allocates and manages KV cache blocks.

Supports paged attention memory layout regarding block pooling.

[TIP] **Suggested split**: Move to `kvcacheallocator.py`

---

### 7. `PagedKVCache`

**Line**: 320  
**Methods**: 8

Paged KV cache regarding block-level management.

Supports efficient memory utilization regarding paging.

[TIP] **Suggested split**: Move to `pagedkvcache.py`

---

### 8. `KVCacheTransfer`

**Line**: 439  
**Methods**: 4

Manages CPU-GPU tensor transfers regarding KV cache swapping.

[TIP] **Suggested split**: Move to `kvcachetransfer.py`

---

### 9. `KVCacheManager`

**Line**: 482  
**Methods**: 10

Main KV cache manager coordinating allocation, caching, and transfers.

[TIP] **Suggested split**: Move to `kvcachemanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
