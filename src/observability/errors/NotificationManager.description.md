# NotificationManager

**File**: `src\observability\errors\NotificationManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 101  
**Complexity**: 7 (moderate)

## Overview

Auto-extracted class from agent_errors.py

## Classes (1)

### `NotificationManager`

Manages error notifications to various channels.

Supports Slack, Teams, Email, Webhooks, and Discord notifications
with configurable severity thresholds.

Attributes:
    configs: List of notification configurations.

**Methods** (7):
- `__init__(self)`
- `add_config(self, config)`
- `remove_config(self, channel)`
- `notify(self, error)`
- `_format_message(self, error, template)`
- `_send(self, config, message)`
- `get_configs(self)`

## Dependencies

**Imports** (7):
- `ErrorEntry.ErrorEntry`
- `NotificationChannel.NotificationChannel`
- `NotificationConfig.NotificationConfig`
- `__future__.annotations`
- `logging`
- `src.core.base.version.VERSION`
- `typing.List`

---
*Auto-generated documentation*
