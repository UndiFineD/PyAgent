# NotificationManager

**File**: `src\classes\agent\NotificationManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 105  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for NotificationManager.

## Classes (1)

### `NotificationManager`

Manages event notifications via webhooks and internal callbacks.

**Methods** (8):
- `__init__(self, workspace_root, recorder)`
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
- `collections.abc.Callable`
- `logging`
- `requests`
- `src.core.base.ConnectivityManager.ConnectivityManager`
- `src.core.base.utils.NotificationCore.NotificationCore`
- `src.core.base.version.VERSION`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
