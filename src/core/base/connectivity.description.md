# connectivity

**File**: `src\core\base\connectivity.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 8 imports  
**Lines**: 102  
**Complexity**: 5 (moderate)

## Overview

Modern connectivity module providing high-performance binary transport.
Supports MessagePack for serialization and Zstd for compression (Phase 255).

## Classes (2)

### `BinaryTransport`

Handles binary serialization and compression for agent communication.
Utilizes MessagePack and Zstd for optimal performance.

**Methods** (2):
- `pack(data, compress, level)`
- `unpack(payload, compressed)`

### `HeartbeatSignal`

Specialized structure for high-frequency heartbeat signals.
Optimized for BinaryTransport.

**Methods** (3):
- `__init__(self, agent_id, status, load)`
- `to_dict(self)`
- `from_dict(cls, data)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `logging`
- `msgpack`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Optional`
- `typing.Union`
- `zstd`

---
*Auto-generated documentation*
