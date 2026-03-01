# Class Breakdown: locality_manager

**File**: `src\infrastructure\swarm\distributed\v2\locality_manager.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LocalityGroup`

**Line**: 27  
**Methods**: 1

Represents a set of ranks within the same network topology segment.

[TIP] **Suggested split**: Move to `localitygroup.py`

---

### 2. `LocalityManager`

**Line**: 36  
**Methods**: 5

Groups ranks by physical/logical proximity (Rack, Region, or Subnet).
Used to optimize data parallelism and KV-cache offloading across nodes.

[TIP] **Suggested split**: Move to `localitymanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
