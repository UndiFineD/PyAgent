# PersistenceMixin

**File**: `src\core\base\mixins\PersistenceMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 112  
**Complexity**: 11 (moderate)

## Overview

Python module containing implementation for PersistenceMixin.

## Classes (1)

### `PersistenceMixin`

Handles agent state, history, scratchpad, metrics, and file persistence.

**Methods** (11):
- `__init__(self)`
- `state(self)`
- `register_webhook(self, url)`
- `_trigger_event(self, event_type, data)`
- `generate_diff(self)`
- `get_diff(self)`
- `read_previous_content(self)`
- `update_file(self)`
- `_write_dry_run_diff(self)`
- `save_state(self)`
- ... and 1 more methods

## Dependencies

**Imports** (9):
- `logging`
- `pathlib.Path`
- `src.core.base.AgentHistory.AgentConversationHistory`
- `src.core.base.AgentScratchpad.AgentScratchpad`
- `src.core.base.models.AgentState`
- `src.core.base.models.EventType`
- `typing.Any`
- `typing.List`

---
*Auto-generated documentation*
