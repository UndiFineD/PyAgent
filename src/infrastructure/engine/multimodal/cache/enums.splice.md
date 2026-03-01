# Class Breakdown: enums

**File**: `src\infrastructure\engine\multimodal\cache\enums.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MediaType`

**Line**: 22  
**Inherits**: Enum  
**Methods**: 0

Types of media content.

[TIP] **Suggested split**: Move to `mediatype.py`

---

### 2. `CacheBackend`

**Line**: 33  
**Inherits**: Enum  
**Methods**: 0

Cache storage backend types.

[TIP] **Suggested split**: Move to `cachebackend.py`

---

### 3. `HashAlgorithm`

**Line**: 43  
**Inherits**: Enum  
**Methods**: 0

Hash algorithms for content addressing.

[TIP] **Suggested split**: Move to `hashalgorithm.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
