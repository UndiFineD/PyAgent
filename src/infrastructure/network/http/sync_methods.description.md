# sync_methods

**File**: `src\infrastructure\network\http\sync_methods.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 121  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for sync_methods.

## Classes (1)

### `SyncHTTPMixin`

Mixin providing synchronous HTTP methods.

**Methods** (6):
- `get_response(self, url)`
- `get_bytes(self, url)`
- `get_text(self, url)`
- `get_json(self, url)`
- `post_json(self, url, data)`
- `download_file(self, url, save_path)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `pathlib.Path`
- `src.infrastructure.network.http.connection.HTTPConnection`
- `typing.Any`
- `typing.Callable`
- `typing.Mapping`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
