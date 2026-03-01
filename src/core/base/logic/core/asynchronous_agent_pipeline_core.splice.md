# Class Breakdown: asynchronous_agent_pipeline_core

**File**: `src\core\base\logic\core\asynchronous_agent_pipeline_core.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ToolCall`

**Line**: 36  
**Methods**: 0

Represents a tool call request

[TIP] **Suggested split**: Move to `toolcall.py`

---

### 2. `ToolResult`

**Line**: 46  
**Methods**: 0

Result from tool execution

[TIP] **Suggested split**: Move to `toolresult.py`

---

### 3. `Trajectory`

**Line**: 58  
**Methods**: 0

Complete trajectory from state to reward

[TIP] **Suggested split**: Move to `trajectory.py`

---

### 4. `AsynchronousAgentPipelineCore`

**Line**: 68  
**Methods**: 4

Core implementing asynchronous agent pipeline pattern.

Decouples inference, tool execution, and learning into parallel components
communicating via queues to eliminate compute bubbles.

[TIP] **Suggested split**: Move to `asynchronousagentpipelinecore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
