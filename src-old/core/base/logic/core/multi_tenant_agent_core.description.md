# multi_tenant_agent_core

**File**: `src\core\base\logic\core\multi_tenant_agent_core.py`  
**Type**: Python Module  
**Summary**: 11 classes, 0 functions, 14 imports  
**Lines**: 560  
**Complexity**: 1 (simple)

## Overview

Multi-Tenant Agent Core

Implements multi-tenant agent orchestration patterns from AgentCloud.
Provides database-driven agent, task, and crew management with resource controls.
Based on AgentCloud's CrewAI platform architecture.

## Classes (11)

### `ProcessType`

**Inherits from**: str, Enum

Crew process types.

### `ToolType`

**Inherits from**: str, Enum

Tool types supported.

### `AgentStatus`

**Inherits from**: str, Enum

Agent status states.

### `TaskStatus`

**Inherits from**: str, Enum

Task execution status.

### `TenantConfig`

Configuration for a tenant.

### `AgentDefinition`

Agent definition with role and capabilities.

### `TaskDefinition`

Task definition with requirements and outputs.

### `CrewDefinition`

Crew definition for multi-agent orchestration.

### `ToolDefinition`

Tool definition with capabilities.

### `ExecutionResult`

Result of task/crew execution.

### `MultiTenantAgentCore`

**Inherits from**: BaseCore

Multi-tenant agent orchestration core based on AgentCloud patterns.

Features:
- Tenant isolation with resource limits
- Database-driven agent/task/crew management
- Multiple process types (sequential, hierarchical, consensual)
- Tool management and assignment
- Rate limiting and resource controls
- Execution tracking and monitoring

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (14):
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `enum.Enum`
- `logging`
- `src.core.base.common.base_core.BaseCore`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Union`
- `uuid`

---
*Auto-generated documentation*
