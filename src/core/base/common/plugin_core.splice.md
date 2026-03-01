# Class Breakdown: plugin_core

**File**: `src\core\base\common\plugin_core.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PluginMetadata`

**Line**: 48  
**Methods**: 1

Strictly typed metadata for a plugin.

[TIP] **Suggested split**: Move to `pluginmetadata.py`

---

### 2. `PluginCore`

**Line**: 67  
**Inherits**: BaseCore  
**Methods**: 16

Authoritative engine for discovering and managing plugins.

[TIP] **Suggested split**: Move to `plugincore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
