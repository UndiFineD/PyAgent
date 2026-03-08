# sandbox

**File**: `src\core\base\sandbox.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 66  
**Complexity**: 3 (simple)

## Overview

Phase 132: Plugin Sandbox Isolation.
Enforces process-level lockdowns for potentially unsafe plugin code.

## Classes (1)

### `SandboxManager`

Manages restricted execution environments for plugins.

**Methods** (3):
- `get_sandboxed_env(base_env)`
- `is_path_safe(target_path, workspace_root)`
- `apply_process_limits(creationflags)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `os`
- `pathlib.Path`
- `subprocess`
- `sys`

---
*Auto-generated documentation*
