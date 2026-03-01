# api

**File**: `src\infrastructure\compute\backend\llm_backends\lmstudio\api.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 201  
**Complexity**: 6 (moderate)

## Overview

LM Studio REST API client with HTTP fallback support.

## Classes (1)

### `LMStudioAPIClient`

HTTP REST API client for LM Studio with retry and error handling.

**Methods** (6):
- `__init__(self, base_url, api_token, default_model)`
- `_normalize_url(self, endpoint)`
- `_get_headers(self)`
- `_http_request_with_retry(self, method, url, max_retries)`
- `list_models(self)`
- `get_info(self)`

## Dependencies

**Imports** (6):
- `httpx`
- `logging`
- `os`
- `time`
- `typing.Any`
- `typing.Optional`

---
*Auto-generated documentation*
