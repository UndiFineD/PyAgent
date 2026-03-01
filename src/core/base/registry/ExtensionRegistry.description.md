# ExtensionRegistry

**File**: `src\core\base\registry\ExtensionRegistry.py`  
**Type**: Python Module  
**Summary**: 6 classes, 5 functions, 18 imports  
**Lines**: 575  
**Complexity**: 47 (complex)

## Overview

Extension Registry Module - Phase 20: Production Infrastructure
================================================================

Plugin system for managing extensible component registries.
Inspired by vLLM's registry.py pattern.

Features:
- ExtensionManager: Register and instantiate extension classes by name
- TypedExtensionManager: Generic typed extension registry
- MultiExtensionManager: Registry supporting multiple implementations
- @register decorator: Easy class registration
- Lazy instantiation: Classes loaded only when accessed
- Priority ordering: Extensions can define priority

Author: PyAgent Phase 20

## Classes (6)

### `ExtensionManager`

A registry for managing pluggable extension classes.

Provides a simple mechanism to register and instantiate extension classes
by name. Commonly used for plugin systems where different implementations
can be swapped at runtime.

Example:
    >>> FOO_REGISTRY = ExtensionManager("foo")
    >>> @FOO_REGISTRY.register("my_impl")
    ... class MyFooImpl:
    ...     def __init__(self, value: int):
    ...         self.value = value
    >>> foo = FOO_REGISTRY.load("my_impl", value=123)
    >>> foo.value
    123

**Methods** (11):
- `__init__(self, name)`
- `register(self, name)`
- `register_class(self, name, cls)`
- `unregister(self, name)`
- `load(self, cls_name)`
- `get_class(self, cls_name)`
- `has(self, name)`
- `list_registered(self)`
- `__contains__(self, name)`
- `__len__(self)`
- ... and 1 more methods

### `TypedExtensionManager`

**Inherits from**: Unknown

A type-safe registry for managing extension classes of a specific base type.

Example:
    >>> class BasePlugin(ABC):
    ...     @abstractmethod
    ...     def process(self, data: str) -> str: ...
    >>> PLUGINS = TypedExtensionManager[BasePlugin]("plugins", BasePlugin)
    >>> @PLUGINS.register("upper")
    ... class UpperPlugin(BasePlugin):
    ...     def process(self, data: str) -> str:
    ...         return data.upper()

**Methods** (8):
- `__init__(self, name, base_class)`
- `register(self, name)`
- `load(self, cls_name)`
- `get_class(self, cls_name)`
- `has(self, name)`
- `list_registered(self)`
- `__contains__(self, name)`
- `__len__(self)`

### `ExtensionInfo`

Metadata for a registered extension.

**Methods** (1):
- `__lt__(self, other)`

### `MultiExtensionManager`

Registry supporting multiple implementations per key with priority ordering.

Useful for plugin systems where multiple handlers can be registered
for the same extension point.

Example:
    >>> HANDLERS = MultiExtensionManager("handlers")
    >>> @HANDLERS.register("format", priority=10)
    ... class JSONFormatter: ...
    >>> @HANDLERS.register("format", priority=5)
    ... class XMLFormatter: ...
    >>> HANDLERS.get_all("format")  # Returns [JSONFormatter, XMLFormatter]

**Methods** (10):
- `__init__(self, name)`
- `register(self, name, priority)`
- `get_first(self, name)`
- `get_all(self, name)`
- `get_classes(self, name)`
- `get_infos(self, name)`
- `has(self, name)`
- `list_extension_points(self)`
- `count(self, name)`
- `clear(self, name)`

### `LazyExtensionManager`

Extension manager with lazy module loading.

Extensions are specified as 'module:class' strings and only loaded
when accessed.

Example:
    >>> LAZY = LazyExtensionManager("lazy")
    >>> LAZY.register_lazy("json", "json:JSONEncoder")
    >>> encoder = LAZY.load("json")  # Imports json module only now

**Methods** (8):
- `__init__(self, name)`
- `register_lazy(self, name, spec)`
- `_import_class(self, spec)`
- `load(self, name)`
- `get_class(self, name)`
- `has(self, name)`
- `is_loaded(self, name)`
- `list_registered(self)`

### `GlobalRegistry`

A singleton registry for managing multiple extension managers.

Provides a centralized way to access all extension registries.

**Methods** (4):
- `__new__(cls)`
- `get_or_create(self, name)`
- `get(self, name)`
- `list_managers(self)`

## Functions (5)

### `get_global_registry()`

Get the global extension registry.

### `create_registry(name)`

Create a new extension manager with the given name.

### `create_typed_registry(name, base_class)`

Create a new typed extension manager.

### `create_multi_registry(name)`

Create a new multi-extension manager.

### `create_lazy_registry(name)`

Create a new lazy extension manager.

## Dependencies

**Imports** (18):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `dataclasses.dataclass`
- `dataclasses.field`
- `functools.wraps`
- `importlib`
- `logging`
- `threading`
- `typing.Any`
- `typing.Callable`
- `typing.ClassVar`
- `typing.Generic`
- `typing.Protocol`
- `typing.TYPE_CHECKING`
- ... and 3 more

---
*Auto-generated documentation*
