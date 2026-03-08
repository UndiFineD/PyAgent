# Class Breakdown: hash_registry

**File**: `src\core\base\common\utils\hash_registry.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `HashAlgorithm`

**Line**: 56  
**Inherits**: Enum  
**Methods**: 0

Available hash algorithms.

[TIP] **Suggested split**: Move to `hashalgorithm.py`

---

### 2. `ContentHasher`

**Line**: 266  
**Methods**: 4

Configurable content hasher for cache keys.

Example:
    >>> hasher = ContentHasher(algorithm='xxhash64', prefix='cache')
    >>> key = hasher.hash("some content")
    >>> print(key)  # cache:a1b2c3d...

[TIP] **Suggested split**: Move to `contenthasher.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
