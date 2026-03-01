# AgentAPIServer

**File**: `src\classes\api\AgentAPIServer.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 15 imports  
**Lines**: 131  
**Complexity**: 2 (simple)

## Overview

FastAPI-based API gateway for the PyAgent fleet.

## Classes (2)

### `TaskRequest`

**Inherits from**: BaseModel

Class TaskRequest implementation.

### `TelemetryManger`

Class TelemetryManger implementation.

**Methods** (2):
- `__init__(self)`
- `disconnect(self, websocket)`

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `fastapi.FastAPI`
- `fastapi.WebSocket`
- `fastapi.WebSocketDisconnect`
- `json`
- `pydantic.BaseModel`
- `src.core.base.version.VERSION`
- `src.infrastructure.api.FleetLoadBalancer.FleetLoadBalancer`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `uvicorn`

---
*Auto-generated documentation*
