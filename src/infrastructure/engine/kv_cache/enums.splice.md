# Class Breakdown: enums

**File**: `src\infrastructure\engine\kv_cache\enums.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CacheGroupType`

**Line**: 23  
**Inherits**: Enum  
**Methods**: 0

Type of KV cache group.

[TIP] **Suggested split**: Move to `cachegrouptype.py`

---

### 2. `AllocationStrategy`

**Line**: 34  
**Inherits**: Enum  
**Methods**: 0

Block allocation strategy.

[TIP] **Suggested split**: Move to `allocationstrategy.py`

---

### 3. `EvictionPolicy`

**Line**: 43  
**Inherits**: Enum  
**Methods**: 0

Block eviction policy.

[TIP] **Suggested split**: Move to `evictionpolicy.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
