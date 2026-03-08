# SelfHealingCore

**File**: `src\classes\orchestration\SelfHealingCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 9 imports  
**Lines**: 97  
**Complexity**: 5 (moderate)

## Overview

SelfHealingCore logic for fleet resilience.
Contains pure logic for health threshold calculation, anomaly detection,
and recovery strategy selection.

## Classes (2)

### `HealthStatus`

Class HealthStatus implementation.

### `SelfHealingCore`

Pure logic core for the SelfHealing orchestrator.

**Methods** (5):
- `__init__(self, timeout_seconds, max_errors)`
- `update_health(self, agent_name, latency, error)`
- `detect_failures(self)`
- `get_recovery_action(self, agent_name)`
- `validate_plugin_version(self, plugin_version, required_version)`

## Dependencies

**Imports** (9):
- `dataclasses.dataclass`
- `dataclasses.field`
- `logging`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
