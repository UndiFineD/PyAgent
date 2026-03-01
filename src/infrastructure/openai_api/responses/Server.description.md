# Server

**File**: `src\infrastructure\openai_api\responses\Server.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 99  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for Server.

## Classes (1)

### `ResponsesAPIServer`

OpenAI Responses API server implementation.

**Methods** (2):
- `__init__(self, model_handler, store, enable_store)`
- `_create_response_id(self)`

## Dependencies

**Imports** (17):
- `Enums.ResponseStatus`
- `Models.Response`
- `Models.ResponseConfig`
- `Models.ResponseUsage`
- `Store.InMemoryResponseStore`
- `Store.ResponseStore`
- `Streaming.SSEStream`
- `Streaming.StreamingHandler`
- `asyncio`
- `logging`
- `typing.AsyncIterator`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- ... and 2 more

---
*Auto-generated documentation*
