# Class Breakdown: tool_framework_mixin

**File**: `src\core\base\mixins\tool_framework_mixin.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ToolParameter`

**Line**: 43  
**Methods**: 1

Represents a tool parameter with validation.

[TIP] **Suggested split**: Move to `toolparameter.py`

---

### 2. `ToolDefinition`

**Line**: 62  
**Methods**: 1

Complete definition of a tool.

[TIP] **Suggested split**: Move to `tooldefinition.py`

---

### 3. `ToolExecutionError`

**Line**: 81  
**Inherits**: Exception  
**Methods**: 0

Exception raised when tool execution fails.

[TIP] **Suggested split**: Move to `toolexecutionerror.py`

---

### 4. `ToolValidationError`

**Line**: 86  
**Inherits**: Exception  
**Methods**: 0

Exception raised when tool parameters are invalid.

[TIP] **Suggested split**: Move to `toolvalidationerror.py`

---

### 5. `ToolFrameworkMixin`

**Line**: 91  
**Methods**: 10

Mixin providing schema-based tool creation and management.
Inspired by Adorable's tool system with createTool() pattern.

[TIP] **Suggested split**: Move to `toolframeworkmixin.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
