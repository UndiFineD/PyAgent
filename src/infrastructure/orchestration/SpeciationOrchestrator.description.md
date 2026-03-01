# SpeciationOrchestrator

**File**: `src\infrastructure\orchestration\SpeciationOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 64  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for SpeciationOrchestrator.

## Classes (1)

### `SpeciationOrchestrator`

Phase 39: Autonomous Sub-Fleet Speciation.
Uses the SpeciationAgent to spawn specialized 'breeds' of the fleet for specific domains.

**Methods** (4):
- `__init__(self, fleet)`
- `speciate(self, domain)`
- `evolve_specialized_agent(self, base_agent, niche)`
- `get_sub_fleet(self, domain)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `logging`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
