# NotificationManager

**File**: `src\observability\improvements\NotificationManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 50  
**Complexity**: 5 (moderate)

## Overview

Auto-extracted class from agent_improvements.py

## Classes (1)

### `NotificationManager`

Notifies subscribers about improvement changes.

**Methods** (5):
- `__init__(self)`
- `subscribe(self, improvement_id, subscriber)`
- `get_subscribers(self, improvement_id)`
- `on_notification(self, callback)`
- `notify_status_change(self, improvement_id, old_status, new_status)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `collections.abc.Callable`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
