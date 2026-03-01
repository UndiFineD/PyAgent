# Class Breakdown: sse

**File**: `src\infrastructure\mcp_tools\sse.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SSEMCPServer`

**Line**: 28  
**Inherits**: MCPToolServer  
**Methods**: 1

MCP server using Server-Sent Events.

[TIP] **Suggested split**: Move to `ssemcpserver.py`

---

### 2. `MockSSEClient`

**Line**: 163  
**Methods**: 1

Mock SSE client for testing.

[TIP] **Suggested split**: Move to `mocksseclient.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
