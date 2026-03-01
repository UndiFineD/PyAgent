# TransportLayer

**File**: `src\infrastructure\voyager\TransportLayer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 100  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for TransportLayer.

## Classes (1)

### `VoyagerTransport`

VoyagerTransport: High-performance P2P message bus using ZeroMQ.
Uses DEALER/ROUTER pattern for asynchronous bi-directional communication.

**Methods** (2):
- `__init__(self, host, port)`
- `stop(self)`

## Dependencies

**Imports** (12):
- `asyncio`
- `logging`
- `msgpack`
- `src.observability.StructuredLogger.StructuredLogger`
- `typing.Any`
- `typing.Awaitable`
- `typing.Callable`
- `typing.Dict`
- `typing.Optional`
- `zmq`
- `zmq.asyncio`

---
*Auto-generated documentation*
