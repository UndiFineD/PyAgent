# BootstrapConfigs

**File**: `src\infrastructure\fleet\BootstrapConfigs.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 3 imports  
**Lines**: 157  
**Complexity**: 1 (simple)

## Overview

Hardcoded bootstrap configurations for essential system components.
These must remain static to ensure the system can boot up before dynamic discovery.

## Functions (1)

### `get_bootstrap_agents()`

Returns the bootstrap agents with dynamic overrides applied.

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `src.core.base.Version.VERSION`
- `src.infrastructure.fleet.RegistryOverlay.RegistryOverlay`

---
*Auto-generated documentation*
