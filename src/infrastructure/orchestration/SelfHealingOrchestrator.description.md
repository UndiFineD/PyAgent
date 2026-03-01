# SelfHealingOrchestrator

**File**: `src\infrastructure\orchestration\SelfHealingOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 132  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for SelfHealingOrchestrator.

## Classes (1)

### `SelfHealingOrchestrator`

Advanced Self-Healing v3: Shell for fleet resilience logic.
Delegates thresholds and strategy to SelfHealingCore.
Uses AgentRegistry tools for re-loading failed plugins.

**Methods** (8):
- `__init__(self, fleet_manager)`
- `health_registry(self)`
- `register_heartbeat(self, agent_name, state, latency, error)`
- `check_fleet_health(self)`
- `attempt_recovery(self, agent_name)`
- `attempt_repair(self, agent_name, error)`
- `get_recovery_status(self)`
- `review_recovery_lessons(self)`

## Dependencies

**Imports** (9):
- `SelfHealingCore.SelfHealingCore`
- `__future__.annotations`
- `logging`
- `src.core.base.version.VERSION`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
