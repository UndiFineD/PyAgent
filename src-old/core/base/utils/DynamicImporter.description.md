# DynamicImporter

**File**: `src\core\base\utils\DynamicImporter.py`  
**Type**: Python Module  
**Summary**: 3 classes, 13 functions, 12 imports  
**Lines**: 634  
**Complexity**: 32 (complex)

## Overview

DynamicImporter - Runtime import utilities for dynamic module loading.

Phase 22 implementation based on vLLM's import_utils.py patterns.
Provides utilities for runtime module loading, lazy imports, and qualified name resolution.

Features:
- import_from_path: Import module from filesystem path
- resolve_obj_by_qualname: Resolve "module.class" strings to objects
- lazy_import: Deferred module loading with placeholder
- safe_import: Import with fallback value on failure
- PlaceholderModule: Deferred import with informative error messages
- register_lazy_module: Registry pattern for lazy loading

Use Cases:
- Plugin systems that load modules at runtime
- Configuration-driven module selection
- Reducing startup time with lazy loading
- Testing with mock module substitution

## Classes (3)

### `PlaceholderModule`

A placeholder for a module that hasn't been imported yet.

Provides a helpful error message when accessed, explaining
that the module needs to be installed or is not available.

Attributes:
    module_name: Name of the module this is a placeholder for.
    install_hint: Optional hint for installing the module.
    reason: Optional reason why the module wasn't loaded.

**Methods** (6):
- `__init__(self, module_name)`
- `_raise_error(self)`
- `__getattr__(self, name)`
- `__call__(self)`
- `__repr__(self)`
- `is_placeholder(self)`

### `LazyModuleRegistry`

Registry for lazy module loading with deferred import.

Modules are registered with their import path but not loaded
until first access. This reduces startup time for rarely-used
modules.

Examples:
    >>> registry = LazyModuleRegistry()
    >>> registry.register("parser", "myapp.parsers.JSONParser")
    >>> # Module is not imported yet
    >>> parser_cls = registry.get("parser")  # Now it's imported

**Methods** (10):
- `__init__(self)`
- `register(self, name, qualname)`
- `register_many(self, mappings)`
- `get(self, name)`
- `__getitem__(self, name)`
- `__contains__(self, name)`
- `list_registered(self)`
- `is_loaded(self, name)`
- `preload(self)`
- `preload_all(self)`

### `LazyAttribute`

**Inherits from**: Unknown

A descriptor that lazily imports a module attribute.

Use this in classes to defer import until attribute access.

Examples:
    >>> class MyClass:
    ...     numpy = LazyAttribute("numpy")
    ...     json_dumps = LazyAttribute("json.dumps")
    ...
    >>> obj = MyClass()
    >>> obj.numpy.array([1, 2, 3])  # Imports numpy here

**Methods** (3):
- `__init__(self, qualname)`
- `__get__(self, obj, objtype)`
- `__set__(self, obj, value)`

## Functions (13)

### `import_from_path(module_name, file_path)`

Import a Python module from a filesystem path.

This allows importing modules that are not on sys.path.

Args:
    module_name: Name to give the imported module.
    file_path: Path to the Python file.
    add_to_sys_modules: Whether to add to sys.modules (default: True).
    
Returns:
    The imported module object.
    
Raises:
    FileNotFoundError: If the file doesn't exist.
    ImportError: If the module can't be loaded.
    
Examples:
    >>> mod = import_from_path("my_plugin", "/path/to/plugin.py")
    >>> mod.some_function()

### `resolve_obj_by_qualname(qualname)`

Resolve a fully qualified name to an object.

The qualname should be in the format "module.submodule.ClassName"
or "module.function_name".

Args:
    qualname: Fully qualified name like "collections.OrderedDict".
    
Returns:
    The resolved object (class, function, or module).
    
Raises:
    ImportError: If the module can't be imported.
    AttributeError: If the attribute doesn't exist.
    
Examples:
    >>> OrderedDict = resolve_obj_by_qualname("collections.OrderedDict")
    >>> OrderedDict()
    OrderedDict()
    >>> json_loads = resolve_obj_by_qualname("json.loads")
    >>> json_loads('{"a": 1}')
    {"a": 1}

### `resolve_obj_by_qualname_parts(module_path, attr_path)`

Resolve an object from module path and attribute path separately.

Args:
    module_path: The module to import (e.g., "collections").
    attr_path: Dot-separated path to attribute (e.g., "OrderedDict").
    
Returns:
    The resolved object.
    
Examples:
    >>> cls = resolve_obj_by_qualname_parts("json", "JSONEncoder")
    >>> isinstance(cls(), cls)
    True

### `lazy_import(module_name)`

Lazily import a module, returning a placeholder if not available.

This is useful for optional dependencies that may not be installed.

Args:
    module_name: Name of the module to import.
    install_hint: Installation command to show if import fails.
    
Returns:
    The module if available, or a PlaceholderModule otherwise.
    
Examples:
    >>> numpy = lazy_import("numpy", install_hint="pip install numpy")
    >>> # If numpy is installed, use it normally
    >>> # If not, access will raise a helpful error

### `safe_import(module_name, default)`

Safely import a module, returning a default value on failure.

Args:
    module_name: Name of the module to import.
    default: Value to return if import fails.
    
Returns:
    The module if available, or the default value.
    
Examples:
    >>> numpy = safe_import("numpy")  # Returns None if not installed
    >>> if numpy is not None:
    ...     arr = numpy.array([1, 2, 3])

### `register_lazy_module(name, qualname)`

Register a module for global lazy loading.

Args:
    name: Name to register under.
    qualname: Fully qualified name to import.

### `get_lazy_module(name)`

Get a globally registered lazy module.

Args:
    name: Registered name to look up.
    
Returns:
    The imported object.

### `reload_module(module)`

Reload a module, refreshing its code.

Args:
    module: Module object or name to reload.
    
Returns:
    The reloaded module.
    
Raises:
    ImportError: If module can't be reloaded.

### `unload_module(module_name)`

Unload a module from sys.modules.

Note: This doesn't unload dependencies or clean up references.

Args:
    module_name: Name of module to unload.
    
Returns:
    True if module was unloaded, False if not loaded.

### `is_module_available(module_name)`

Check if a module is available without importing it.

Args:
    module_name: Name of module to check.
    
Returns:
    True if module can be imported.

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `importlib`
- `importlib.util`
- `logging`
- `pathlib.Path`
- `sys`
- `types.ModuleType`
- `typing.Any`
- `typing.Callable`
- `typing.Generic`
- `typing.TypeVar`
- `typing.overload`

---
*Auto-generated documentation*
