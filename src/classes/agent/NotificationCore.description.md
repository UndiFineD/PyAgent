# NotificationCore

**File**: `src\classes\agent\NotificationCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 39  
**Complexity**: 3 (simple)

## Overview

NotificationCore logic for PyAgent.
Pure logic for payload formatting and domain extraction.
No I/O or side effects.

## Classes (1)

### `NotificationCore`

Pure logic core for notification management.

**Methods** (3):
- `construct_payload(event_name, event_data)`
- `get_domain_from_url(url)`
- `validate_event_data(data)`

## Dependencies

**Imports** (5):
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- `urllib.parse`

---
*Auto-generated documentation*
