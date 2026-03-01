# ModalTeleportationOrchestrator

**File**: `src\infrastructure\orchestration\ModalTeleportationOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 67  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for ModalTeleportationOrchestrator.

## Classes (1)

### `ModalTeleportationOrchestrator`

Implements Cross-Modal Teleportation (Phase 33).
Converts task state between different modalities (e.g., GUI -> Code, Voice -> SQL).

**Methods** (3):
- `__init__(self, fleet)`
- `teleport_state(self, source_modality, target_modality, source_data)`
- `identify_optimal_target(self, source_modality, raw_data)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `logging`
- `src.core.base.version.VERSION`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `typing.Any`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
