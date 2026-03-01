# Class Breakdown: ToolCore

**File**: `src\infrastructure\orchestration\ToolCore.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ToolMetadata`

**Line**: 30  
**Inherits**: BaseModel  
**Methods**: 0

Metadata for a registered tool.

[TIP] **Suggested split**: Move to `toolmetadata.py`

---

### 2. `ToolCore`

**Line**: 40  
**Methods**: 5

Pure logic for tool registration and invocation.
Handles parameter introspection and argument filtering.

[TIP] **Suggested split**: Move to `toolcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
