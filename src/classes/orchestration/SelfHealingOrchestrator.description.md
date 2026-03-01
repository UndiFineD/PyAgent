# SelfHealingOrchestrator

**File**: `src\classes\orchestration\SelfHealingOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 90  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for SelfHealingOrchestrator.

## Classes (1)

### `SelfHealingOrchestrator`

Advanced Self-Healing v3: Shell for fleet resilience logic.
Delegates thresholds and strategy to SelfHealingCore.
Uses AgentRegistry tools for re-loading failed plugins.

**Methods** (6):
- `__init__(self, fleet_manager)`
- `register_heartbeat(self, agent_name, state, latency, error)`
- `check_fleet_health(self)`
- `attempt_recovery(self, agent_name)`
- `get_recovery_status(self)`
- `review_recovery_lessons(self)`

## Dependencies

**Imports** (7):
- `SelfHealingCore.SelfHealingCore`
- `logging`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
