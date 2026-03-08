# Class Breakdown: EnvConfig

**File**: `src\core\config\EnvConfig.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `EnvVar`

**Line**: 48  
**Inherits**: Unknown  
**Methods**: 7

Descriptor for type-safe environment variable access.

Provides automatic type conversion, default values, and validation.

Example:
    >>> class Config:
    ...     DEBUG = EnvVar("DEBUG", default=F...

[TIP] **Suggested split**: Move to `envvar.py`

---

### 2. `EnvConfigMeta`

**Line**: 295  
**Methods**: 0

Metadata for an environment configuration.

[TIP] **Suggested split**: Move to `envconfigmeta.py`

---

### 3. `EnvConfig`

**Line**: 304  
**Methods**: 4

Base class for environment-based configuration.

Subclass and add EnvVar descriptors for type-safe config.

Example:
    >>> class AppConfig(EnvConfig):
    ...     DEBUG = EnvVar("APP_DEBUG", default...

[TIP] **Suggested split**: Move to `envconfig.py`

---

### 4. `NamespacedConfig`

**Line**: 394  
**Methods**: 10

Configuration with automatic namespace prefixing.

Example:
    >>> config = NamespacedConfig("MYAPP")
    >>> config.get("DEBUG", False)  # Reads MYAPP_DEBUG
    >>> config.get("PORT", 8080)    # Rea...

[TIP] **Suggested split**: Move to `namespacedconfig.py`

---

### 5. `LazyEnvVar`

**Line**: 470  
**Inherits**: Unknown  
**Methods**: 3

Environment variable computed lazily on first access.

Useful when the default requires computation.

[TIP] **Suggested split**: Move to `lazyenvvar.py`

---

### 6. `temp_env`

**Line**: 521  
**Methods**: 3

Context manager for temporarily setting environment variables.

Example:
    >>> with temp_env(DEBUG="1", PORT="9000"):
    ...     print(os.environ.get("DEBUG"))  # "1"
    >>> print(os.environ.get("...

[TIP] **Suggested split**: Move to `temp_env.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
