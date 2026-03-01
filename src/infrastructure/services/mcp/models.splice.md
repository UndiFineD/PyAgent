# Class Breakdown: models

**File**: `src\infrastructure\services\mcp\models.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MCPServerType`

**Line**: 31  
**Inherits**: Enum  
**Methods**: 0

MCP server connection types.

[TIP] **Suggested split**: Move to `mcpservertype.py`

---

### 2. `ToolStatus`

**Line**: 41  
**Inherits**: Enum  
**Methods**: 0

Tool execution status.

[TIP] **Suggested split**: Move to `toolstatus.py`

---

### 3. `SessionState`

**Line**: 52  
**Inherits**: Enum  
**Methods**: 0

MCP session state.

[TIP] **Suggested split**: Move to `sessionstate.py`

---

### 4. `MCPServerConfig`

**Line**: 64  
**Methods**: 1

MCP server configuration.

[TIP] **Suggested split**: Move to `mcpserverconfig.py`

---

### 5. `ToolSchema`

**Line**: 91  
**Methods**: 3

Tool schema definition.

[TIP] **Suggested split**: Move to `toolschema.py`

---

### 6. `ToolCall`

**Line**: 137  
**Methods**: 1

Tool call request.

[TIP] **Suggested split**: Move to `toolcall.py`

---

### 7. `ToolResult`

**Line**: 163  
**Methods**: 2

Tool execution result.

[TIP] **Suggested split**: Move to `toolresult.py`

---

### 8. `MCPSession`

**Line**: 197  
**Methods**: 2

MCP session information.

[TIP] **Suggested split**: Move to `mcpsession.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
