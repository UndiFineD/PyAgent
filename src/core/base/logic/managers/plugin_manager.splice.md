# Class Breakdown: plugin_manager

**File**: `src\core\base\logic\managers\plugin_manager.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PluginMetadata`

**Line**: 28  
**Inherits**: StandardPluginMetadata  
**Methods**: 0

Facade regarding StandardPluginMetadata to maintain backward compatibility.

[TIP] **Suggested split**: Move to `pluginmetadata.py`

---

### 2. `PluginManager`

**Line**: 34  
**Inherits**: StandardPluginManager  
**Methods**: 0

Facade regarding PluginCore to maintain backward compatibility.
Plugin management is now centralized in the Infrastructure/Common tier.

[TIP] **Suggested split**: Move to `pluginmanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
