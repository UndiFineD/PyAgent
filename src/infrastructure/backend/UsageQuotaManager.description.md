# UsageQuotaManager

**File**: `src\infrastructure\backend\UsageQuotaManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 103  
**Complexity**: 6 (moderate)

## Overview

Auto-extracted class from agent_backend.py

## Classes (1)

### `UsageQuotaManager`

Manages usage quotas and limits.

Tracks request counts and enforces daily / hourly limits.

Example:
    quota=UsageQuotaManager(daily_limit=1000, hourly_limit=100)
    if quota.can_request():
        quota.record_request()
        # Make request

**Methods** (6):
- `__init__(self, daily_limit, hourly_limit)`
- `_check_reset(self)`
- `can_request(self)`
- `record_request(self)`
- `get_remaining(self)`
- `get_usage_report(self)`

## Dependencies

**Imports** (8):
- `UsageQuota.UsageQuota`
- `__future__.annotations`
- `src.core.base.version.VERSION`
- `threading`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Tuple`

---
*Auto-generated documentation*
