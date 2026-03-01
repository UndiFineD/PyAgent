# ImmunizationOrchestrator

**File**: `src\infrastructure\orchestration\ImmunizationOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 81  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for ImmunizationOrchestrator.

## Classes (1)

### `ImmunizationOrchestrator`

Implements Swarm Immunization (Phase 32).
Collectively identifies and "immunizes" the fleet against adversarial prompt patterns.

**Methods** (4):
- `__init__(self, fleet)`
- `scan_for_threats(self, prompt)`
- `immunize(self, adversarial_example, label)`
- `get_audit_trail(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `logging`
- `re`
- `src.core.base.version.VERSION`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
