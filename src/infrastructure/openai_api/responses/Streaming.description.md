# Streaming

**File**: `src\infrastructure\openai_api\responses\Streaming.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 14 imports  
**Lines**: 87  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for Streaming.

## Classes (3)

### `SSEEvent`

Server-Sent Event.

**Methods** (1):
- `encode(self)`

### `SSEStream`

SSE streaming handler.

**Methods** (1):
- `__init__(self, response_id)`

### `StreamingHandler`

Handles streaming response generation.

**Methods** (1):
- `__init__(self, response, stream)`

## Dependencies

**Imports** (14):
- `Enums.ResponseStatus`
- `Enums.ResponseType`
- `Models.Response`
- `Models.ResponseOutput`
- `Models.ResponseUsage`
- `Models.TextContent`
- `asyncio`
- `dataclasses.dataclass`
- `json`
- `typing.Any`
- `typing.AsyncIterator`
- `typing.List`
- `typing.Optional`
- `uuid`

---
*Auto-generated documentation*
