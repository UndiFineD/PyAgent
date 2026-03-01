# EnvConfig

**File**: `src\core\config\EnvConfig.py`  
**Type**: Python Module  
**Summary**: 6 classes, 6 functions, 17 imports  
**Lines**: 585  
**Complexity**: 33 (complex)

## Overview

Environment Configuration Module - Phase 20: Production Infrastructure
========================================================================

Type-safe environment variable access with defaults and validation.
Inspired by vLLM's envs.py pattern.

Features:
- Type-safe environment variable access
- Default values with proper typing
- Validation and transformation
- Lazy evaluation support
- Configuration namespacing
- Environment variable documentation

Author: PyAgent Phase 20

## Classes (6)

### `EnvVar`

**Inherits from**: Unknown

Descriptor for type-safe environment variable access.

Provides automatic type conversion, default values, and validation.

Example:
    >>> class Config:
    ...     DEBUG = EnvVar("DEBUG", default=False)
    ...     PORT = EnvVar("PORT", default=8080)
    ...     HOST = EnvVar("HOST", default="localhost")
    >>> config = Config()
    >>> config.DEBUG  # Returns False or bool from DEBUG env var

**Methods** (7):
- `__init__(self, name, default)`
- `get(self)`
- `_auto_convert(self, raw_value)`
- `reset_cache(self)`
- `__get__(self, obj, objtype)`
- `__set__(self, obj, value)`
- `__repr__(self)`

### `EnvConfigMeta`

Metadata for an environment configuration.

### `EnvConfig`

Base class for environment-based configuration.

Subclass and add EnvVar descriptors for type-safe config.

Example:
    >>> class AppConfig(EnvConfig):
    ...     DEBUG = EnvVar("APP_DEBUG", default=False, description="Enable debug mode")
    ...     PORT = EnvVar("APP_PORT", default=8080, description="Server port")
    ...     
    ...     class Meta:
    ...         prefix = "APP_"
    >>> config = AppConfig()
    >>> config.DEBUG
    False

**Methods** (4):
- `reset_all_caches(cls)`
- `get_metadata(cls)`
- `to_dict(cls)`
- `print_config(cls, mask_secrets)`

### `NamespacedConfig`

Configuration with automatic namespace prefixing.

Example:
    >>> config = NamespacedConfig("MYAPP")
    >>> config.get("DEBUG", False)  # Reads MYAPP_DEBUG
    >>> config.get("PORT", 8080)    # Reads MYAPP_PORT

**Methods** (10):
- `__init__(self, namespace, sep)`
- `_full_name(self, name)`
- `get(self, name, default)`
- `get_bool(self, name, default)`
- `get_int(self, name, default)`
- `get_float(self, name, default)`
- `get_list(self, name, default, sep)`
- `set(self, name, value)`
- `reset_cache(self)`
- `to_dict(self)`

### `LazyEnvVar`

**Inherits from**: Unknown

Environment variable computed lazily on first access.

Useful when the default requires computation.

**Methods** (3):
- `__init__(self, name, default_factory)`
- `get(self)`
- `reset(self)`

### `temp_env`

Context manager for temporarily setting environment variables.

Example:
    >>> with temp_env(DEBUG="1", PORT="9000"):
    ...     print(os.environ.get("DEBUG"))  # "1"
    >>> print(os.environ.get("DEBUG"))  # Original value

**Methods** (3):
- `__init__(self)`
- `__enter__(self)`
- `__exit__(self)`

## Functions (6)

### `get_env(name, default)`

Get an environment variable with type conversion.

Args:
    name: Environment variable name.
    default: Default value if not set.
    type_: Expected type (inferred from default if not provided).

Returns:
    The environment variable value, converted to the appropriate type.

### `get_env_bool(name, default)`

Get a boolean environment variable.

### `get_env_int(name, default)`

Get an integer environment variable.

### `get_env_float(name, default)`

Get a float environment variable.

### `get_env_list(name, default, sep)`

Get a list environment variable (comma-separated by default).

Args:
    name: Environment variable name.
    default: Default value if not set.
    sep: Separator for splitting the value.

### `get_env_json(name, default)`

Get a JSON-encoded environment variable.

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `functools`
- `json`
- `logging`
- `os`
- `typing.Any`
- `typing.Callable`
- `typing.Generic`
- `typing.Literal`
- `typing.TYPE_CHECKING`
- `typing.TypeVar`
- `typing.get_args`
- `typing.get_origin`
- ... and 2 more

---
*Auto-generated documentation*
