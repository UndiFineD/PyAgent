# types

**File**: `src\infrastructure\parallel\dp\types.py`  
**Type**: Python Module  
**Summary**: 7 classes, 0 functions, 8 imports  
**Lines**: 96  
**Complexity**: 4 (simple)

## Overview

Types and configuration for data parallel coordination.

## Classes (7)

### `DPRole`

**Inherits from**: Enum

Data parallel role.

### `WorkerHealth`

**Inherits from**: Enum

Worker health status.

### `LoadBalanceStrategy`

**Inherits from**: Enum

Load balancing strategy.

### `DPConfig`

Configuration for data parallel coordinator.

### `WorkerState`

State of a DP worker.

**Methods** (1):
- `update_latency(self, latency_ms)`

### `StepState`

State for a single step.

**Methods** (2):
- `is_complete(self)`
- `duration_ms(self)`

### `WaveState`

State for an execution wave.

**Methods** (1):
- `is_complete(self)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `time`
- `typing.Any`
- `typing.Optional`

---
*Auto-generated documentation*
