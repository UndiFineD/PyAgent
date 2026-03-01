# TeleportationEngine

**File**: `src\infrastructure\voyager\TeleportationEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 70  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for TeleportationEngine.

## Classes (1)

### `TeleportationEngine`

Handles the serialization and deserialization of agent states for 
cross-machine 'teleportation'.

**Methods** (4):
- `capture_agent_state(agent)`
- `restore_agent_state(blob)`
- `encode_for_transport(blob)`
- `decode_from_transport(encoded)`

## Dependencies

**Imports** (8):
- `base64`
- `msgpack`
- `src.core.base.Version.VERSION`
- `src.observability.StructuredLogger.StructuredLogger`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- `zlib`

---
*Auto-generated documentation*
