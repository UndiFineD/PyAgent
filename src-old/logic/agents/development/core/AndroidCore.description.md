# AndroidCore

**File**: `src\logic\agents\development\core\AndroidCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 66  
**Complexity**: 3 (simple)

## Overview

Core logic for Android ADB integration (Phase 175).
Encapsulates ADB commands for UI testing.

## Classes (1)

### `AndroidCore`

Class AndroidCore implementation.

**Methods** (3):
- `run_adb_command(command, serial, recorder)`
- `list_devices(recorder)`
- `take_screenshot(output_path, serial, recorder)`

## Dependencies

**Imports** (4):
- `src.core.base.interfaces.ContextRecorderInterface`
- `subprocess`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
