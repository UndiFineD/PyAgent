# Class Breakdown: discovery_orchestrator

**File**: `src\infrastructure\swarm\orchestration\swarm\discovery_orchestrator.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `DiscoveryOrchestrator`

**Line**: 40  
**Methods**: 6

Handles peer-to-peer discovery of fleet nodes using mDNS/Zeroconf.

[TIP] **Suggested split**: Move to `discoveryorchestrator.py`

---

### 2. `FleetServiceListener`

**Line**: 148  
**Inherits**: ServiceListener  
**Methods**: 4

Listens for other PyAgent fleet nodes and registers them.

[TIP] **Suggested split**: Move to `fleetservicelistener.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
