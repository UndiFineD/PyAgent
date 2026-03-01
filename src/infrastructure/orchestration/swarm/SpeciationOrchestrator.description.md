# SpeciationOrchestrator

**File**: `src\infrastructure\orchestration\swarm\SpeciationOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 74  
**Complexity**: 3 (simple)

## Overview

SpeciationOrchestrator: Categorizes and evolves agent specialized "species".
Analyzes task patterns to suggest when new specialized agent types should be created.

## Classes (1)

### `SpeciationOrchestrator`

Orchestrator for managing agent speciation and occupational evolution.
Uses task telemetry to identify gaps in agent capabilities.

**Methods** (3):
- `__init__(self, fleet)`
- `identify_niche_gap(self, unhandled_tasks)`
- `record_evolution_event(self, species_name, parent_type)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `logging`
- `src.core.base.Version.VERSION`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `typing.Dict`
- `typing.List`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
