# SelfHealingCore

**File**: `src\infrastructure\orchestration\SelfHealingCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 6 imports  
**Lines**: 115  
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

**Imports** (6):
- `__future__.annotations`
- `dataclasses.dataclass`
- `src.core.base.version.VERSION`
- `time`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
