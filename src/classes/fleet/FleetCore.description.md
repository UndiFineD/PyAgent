# FleetCore

**File**: `src\classes\fleet\FleetCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 74  
**Complexity**: 4 (simple)

## Overview

FleetCore logic for high-level fleet management.
Contains pure logic for tool scoring, capability mapping, and state transition validation.

## Classes (1)

### `FleetCore`

Pure logic core for the FleetManager.

**Methods** (4):
- `__init__(self, default_score_threshold)`
- `cached_logic_match(self, goal, tool_name, tool_owner)`
- `score_tool_candidates(self, goal, tools_metadata, provided_kwargs)`
- `validate_state_transition(self, current_state, next_state)`

## Dependencies

**Imports** (6):
- `functools.lru_cache`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
