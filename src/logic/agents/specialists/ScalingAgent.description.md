# ScalingAgent

**File**: `src\logic\agents\specialists\ScalingAgent.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 14 imports  
**Lines**: 291  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for ScalingAgent.

## Classes (5)

### `ProviderType`

**Inherits from**: Enum

Class ProviderType implementation.

### `ScalingStrategy`

**Inherits from**: Enum

Class ScalingStrategy implementation.

### `ProviderMetrics`

Tracks metrics for a compute provider.

### `ScalingDecision`

Represents a scaling action.

### `ScalingAgent`

**Inherits from**: BaseAgent

Agent specializing in dynamic fleet scaling, multi-provider deployment,
load balancing, and high-concurrency async operations coordination.

**Methods** (6):
- `__init__(self, file_path)`
- `total_capacity(self)`
- `total_active(self)`
- `utilization(self)`
- `_calculate_distribution(self, target, priority)`
- `_select_provider(self, strategy)`

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `logging`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.BaseUtilities.as_tool`
- `src.core.base.Version.VERSION`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
