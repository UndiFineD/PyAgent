# Class Breakdown: base

**File**: `src\infrastructure\services\tools\parser\base.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ToolParserType`

**Line**: 35  
**Inherits**: Enum  
**Methods**: 0

Supported tool parser types.

[TIP] **Suggested split**: Move to `toolparsertype.py`

---

### 2. `ToolCallStatus`

**Line**: 50  
**Inherits**: Enum  
**Methods**: 0

Tool call parsing status.

[TIP] **Suggested split**: Move to `toolcallstatus.py`

---

### 3. `ToolParameter`

**Line**: 65  
**Methods**: 0

Tool parameter definition.

[TIP] **Suggested split**: Move to `toolparameter.py`

---

### 4. `ToolCall`

**Line**: 77  
**Methods**: 2

Parsed tool/function call.

[TIP] **Suggested split**: Move to `toolcall.py`

---

### 5. `ToolParseResult`

**Line**: 110  
**Methods**: 2

Result of tool call parsing.

[TIP] **Suggested split**: Move to `toolparseresult.py`

---

### 6. `StreamingToolState`

**Line**: 129  
**Methods**: 0

State for streaming tool parsing.

[TIP] **Suggested split**: Move to `streamingtoolstate.py`

---

### 7. `ToolParser`

**Line**: 146  
**Inherits**: ABC  
**Methods**: 4

Base class for tool parsers.

[TIP] **Suggested split**: Move to `toolparser.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
