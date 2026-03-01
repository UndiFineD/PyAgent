# Class Breakdown: env_config

**File**: `src\core\config\env_config.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `EnvVar`

**Line**: 48  
**Inherits**: Unknown  
**Methods**: 8

Descriptor for type-safe environment variable access.

Provides automatic type conversion, default values, and validation.

Example:
    >>> class Config:
    ...     DEBUG = EnvVar("DEBUG", default=F...

[TIP] **Suggested split**: Move to `envvar.py`

---

### 2. `EnvConfigMeta`

**Line**: 312  
**Methods**: 0

Metadata for an environment configuration.

[TIP] **Suggested split**: Move to `envconfigmeta.py`

---

### 3. `EnvConfig`

**Line**: 322  
**Methods**: 7

Base class for environment-based configuration.

Subclass and add EnvVar descriptors for type-safe config.

Example:
    >>> class AppConfig(EnvConfig):
    ...     DEBUG = EnvVar("APP_DEBUG", default...

[TIP] **Suggested split**: Move to `envconfig.py`

---

### 4. `NamespacedConfig`

**Line**: 435  
**Methods**: 10

Configuration with automatic namespace prefixing.

Example:
    >>> config = NamespacedConfig("MYAPP")
    >>> config.get("DEBUG", False)  # Reads MYAPP_DEBUG
    >>> config.get("PORT", 8080)    # Rea...

[TIP] **Suggested split**: Move to `namespacedconfig.py`

---

### 5. `LazyEnvVar`

**Line**: 508  
**Inherits**: Unknown  
**Methods**: 4

Environment variable computed lazily on first access.

Useful when the default requires computation.

[TIP] **Suggested split**: Move to `lazyenvvar.py`

---

### 6. `TempEnv`

**Line**: 565  
**Methods**: 3

Context manager for temporarily setting environment variables.

Example usage:
    >>> with TempEnv(DEBUG="1"):
    ...     print(os.environ.get("DEBUG"))  # "1"
    >>> print(os.environ.get("DEBUG"))...

[TIP] **Suggested split**: Move to `tempenv.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
