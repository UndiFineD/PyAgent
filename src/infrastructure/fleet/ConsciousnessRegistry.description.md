# ConsciousnessRegistry

**File**: `src\infrastructure\fleet\ConsciousnessRegistry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 90  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for ConsciousnessRegistry.

## Classes (1)

### `ConsciousnessRegistry`

Phase 240: Fleet Consciousness Registry.
Indexes and summarizes the 'Thought Streams' of all agents for global awareness.
Allows any agent to 'know' what the rest of the fleet is doing.

**Methods** (6):
- `__new__(cls)`
- `__init__(self, fleet)`
- `_on_thought(self, event)`
- `get_agent_awareness(self, agent_name)`
- `get_global_awareness(self)`
- `summarize_fleet_state(self)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `datetime.datetime`
- `logging`
- `src.infrastructure.orchestration.SignalRegistry.SignalRegistry`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
