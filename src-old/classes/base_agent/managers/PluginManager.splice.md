# Class Breakdown: PluginManager

**File**: `src\classes\base_agent\managers\PluginManager.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PluginMetadata`

**Line**: 38  
**Methods**: 0

Strictly typed metadata for a plugin.

[TIP] **Suggested split**: Move to `pluginmetadata.py`

---

### 2. `PluginManager`

**Line**: 48  
**Methods**: 7

Modernized PluginManager (Phase 226).
Handles discovery, manifest enforcement, health tracking, and graceful shutdown.

[TIP] **Suggested split**: Move to `pluginmanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
