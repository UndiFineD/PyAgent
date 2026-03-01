# Class Breakdown: lazy_loader

**File**: `src\core\lazy_loader.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LazyLoader`

**Line**: 56  
**Methods**: 4

A descriptor class for deferred imports.

LazyLoader delays the import of a module/attribute until first access,
reducing startup time for modules with expensive imports.

Attributes:
    module_path:...

[TIP] **Suggested split**: Move to `lazyloader.py`

---

### 2. `ModuleLazyLoader`

**Line**: 170  
**Methods**: 11

A utility class for implementing module-level __getattr__ lazy loading.

This class provides a clean way to implement the PEP 562 __getattr__ pattern
for lazy loading of module-level attributes. It ma...

[TIP] **Suggested split**: Move to `modulelazyloader.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
