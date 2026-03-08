# IntentCoherenceEngine

**File**: `src\classes\orchestration\IntentCoherenceEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 69  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for IntentCoherenceEngine.

## Classes (1)

### `IntentCoherenceEngine`

Implements Swarm Consciousness (Phase 30).
Maintains a unified 'Intent' layer that synchronizes all agent goals
without necessitating explicit task decomposition.

**Methods** (4):
- `__init__(self, fleet)`
- `broadcast_intent(self, intent, priority)`
- `align_agent(self, agent_name, local_task)`
- `get_current_intent(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `datetime.datetime`
- `logging`
- `src.classes.fleet.FleetManager.FleetManager`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
