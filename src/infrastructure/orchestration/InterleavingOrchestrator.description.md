# InterleavingOrchestrator

**File**: `src\infrastructure\orchestration\InterleavingOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 126  
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

**Imports** (8):
- `__future__.annotations`
- `logging`
- `src.core.base.version.VERSION`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
