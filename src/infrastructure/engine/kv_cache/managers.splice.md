# Class Breakdown: managers

**File**: `src\infrastructure\engine\kv_cache\managers.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SingleTypeKVCacheManager`

**Line**: 26  
**Inherits**: ABC  
**Methods**: 5

Abstract base for single-type KV cache management.

[TIP] **Suggested split**: Move to `singletypekvcachemanager.py`

---

### 2. `FullAttentionManager`

**Line**: 62  
**Inherits**: SingleTypeKVCacheManager  
**Methods**: 1

Manager for full (standard) causal attention KV cache.

[TIP] **Suggested split**: Move to `fullattentionmanager.py`

---

### 3. `SlidingWindowManager`

**Line**: 70  
**Inherits**: SingleTypeKVCacheManager  
**Methods**: 1

Manager for sliding window attention KV cache.

[TIP] **Suggested split**: Move to `slidingwindowmanager.py`

---

### 4. `CrossAttentionManager`

**Line**: 80  
**Inherits**: SingleTypeKVCacheManager  
**Methods**: 1

Manager for cross-attention KV cache (fixed length prompt/encoder).

[TIP] **Suggested split**: Move to `crossattentionmanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
