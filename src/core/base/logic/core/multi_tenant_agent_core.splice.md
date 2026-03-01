# Class Breakdown: multi_tenant_agent_core

**File**: `src\core\base\logic\core\multi_tenant_agent_core.py`  
**Classes**: 11

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ProcessType`

**Line**: 34  
**Inherits**: str, Enum  
**Methods**: 0

Crew process types.

[TIP] **Suggested split**: Move to `processtype.py`

---

### 2. `ToolType`

**Line**: 41  
**Inherits**: str, Enum  
**Methods**: 0

Tool types supported.

[TIP] **Suggested split**: Move to `tooltype.py`

---

### 3. `AgentStatus`

**Line**: 48  
**Inherits**: str, Enum  
**Methods**: 0

Agent status states.

[TIP] **Suggested split**: Move to `agentstatus.py`

---

### 4. `TaskStatus`

**Line**: 55  
**Inherits**: str, Enum  
**Methods**: 0

Task execution status.

[TIP] **Suggested split**: Move to `taskstatus.py`

---

### 5. `TenantConfig`

**Line**: 65  
**Methods**: 0

Configuration for a tenant.

[TIP] **Suggested split**: Move to `tenantconfig.py`

---

### 6. `AgentDefinition`

**Line**: 77  
**Methods**: 0

Agent definition with role and capabilities.

[TIP] **Suggested split**: Move to `agentdefinition.py`

---

### 7. `TaskDefinition`

**Line**: 96  
**Methods**: 0

Task definition with requirements and outputs.

[TIP] **Suggested split**: Move to `taskdefinition.py`

---

### 8. `CrewDefinition`

**Line**: 113  
**Methods**: 0

Crew definition for multi-agent orchestration.

[TIP] **Suggested split**: Move to `crewdefinition.py`

---

### 9. `ToolDefinition`

**Line**: 130  
**Methods**: 0

Tool definition with capabilities.

[TIP] **Suggested split**: Move to `tooldefinition.py`

---

### 10. `ExecutionResult`

**Line**: 142  
**Methods**: 0

Result of task/crew execution.

[TIP] **Suggested split**: Move to `executionresult.py`

---

### 11. `MultiTenantAgentCore`

**Line**: 153  
**Inherits**: BaseCore  
**Methods**: 1

Multi-tenant agent orchestration core based on AgentCloud patterns.

Features:
- Tenant isolation with resource limits
- Database-driven agent/task/crew management
- Multiple process types (sequential...

[TIP] **Suggested split**: Move to `multitenantagentcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
