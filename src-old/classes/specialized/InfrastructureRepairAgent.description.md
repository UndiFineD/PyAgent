# InfrastructureRepairAgent

**File**: `src\classes\specialized\InfrastructureRepairAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 63  
**Complexity**: 4 (simple)

## Overview

Agent for automated infrastructure and environment repair.
Detects and fixes environment issues like missing dependencies or broken paths.

## Classes (1)

### `InfrastructureRepairAgent`

**Inherits from**: BaseAgent

Monitors and repairs the agent's execution environment.

**Methods** (4):
- `__init__(self, path)`
- `audit_environment(self)`
- `repair_issue(self, issue)`
- `auto_repair(self)`

## Dependencies

**Imports** (6):
- `logging`
- `pandas`
- `src.classes.base_agent.BaseAgent`
- `subprocess`
- `sys`
- `yaml`

---
*Auto-generated documentation*
