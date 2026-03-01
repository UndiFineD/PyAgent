# AgentBus

**File**: `src\infrastructure\orchestration\AgentBus.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 152  
**Complexity**: 3 (simple)

## Overview

Phase 164: Zero-Latency Agent Communication Bus.
Uses ZeroMQ for high-performance inter-process messaging.

## Classes (1)

### `AgentCommunicationBus`

Zero-latency messaging bus for swarm orchestration.

**Methods** (3):
- `__init__(self, pub_port, sub_port)`
- `subscribe(self, topic, handler)`
- `stop(self)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `asyncio`
- `inspect`
- `logging`
- `orjson`
- `signal`
- `sys`
- `typing.Any`
- `typing.Callable`
- `zmq`
- `zmq.asyncio`

---
*Auto-generated documentation*
