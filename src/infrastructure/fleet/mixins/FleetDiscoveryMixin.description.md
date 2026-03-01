# FleetDiscoveryMixin

**File**: `src\infrastructure\fleet\mixins\FleetDiscoveryMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 81  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for FleetDiscoveryMixin.

## Classes (1)

### `FleetDiscoveryMixin`

Mixin for FleetManager to support LAN-based peer discovery and synchronization.

**Methods** (4):
- `init_discovery(self, agent_id, service_port)`
- `get_lan_peers(self)`
- `get_peer_urls(self)`
- `get_fastest_peers(self, limit)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `aiohttp`
- `logging`
- `os`
- `src.infrastructure.network.LANDiscovery.LANDiscovery`
- `src.infrastructure.network.LANDiscovery.PeerInfo`
- `src.observability.StructuredLogger.StructuredLogger`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
