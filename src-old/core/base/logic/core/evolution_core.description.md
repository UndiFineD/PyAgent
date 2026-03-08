# evolution_core

**File**: `src\core\base\logic\core\evolution_core.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 7 imports  
**Lines**: 89  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for evolution_core.

## Classes (2)

### `AgentMetadata`

Class AgentMetadata implementation.

### `EvolutionCore`

Manages the lifecycle and evolution of agents based on task performance.
Harvested from self-evolving-subagent patterns.

**Methods** (4):
- `__init__(self, sop_core)`
- `record_usage(self, agent_name, success)`
- `_check_promotion(self, meta)`
- `propose_integration(self, agent_a_name, agent_b_name)`

## Dependencies

**Imports** (7):
- `dataclasses.dataclass`
- `dataclasses.field`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
