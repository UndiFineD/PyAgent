# rtp_server_core

**File**: `src\infrastructure\transport\rtp_server_core.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 10 imports  
**Lines**: 98  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for rtp_server_core.

## Classes (2)

### `RTPSession`

Represents an active RTP session for a call.

### `RTPServerCore`

Core logic for handling bidirectional RTP audio streams.
Harvested from .external/Asterisk-AI-Voice-Agent

**Methods** (3):
- `__init__(self, host, port_range)`
- `allocate_session(self, call_id)`
- `handle_packet(self, data, addr)`

## Dependencies

**Imports** (10):
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `socket`
- `struct`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
