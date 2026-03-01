# swarm_orchestrator_core

**File**: `src\core\base\logic\core\swarm_orchestrator_core.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 9 imports  
**Lines**: 98  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for swarm_orchestrator_core.

## Classes (3)

### `DelegationMode`

**Inherits from**: str, Enum

Class DelegationMode implementation.

### `SwarmMember`

Class SwarmMember implementation.

### `SwarmOrchestratorCore`

Handles higher-level multi-agent orchestration logic.
Patterns harvested from Agno (Team) and AgentUniverse (WorkPatterns).

**Methods** (4):
- `__init__(self, swarm_id)`
- `register_member(self, member)`
- `_find_best_agent(self, requirements)`
- `get_swarm_status(self)`

## Dependencies

**Imports** (9):
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Literal`
- `typing.Optional`

---
*Auto-generated documentation*
