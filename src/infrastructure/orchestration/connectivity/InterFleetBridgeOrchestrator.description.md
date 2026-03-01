# InterFleetBridgeOrchestrator

**File**: `src\infrastructure\orchestration\connectivity\InterFleetBridgeOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 109  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for InterFleetBridgeOrchestrator.

## Classes (1)

### `InterFleetBridgeOrchestrator`

InterFleetBridgeOrchestrator: Manages peer connectivity and 
cross-machine discovery for the Voyager Constellation.

**Methods** (3):
- `__init__(self, fleet_manager)`
- `get_known_peers(self)`
- `connected_fleets(self)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `asyncio`
- `logging`
- `src.core.base.Version.VERSION`
- `src.infrastructure.voyager.DiscoveryNode.DiscoveryNode`
- `src.infrastructure.voyager.RemoteNeuralSynapse.RemoteNeuralSynapse`
- `src.observability.StructuredLogger.StructuredLogger`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
