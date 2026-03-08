# Class Breakdown: bridge

**File**: `src\tools\mcp\bridge.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MCPServerType`

**Line**: 44  
**Inherits**: Enum  
**Methods**: 0

Types of MCP servers.

[TIP] **Suggested split**: Move to `mcpservertype.py`

---

### 2. `MCPCategory`

**Line**: 52  
**Inherits**: Enum  
**Methods**: 0

MCP server categories.

[TIP] **Suggested split**: Move to `mcpcategory.py`

---

### 3. `MCPServerConfig`

**Line**: 67  
**Methods**: 0

Configuration for an MCP server.

[TIP] **Suggested split**: Move to `mcpserverconfig.py`

---

### 4. `MCPTool`

**Line**: 87  
**Methods**: 0

Represents an MCP tool.

[TIP] **Suggested split**: Move to `mcptool.py`

---

### 5. `MCPServerRegistry`

**Line**: 97  
**Methods**: 8

Registry of available MCP servers.

Manages discovery, configuration, and lifecycle of MCP servers.

[TIP] **Suggested split**: Move to `mcpserverregistry.py`

---

### 6. `MCPServerInstance`

**Line**: 254  
**Methods**: 1

Instance of a running MCP server.

Manages the lifecycle of an MCP server process.

[TIP] **Suggested split**: Move to `mcpserverinstance.py`

---

### 7. `MCPBridge`

**Line**: 422  
**Methods**: 4

MCP Protocol Bridge.

Provides standardized interface for external services through MCP servers.

[TIP] **Suggested split**: Move to `mcpbridge.py`

---

### 8. `MCPToolOrchestrator`

**Line**: 521  
**Methods**: 1

Intelligent tool selection and orchestration.

Uses AI to select the best MCP tools for a given task.

[TIP] **Suggested split**: Move to `mcptoolorchestrator.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
