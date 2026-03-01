# DiscoveryNode

**File**: `src\infrastructure\voyager\DiscoveryNode.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 18 imports  
**Lines**: 181  
**Complexity**: 9 (moderate)

## Overview

Python module containing implementation for DiscoveryNode.

## Classes (2)

### `VoyagerPeerListener`

**Inherits from**: ServiceListener

Listens for other PyAgent Voyager peers on the local network.

**Methods** (4):
- `__init__(self, callback, loop)`
- `add_service(self, zc, type_, name)`
- `update_service(self, zc, type_, name)`
- `remove_service(self, zc, type_, name)`

### `DiscoveryNode`

DiscoveryNode handles decentralized peer advertisement and lookup.
Uses mDNS (zeroconf) for Phase 1.0 of Project Voyager.

**Methods** (5):
- `__init__(self, node_name, port, transport_port)`
- `_get_local_ip(self)`
- `_peer_discovered(self, info)`
- `get_active_peers(self)`
- `resolve_synapse_address(self, peer_name)`

## Dependencies

**Imports** (18):
- `asyncio`
- `logging`
- `signal`
- `socket`
- `src.core.base.Version.VERSION`
- `src.observability.StructuredLogger.StructuredLogger`
- `sys`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `uuid`
- `zeroconf.IPVersion`
- `zeroconf.ServiceBrowser`
- ... and 3 more

---
*Auto-generated documentation*
