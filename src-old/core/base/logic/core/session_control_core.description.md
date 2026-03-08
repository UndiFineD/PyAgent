# session_control_core

**File**: `src\core\base\logic\core\session_control_core.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 5 imports  
**Lines**: 69  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for session_control_core.

## Classes (2)

### `SessionSignal`

**Inherits from**: Enum

Signals for agent session lifecycle control.

### `SessionControlCore`

Manages session interrupt signals and shared state flags for long-running agent tasks.
Enables orchestration layers to pause or stop agents mid-loop via filesystem or shared memory flags.
Lesson harvested from .external/agentcloud pattern.

**Methods** (6):
- `__init__(self, storage_dir)`
- `_get_signal_file(self, session_id)`
- `set_signal(self, session_id, signal)`
- `get_signal(self, session_id)`
- `check_interrupt(self, session_id)`
- `check_pause(self, session_id)`

## Dependencies

**Imports** (5):
- `enum`
- `json`
- `pathlib.Path`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
