# InterleavingOrchestrator

**File**: `src\classes\orchestration\InterleavingOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 102  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for InterleavingOrchestrator.

## Classes (1)

### `InterleavingOrchestrator`

Advanced orchestrator that implements 'Neural Interleaving' - 
switching between different reasoning models or agent tiers based on task complexity.

**Methods** (5):
- `__init__(self, fleet)`
- `execute_interleaved_task(self, task)`
- `_assess_complexity(self, task)`
- `_select_strategy(self, score)`
- `record_tier_performance(self, task_id, tier, latency, success)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `json`
- `logging`
- `src.classes.fleet.FleetManager.FleetManager`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
