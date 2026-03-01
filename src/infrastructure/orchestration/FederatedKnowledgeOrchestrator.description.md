# FederatedKnowledgeOrchestrator

**File**: `src\infrastructure\orchestration\FederatedKnowledgeOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 138  
**Complexity**: 4 (simple)

## Overview

FederatedKnowledgeOrchestrator for PyAgent.
Synchronizes learned insights ('Lessons Learned') between distributed fleet nodes.
Uses InterFleetBridgeOrchestrator to transmit knowledge without raw data leakage.

## Classes (1)

### `FederatedKnowledgeOrchestrator`

Orchestrates the synchronization of cognitive insights across distributed fleets.

**Methods** (4):
- `__init__(self, fleet_manager, fleet)`
- `broadcast_lesson(self, lesson_id, lesson_data)`
- `receive_and_fuse_knowledge(self, incoming_knowledge)`
- `run_fleet_wide_sync(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `logging`
- `src.core.base.version.VERSION`
- `src.infrastructure.orchestration.InterFleetBridgeOrchestrator.InterFleetBridgeOrchestrator`
- `src.logic.agents.cognitive.KnowledgeAgent.KnowledgeAgent`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
