# Class Breakdown: structural

**File**: `src\infrastructure\engine\kv_cache\structural.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `FreeBlockQueue`

**Line**: 25  
**Methods**: 7

Doubly-linked list queue for free blocks with O(1) operations.
Maintains LRU order for eviction decisions.

[TIP] **Suggested split**: Move to `freeblockqueue.py`

---

### 2. `BlockHashCache`

**Line**: 91  
**Methods**: 5

Cache mapping block hashes to blocks for prefix caching.

[TIP] **Suggested split**: Move to `blockhashcache.py`

---

### 3. `BlockPool`

**Line**: 135  
**Methods**: 10

Manages allocation, caching, and eviction of KV cache blocks.

[TIP] **Suggested split**: Move to `blockpool.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
