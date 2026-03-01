# Class Breakdown: extension_registry

**File**: `src\core\base\registry\extension_registry.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ExtensionManager`

**Line**: 29  
**Methods**: 8

A registry for managing pluggable extension classes.

[TIP] **Suggested split**: Move to `extensionmanager.py`

---

### 2. `ExtensionInfo`

**Line**: 95  
**Methods**: 2

Information about a registered extension.

[TIP] **Suggested split**: Move to `extensioninfo.py`

---

### 3. `TypedExtensionManager`

**Line**: 107  
**Inherits**: ExtensionManager, Unknown  
**Methods**: 4

Type-safe extension manager for registering subclasses of a base type.

[TIP] **Suggested split**: Move to `typedextensionmanager.py`

---

### 4. `MultiExtensionManager`

**Line**: 140  
**Methods**: 6

Manager for multiple implementations per key with priority support.

[TIP] **Suggested split**: Move to `multiextensionmanager.py`

---

### 5. `LazyExtensionManager`

**Line**: 194  
**Inherits**: ExtensionManager  
**Methods**: 5

Lazy-loading extension manager that imports classes on demand.

[TIP] **Suggested split**: Move to `lazyextensionmanager.py`

---

### 6. `GlobalRegistry`

**Line**: 281  
**Inherits**: ExtensionManager  
**Methods**: 3

Global singleton registry with additional convenience methods.

[TIP] **Suggested split**: Move to `globalregistry.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
