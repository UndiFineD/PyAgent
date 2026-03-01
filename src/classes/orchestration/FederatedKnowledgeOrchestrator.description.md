# FederatedKnowledgeOrchestrator

**File**: `src\classes\orchestration\FederatedKnowledgeOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 102  
**Complexity**: 4 (simple)

## Overview

FederatedKnowledgeOrchestrator for PyAgent.
Synchronizes learned insights ('Lessons Learned') between distributed fleet nodes.
Uses InterFleetBridgeOrchestrator to transmit knowledge without raw data leakage.

## Classes (1)

### `FederatedKnowledgeOrchestrator`

Orchestrates the synchronization of cognitive insights across distributed fleets.

**Methods** (4):
- `__init__(self, fleet_manager)`
- `broadcast_lesson(self, lesson_id, lesson_data)`
- `receive_and_fuse_knowledge(self, incoming_knowledge)`
- `run_fleet_wide_sync(self)`

## Dependencies

**Imports** (7):
- `logging`
- `src.classes.context.KnowledgeAgent.KnowledgeAgent`
- `src.classes.orchestration.InterFleetBridgeOrchestrator.InterFleetBridgeOrchestrator`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
