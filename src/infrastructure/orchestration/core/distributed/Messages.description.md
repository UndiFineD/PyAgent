# Messages

**File**: `src\infrastructure\orchestration\core\distributed\Messages.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 8 imports  
**Lines**: 63  
**Complexity**: 0 (simple)

## Overview

Message types for coordinator-worker communication.

## Classes (5)

### `CoordinatorMessage`

Base message type for coordinator communication.

### `RequestMessage`

**Inherits from**: CoordinatorMessage

Request message sent to workers.

### `ResponseMessage`

**Inherits from**: CoordinatorMessage

Response message from workers.

### `ControlMessage`

**Inherits from**: CoordinatorMessage

Control message for worker management.

### `MetricsMessage`

**Inherits from**: CoordinatorMessage

Metrics message from workers.

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- `uuid`

---
*Auto-generated documentation*
