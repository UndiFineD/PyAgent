# StreamAgent

**File**: `src\logic\agents\specialists\StreamAgent.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 18 imports  
**Lines**: 354  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for StreamAgent.

## Classes (4)

### `WebhookStatus`

**Inherits from**: Enum

Class WebhookStatus implementation.

### `WebhookConfig`

Configuration for a webhook endpoint.

### `StreamEvent`

Represents an event in the data stream.

### `StreamAgent`

**Inherits from**: BaseAgent

Agent specializing in streaming data injection and extraction.
Interfaces with n8n, Zapier, Make, and other webhook-based automation platforms.

**Methods** (6):
- `__init__(self, file_path)`
- `_validate_schema(self, data, schema)`
- `_get_nested_value(self, data, path)`
- `_extract_json(self, raw)`
- `_extract_csv(self, raw)`
- `_extract_xml(self, raw)`

## Dependencies

**Imports** (18):
- `__future__.annotations`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `json`
- `logging`
- `re`
- `requests`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.BaseUtilities.as_tool`
- `src.core.base.Version.VERSION`
- `time`
- `typing.Any`
- `typing.Callable`
- ... and 3 more

---
*Auto-generated documentation*
