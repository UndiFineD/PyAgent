# RemoteNeuralSynapse

**File**: `src\infrastructure\voyager\RemoteNeuralSynapse.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 112  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for RemoteNeuralSynapse.

## Classes (1)

### `RemoteNeuralSynapse`

Manages the 'synaptic' firing of tasks and agents to remote peers.
Implements the transport layer for Voyager Phase 1.1 using ZMQ.

**Methods** (1):
- `__init__(self, fleet_manager, transport_port, discovery_node)`

## Dependencies

**Imports** (8):
- `asyncio`
- `src.infrastructure.voyager.TeleportationEngine.TeleportationEngine`
- `src.infrastructure.voyager.TransportLayer.VoyagerTransport`
- `src.observability.StructuredLogger.StructuredLogger`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
