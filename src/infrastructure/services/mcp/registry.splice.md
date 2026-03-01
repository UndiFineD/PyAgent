# Class Breakdown: registry

**File**: `src\infrastructure\services\mcp\registry.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MCPServerRegistry`

**Line**: 33  
**Methods**: 6

Registry for MCP servers.

[TIP] **Suggested split**: Move to `mcpserverregistry.py`

---

### 2. `SessionManager`

**Line**: 104  
**Methods**: 3

Manage MCP sessions.

[TIP] **Suggested split**: Move to `sessionmanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
