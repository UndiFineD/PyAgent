# connection

**File**: `src\infrastructure\network\http\connection.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 95  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for connection.

## Classes (1)

### `HTTPConnection`

**Inherits from**: SyncHTTPMixin, AsyncHTTPMixin

Helper class to send HTTP requests with session reuse.

**Methods** (7):
- `__init__(self)`
- `get_sync_client(self)`
- `close(self)`
- `__enter__(self)`
- `__exit__(self)`
- `_validate_http_url(self, url)`
- `_headers(self)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `aiohttp`
- `logging`
- `requests`
- `src.infrastructure.network.http.async_methods.AsyncHTTPMixin`
- `src.infrastructure.network.http.sync_methods.SyncHTTPMixin`
- `typing.Any`
- `typing.Mapping`
- `typing.MutableMapping`
- `urllib.parse.urlparse`

---
*Auto-generated documentation*
