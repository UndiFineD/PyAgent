# Class Breakdown: ToolDraftingCore

**File**: `src\logic\agents\development\core\ToolDraftingCore.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ToolDefinition`

**Line**: 8  
**Methods**: 0

[TIP] **Suggested split**: Move to `tooldefinition.py`

---

### 2. `ToolDraftingCore`

**Line**: 14  
**Methods**: 3

Pure logic for agents generating their own OpenAPI tools.
Handles schema drafting, parameter validation, and endpoint mapping.

[TIP] **Suggested split**: Move to `tooldraftingcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
