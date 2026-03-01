# stream_manager_mixin

**File**: `src\core\base\mixins\stream_manager_mixin.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 17 imports  
**Lines**: 320  
**Complexity**: 5 (moderate)

## Overview

Stream Management Mixin for BaseAgent.
Provides Redis-backed streaming capabilities with resumability, adapted from Adorable patterns.

## Classes (3)

### `StreamState`

Represents the current state of a stream.

**Methods** (2):
- `to_dict(self)`
- `from_dict(cls, data)`

### `StreamInfo`

Information about an active stream.

**Methods** (2):
- `to_dict(self)`
- `from_dict(cls, data)`

### `StreamManagerMixin`

Mixin providing Redis-backed stream management capabilities.
Adapted from Adorable's stream-manager.ts patterns for Python/asyncio.

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `asyncio`
- `contextlib.asynccontextmanager`
- `dataclasses.dataclass`
- `dataclasses.field`
- `json`
- `logging`
- `redis.asyncio`
- `src.core.base.common.models.communication_models.CascadeContext`
- `time`
- `typing.Any`
- `typing.AsyncGenerator`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- ... and 2 more

---
*Auto-generated documentation*
