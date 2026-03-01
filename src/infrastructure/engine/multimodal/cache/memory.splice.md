# Class Breakdown: memory

**File**: `src\infrastructure\engine\multimodal\cache\memory.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MemoryMultiModalCache`

**Line**: 29  
**Inherits**: MultiModalCache  
**Methods**: 7

In-memory LRU cache for multimodal content.

[TIP] **Suggested split**: Move to `memorymultimodalcache.py`

---

### 2. `PerceptualCache`

**Line**: 123  
**Inherits**: MemoryMultiModalCache  
**Methods**: 3

Cache with perceptual similarity matching.

[TIP] **Suggested split**: Move to `perceptualcache.py`

---

### 3. `PrefetchMultiModalCache`

**Line**: 175  
**Inherits**: MemoryMultiModalCache  
**Methods**: 5

Cache with async prefetch support.

[TIP] **Suggested split**: Move to `prefetchmultimodalcache.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
