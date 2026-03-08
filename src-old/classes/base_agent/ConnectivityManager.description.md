# ConnectivityManager

**File**: `src\classes\base_agent\ConnectivityManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 107  
**Complexity**: 11 (moderate)

## Overview

Centralized connectivity management with TTL-based status caching.

## Classes (1)

### `ConnectivityManager`

Manages connection status for external APIs with persistent 15-minute TTL caching.

**Methods** (11):
- `__new__(cls)`
- `__init__(self, workspace_root)`
- `_load_status(self)`
- `_save_status(self)`
- `get_preferred_endpoint(self, group)`
- `set_preferred_endpoint(self, group, endpoint_id)`
- `is_endpoint_available(self, endpoint_id)`
- `update_status(self, endpoint_id, working)`
- `is_online(self, endpoint)`
- `set_status(self, endpoint, online)`
- ... and 1 more methods

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
