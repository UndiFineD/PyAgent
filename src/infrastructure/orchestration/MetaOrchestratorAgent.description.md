# MetaOrchestratorAgent

**File**: `src\infrastructure\orchestration\MetaOrchestratorAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 112  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for MetaOrchestratorAgent.

## Classes (1)

### `MetaOrchestratorAgent`

**Inherits from**: BaseAgent

Expert orchestrator that can decompose high-level objectives into 
multi-agent workflows and manage recursive resolution.

**Methods** (2):
- `__init__(self, fleet, global_context)`
- `_enrich_args(self, args)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `json`
- `logging`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.knowledge.GlobalContext.GlobalContext`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
