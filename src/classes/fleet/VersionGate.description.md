# VersionGate

**File**: `src\classes\fleet\VersionGate.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 55  
**Complexity**: 2 (simple)

## Overview

Unified Version Gatekeeper for PyAgent Fleet.
Handles semantic versioning checks and capability validation.

## Classes (1)

### `VersionGate`

Pure logic for version compatibility checks.
Designed for future Rust porting (Core/Shell pattern).

**Methods** (2):
- `is_compatible(current, required)`
- `filter_by_capability(available, required)`

## Dependencies

**Imports** (3):
- `logging`
- `typing.List`
- `typing.Tuple`

---
*Auto-generated documentation*
