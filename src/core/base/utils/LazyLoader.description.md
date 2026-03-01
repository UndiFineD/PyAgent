# LazyLoader

**File**: `src\core\base\utils\LazyLoader.py`  
**Type**: Python Module  
**Summary**: 3 classes, 3 functions, 7 imports  
**Lines**: 273  
**Complexity**: 15 (moderate)

## Overview

LazyLoader - Lazy module loading utilities.

Inspired by vLLM's __getattr__ pattern for reducing import costs.
Only loads modules when they are actually accessed.

Phase 17: vLLM Pattern Integration (P2)

## Classes (3)

### `LazyModule`

A lazy module wrapper that defers import until first access.

Example:
    >>> math = LazyModule('math')
    >>> # 'math' is not imported yet
    >>> result = math.sqrt(16)  # Now 'math' is imported
    >>> print(result)  # 4.0

**Methods** (5):
- `__init__(self, module_name)`
- `_load(self)`
- `__getattr__(self, name)`
- `__setattr__(self, name, value)`
- `__repr__(self)`

### `LazyImport`

Descriptor for lazy attribute imports within a module.

Used in __getattr__ pattern for package __init__.py files.

Example in __init__.py:
    MODULE_ATTRS = {
        'SomeClass': 'mypackage.submodule:SomeClass',
        'helper_func': 'mypackage.utils:helper_func',
    }
    
    def __getattr__(name):
        if name in MODULE_ATTRS:
            return LazyImport.load(MODULE_ATTRS[name])
        raise AttributeError(f"module has no attribute '{name}'")

**Methods** (2):
- `load(spec)`
- `create_getattr(module_attrs)`

### `DeferredImport`

Context manager for deferring imports.

Useful for optional dependencies that may not be installed.

Example:
    >>> with DeferredImport('torch') as torch:
    ...     if torch.available:
    ...         tensor = torch.module.zeros(10)
    ...     else:
    ...         print("PyTorch not available")

**Methods** (5):
- `__init__(self, module_name)`
- `__enter__(self)`
- `__exit__(self)`
- `available(self)`
- `module(self)`

## Functions (3)

### `lazy_import(module_name)`

Create a lazy module reference.

Args:
    module_name: Full module path (e.g., 'numpy', 'torch.nn')
    
Returns:
    LazyModule that imports on first access
    
Example:
    >>> np = lazy_import('numpy')
    >>> # numpy not imported yet
    >>> arr = np.array([1, 2, 3])  # Now imported

### `optional_import(module_name, fallback)`

Import a module if available, with fallback.

Args:
    module_name: Module to import
    fallback: Value to return if import fails
    
Returns:
    Tuple of (module_or_fallback, is_available)
    
Example:
    >>> torch, has_torch = optional_import('torch')
    >>> if has_torch:
    ...     device = torch.device('cuda')

### `require_import(module_name, package_name)`

Import a module or raise a helpful error.

Args:
    module_name: Module to import
    package_name: Package name for pip install hint (defaults to module_name)
    
Returns:
    The imported module
    
Raises:
    ImportError: With helpful installation instructions

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `importlib`
- `sys`
- `typing.Any`
- `typing.Callable`
- `typing.TYPE_CHECKING`
- `typing.TypeVar`

---
*Auto-generated documentation*
