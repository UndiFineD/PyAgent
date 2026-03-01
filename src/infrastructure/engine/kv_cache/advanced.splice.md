# Class Breakdown: advanced

**File**: `src\infrastructure\engine\kv_cache\advanced.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `HierarchicalKVCacheCoordinator`

**Line**: 26  
**Inherits**: KVCacheCoordinator  
**Methods**: 2

Hierarchical coordinator for complex model architectures.

[TIP] **Suggested split**: Move to `hierarchicalkvcachecoordinator.py`

---

### 2. `PredictiveKVCacheCoordinator`

**Line**: 41  
**Inherits**: KVCacheCoordinator  
**Methods**: 4

Coordinator with predictive allocation based on request patterns.

[TIP] **Suggested split**: Move to `predictivekvcachecoordinator.py`

---

### 3. `AsyncPrefetchCoordinator`

**Line**: 70  
**Inherits**: KVCacheCoordinator  
**Methods**: 3

Coordinator with async prefetch support.

[TIP] **Suggested split**: Move to `asyncprefetchcoordinator.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
