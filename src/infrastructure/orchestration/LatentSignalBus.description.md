# LatentSignalBus

**File**: `src\infrastructure\orchestration\LatentSignalBus.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 91  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for LatentSignalBus.

## Classes (1)

### `LatentSignalBus`

Implements Telepathic Signal Compression (Phase 30).
Facilitates high-bandwidth inter-agent communication using compressed 'latent vectors'
(simulated as base64-encoded state payloads) instead of plain natural language.

**Methods** (4):
- `__init__(self, fleet)`
- `transmit_latent(self, channel, state_payload)`
- `receive_latent(self, channel)`
- `list_active_channels(self)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `base64`
- `datetime.datetime`
- `json`
- `logging`
- `src.core.base.version.VERSION`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
