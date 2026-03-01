# LANDiscovery

**File**: `src\infrastructure\network\LANDiscovery.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 15 imports  
**Lines**: 262  
**Complexity**: 15 (moderate)

## Overview

Python module containing implementation for LANDiscovery.

## Classes (2)

### `PeerInfo`

Class PeerInfo implementation.

**Methods** (1):
- `to_dict(self)`

### `LANDiscovery`

Decentralized LAN Discovery for PyAgents.
Follows an Announce -> Respond -> Register -> Sync cycle.

**Methods** (14):
- `__init__(self, agent_id, service_port, secret_key, metadata)`
- `local_ip(self)`
- `_sign(self, data)`
- `_verify(self, data, signature)`
- `_create_message(self, msg_type, extra)`
- `start(self)`
- `stop(self)`
- `_announce_loop(self)`
- `_sync_registry(self, sock)`
- `_listen_loop(self)`
- ... and 4 more methods

## Dependencies

**Imports** (15):
- `dataclasses.asdict`
- `dataclasses.dataclass`
- `hashlib`
- `hmac`
- `json`
- `logging`
- `socket`
- `src.infrastructure.network.NetworkUtils.get_ip`
- `src.observability.StructuredLogger.StructuredLogger`
- `threading`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
