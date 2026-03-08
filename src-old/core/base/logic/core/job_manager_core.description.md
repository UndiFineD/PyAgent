# job_manager_core

**File**: `src\core\base\logic\core\job_manager_core.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 8 imports  
**Lines**: 62  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for job_manager_core.

## Classes (3)

### `JobStatus`

**Inherits from**: Enum

Class JobStatus implementation.

### `AgentJob`

Class AgentJob implementation.

### `JobManagerCore`

Manages the lifecycle of persistent agent jobs (sessions).
Harvested from LiveKit Agents patterns.

**Methods** (2):
- `__init__(self)`
- `get_job(self, job_id)`

## Dependencies

**Imports** (8):
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- `uuid`

---
*Auto-generated documentation*
