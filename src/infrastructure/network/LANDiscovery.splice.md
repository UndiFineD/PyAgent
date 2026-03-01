# Class Breakdown: LANDiscovery

**File**: `src\infrastructure\network\LANDiscovery.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PeerInfo`

**Line**: 19  
**Methods**: 1

[TIP] **Suggested split**: Move to `peerinfo.py`

---

### 2. `LANDiscovery`

**Line**: 31  
**Methods**: 14

Decentralized LAN Discovery for PyAgents.
Follows an Announce -> Respond -> Register -> Sync cycle.

[TIP] **Suggested split**: Move to `landiscovery.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
