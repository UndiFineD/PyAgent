# Class Breakdown: multi_agent_orchestrator

**File**: `src\core\base\logic\multi_agent_orchestrator.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AgentMetadata`

**Line**: 47  
**Methods**: 0

Metadata for registered agents.

[TIP] **Suggested split**: Move to `agentmetadata.py`

---

### 2. `TaskResult`

**Line**: 61  
**Methods**: 0

Result of an agent task execution.

[TIP] **Suggested split**: Move to `taskresult.py`

---

### 3. `MultiAgentOrchestratorCore`

**Line**: 73  
**Methods**: 13

Unified orchestrator for managing multiple agent types.

Provides a centralized system for:
- Agent registration and lifecycle management
- Task dispatch and execution tracking
- Working directory man...

[TIP] **Suggested split**: Move to `multiagentorchestratorcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
