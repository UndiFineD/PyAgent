# PoolingCore

**File**: `src\infrastructure\backend\core\PoolingCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 43  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for PoolingCore.

## Classes (1)

### `PoolingCore`

PoolingCore implements logic for HTTP/2 connection pooling and prompt compression.
It prepares requests for faster TTFT (Time to First Token).

**Methods** (4):
- `__init__(self)`
- `compress_prompt(self, text)`
- `select_best_endpoint(self, preferred_host, endpoint_stats)`
- `should_reuse_session(self, host, active_sessions)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `re`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
