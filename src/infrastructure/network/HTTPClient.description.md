# HTTPClient

**File**: `src\infrastructure\network\HTTPClient.py`  
**Type**: Python Module  
**Summary**: 3 classes, 3 functions, 4 imports  
**Lines**: 100  
**Complexity**: 4 (simple)

## Overview

HTTPClient - Unified sync/async HTTP client with session reuse.

Refactored to modular package structure for Phase 317.
Decomposed into mixins for sync, async, and retry logic.

## Classes (3)

### `HTTPClient`

**Inherits from**: HTTPConnection

Alias for HTTPConnection with sync-focused interface.

### `AsyncHTTPClient`

**Inherits from**: HTTPConnection

Alias for HTTPConnection with async-focused interface.

### `RetryableHTTPClient`

**Inherits from**: HTTPConnection, RetryHTTPMixin

HTTP client with automatic retry on failures.

**Methods** (1):
- `__init__(self)`

## Functions (3)

### `get_bytes(url)`

Convenience function using global HTTP connection.

### `get_text(url)`

Convenience function using global HTTP connection.

### `get_json(url)`

Convenience function using global HTTP connection.

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `src.infrastructure.network.http.connection.HTTPConnection`
- `src.infrastructure.network.http.retry_logic.RetryHTTPMixin`
- `typing.Any`

---
*Auto-generated documentation*
