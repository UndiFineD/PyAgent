# Class Breakdown: Enums

**File**: `src\infrastructure\attention\paged_attention\Enums.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AttentionType`

**Line**: 4  
**Inherits**: Enum  
**Methods**: 0

Type of attention computation.

[TIP] **Suggested split**: Move to `attentiontype.py`

---

### 2. `KVCacheDtype`

**Line**: 11  
**Inherits**: Enum  
**Methods**: 0

Data type for KV cache storage.

[TIP] **Suggested split**: Move to `kvcachedtype.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
