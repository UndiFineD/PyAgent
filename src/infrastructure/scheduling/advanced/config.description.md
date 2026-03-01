# config

**File**: `src\infrastructure\scheduling\advanced\config.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 3 imports  
**Lines**: 49  
**Complexity**: 0 (simple)

## Overview

Configuration and enums for advanced request scheduling.

## Classes (4)

### `RequestPriority`

**Inherits from**: Enum

Priority levels for inference requests.

### `RequestState`

**Inherits from**: Enum

State of an inference request.

### `PreemptionReason`

**Inherits from**: Enum

Reason for request preemption.

### `SchedulerConfig`

Configuration for the request scheduler.

## Dependencies

**Imports** (3):
- `dataclasses.dataclass`
- `enum.Enum`
- `enum.auto`

---
*Auto-generated documentation*
