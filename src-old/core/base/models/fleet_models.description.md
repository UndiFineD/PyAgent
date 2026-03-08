# fleet_models

**File**: `src\core\base\models\fleet_models.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 14 imports  
**Lines**: 84  
**Complexity**: 4 (simple)

## Overview

Models for fleet - wide state and resource management.

## Classes (5)

### `HealthCheckResult`

Result of agent health check.

### `IncrementalState`

State for incremental processing.

### `RateLimitConfig`

Configuration for rate limiting.

### `TokenBudget`

Manages token allocation.

**Methods** (4):
- `used(self)`
- `remaining(self)`
- `allocate(self, name, tokens)`
- `release(self, name)`

### `ShutdownState`

State for graceful shutdown.

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `base_models._empty_dict_str_any`
- `base_models._empty_dict_str_float`
- `base_models._empty_dict_str_int`
- `base_models._empty_dict_str_str`
- `base_models._empty_list_str`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enums.RateLimitStrategy`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
