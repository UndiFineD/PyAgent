# NotificationManager

**File**: `src\core\base\common\utils\NotificationManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 103  
**Complexity**: 10 (moderate)

## Overview

Python module containing implementation for NotificationManager.

## Classes (1)

### `NotificationManager`

Manages event notifications via webhooks and internal callbacks.

**Methods** (10):
- `__init__(self, workspace_root)`
- `_load_status(self)`
- `_save_status(self)`
- `_is_webhook_working(self, url)`
- `_update_status(self, url, working)`
- `register_webhook(self, url)`
- `register_callback(self, callback)`
- `notify(self, event_name, event_data)`
- `_execute_callbacks(self, event_name, event_data)`
- `_send_webhooks(self, event_name, event_data)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `requests`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
