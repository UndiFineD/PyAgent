# Class Breakdown: KVCacheManager

**File**: `src\infrastructure\cache\KVCacheManager.py`  
**Classes**: 9

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `DeviceType`

**Line**: 23  
**Inherits**: str, Enum  
**Methods**: 0

Device type for KV cache.

[TIP] **Suggested split**: Move to `devicetype.py`

---

### 2. `DType`

**Line**: 30  
**Inherits**: str, Enum  
**Methods**: 0

Data type for KV cache.

[TIP] **Suggested split**: Move to `dtype.py`

---

### 3. `KVCacheConfig`

**Line**: 40  
**Methods**: 2

Configuration for KV cache.

[TIP] **Suggested split**: Move to `kvcacheconfig.py`

---

### 4. `KVCacheBlock`

**Line**: 83  
**Methods**: 4

A block in the KV cache.

[TIP] **Suggested split**: Move to `kvcacheblock.py`

---

### 5. `KVCacheBlocks`

**Line**: 137  
**Methods**: 3

Collection of KV cache blocks for a request.

[TIP] **Suggested split**: Move to `kvcacheblocks.py`

---

### 6. `KVCacheAllocator`

**Line**: 154  
**Methods**: 8

Allocates and manages KV cache blocks.

Supports paged attention memory layout with block pooling.

[TIP] **Suggested split**: Move to `kvcacheallocator.py`

---

### 7. `PagedKVCache`

**Line**: 295  
**Methods**: 8

Paged KV cache with block-level management.

Supports efficient memory utilization through paging.

[TIP] **Suggested split**: Move to `pagedkvcache.py`

---

### 8. `KVCacheTransfer`

**Line**: 424  
**Methods**: 4

Manages CPU-GPU tensor transfers for KV cache swapping.

[TIP] **Suggested split**: Move to `kvcachetransfer.py`

---

### 9. `KVCacheManager`

**Line**: 464  
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
