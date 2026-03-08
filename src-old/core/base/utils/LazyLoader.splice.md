# Class Breakdown: LazyLoader

**File**: `src\core\base\utils\LazyLoader.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LazyModule`

**Line**: 17  
**Methods**: 5

A lazy module wrapper that defers import until first access.

Example:
    >>> math = LazyModule('math')
    >>> # 'math' is not imported yet
    >>> result = math.sqrt(16)  # Now 'math' is imported
 ...

[TIP] **Suggested split**: Move to `lazymodule.py`

---

### 2. `LazyImport`

**Line**: 73  
**Methods**: 2

Descriptor for lazy attribute imports within a module.

Used in __getattr__ pattern for package __init__.py files.

Example in __init__.py:
    MODULE_ATTRS = {
        'SomeClass': 'mypackage.submodu...

[TIP] **Suggested split**: Move to `lazyimport.py`

---

### 3. `DeferredImport`

**Line**: 149  
**Methods**: 5

Context manager for deferring imports.

Useful for optional dependencies that may not be installed.

Example:
    >>> with DeferredImport('torch') as torch:
    ...     if torch.available:
    ...    ...

[TIP] **Suggested split**: Move to `deferredimport.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
