# retry_logic

**File**: `src\infrastructure\network\http\retry_logic.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 85  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for retry_logic.

## Classes (1)

### `RetryHTTPMixin`

Mixin providing retry logic for HTTP requests.

**Methods** (1):
- `get_json_with_retry(self, url)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `aiohttp`
- `asyncio`
- `logging`
- `requests`
- `src.infrastructure.network.http.connection.HTTPConnection`
- `time`
- `typing.Any`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
