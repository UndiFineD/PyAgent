# Class Breakdown: ExtensionRegistry

**File**: `src\core\base\registry\ExtensionRegistry.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ExtensionManager`

**Line**: 52  
**Methods**: 11

A registry for managing pluggable extension classes.

Provides a simple mechanism to register and instantiate extension classes
by name. Commonly used for plugin systems where different implementation...

[TIP] **Suggested split**: Move to `extensionmanager.py`

---

### 2. `TypedExtensionManager`

**Line**: 192  
**Inherits**: Unknown  
**Methods**: 8

A type-safe registry for managing extension classes of a specific base type.

Example:
    >>> class BasePlugin(ABC):
    ...     @abstractmethod
    ...     def process(self, data: str) -> str: ...
 ...

[TIP] **Suggested split**: Move to `typedextensionmanager.py`

---

### 3. `ExtensionInfo`

**Line**: 282  
**Methods**: 1

Metadata for a registered extension.

[TIP] **Suggested split**: Move to `extensioninfo.py`

---

### 4. `MultiExtensionManager`

**Line**: 293  
**Methods**: 10

Registry supporting multiple implementations per key with priority ordering.

Useful for plugin systems where multiple handlers can be registered
for the same extension point.

Example:
    >>> HANDLE...

[TIP] **Suggested split**: Move to `multiextensionmanager.py`

---

### 5. `LazyExtensionManager`

**Line**: 403  
**Methods**: 8

Extension manager with lazy module loading.

Extensions are specified as 'module:class' strings and only loaded
when accessed.

Example:
    >>> LAZY = LazyExtensionManager("lazy")
    >>> LAZY.regist...

[TIP] **Suggested split**: Move to `lazyextensionmanager.py`

---

### 6. `GlobalRegistry`

**Line**: 491  
**Methods**: 4

A singleton registry for managing multiple extension managers.

Provides a centralized way to access all extension registries.

[TIP] **Suggested split**: Move to `globalregistry.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
