# Models

**File**: `src\infrastructure\openai_api\responses\Models.py`  
**Type**: Python Module  
**Summary**: 12 classes, 0 functions, 17 imports  
**Lines**: 243  
**Complexity**: 16 (moderate)

## Overview

Python module containing implementation for Models.

## Classes (12)

### `ContentPart`

**Inherits from**: ABC

Base class for content parts.

### `TextContent`

**Inherits from**: ContentPart

Text content part.

**Methods** (1):
- `to_dict(self)`

### `ImageContent`

**Inherits from**: ContentPart

Image content part.

**Methods** (1):
- `to_dict(self)`

### `AudioContent`

**Inherits from**: ContentPart

Audio content part.

**Methods** (1):
- `to_dict(self)`

### `RefusalContent`

**Inherits from**: ContentPart

Refusal content part.

**Methods** (1):
- `to_dict(self)`

### `ToolCallContent`

**Inherits from**: ContentPart

Tool call content part.

**Methods** (1):
- `to_dict(self)`

### `Message`

Chat message.

**Methods** (2):
- `to_dict(self)`
- `from_dict(cls, data)`

### `ToolDefinition`

Tool definition for function calling.

**Methods** (1):
- `to_dict(self)`

### `ResponseConfig`

Response configuration.

**Methods** (1):
- `to_dict(self)`

### `ResponseUsage`

Token usage statistics.

**Methods** (1):
- `to_dict(self)`

### `ResponseOutput`

Single response output.

**Methods** (2):
- `to_dict(self)`
- `text(self)`

### `Response`

Complete response object.

**Methods** (4):
- `to_dict(self)`
- `add_text_output(self, text)`
- `complete(self, usage)`
- `fail(self, error_message, error_code)`

## Dependencies

**Imports** (17):
- `Enums.ContentPartType`
- `Enums.ResponseStatus`
- `Enums.ResponseType`
- `Enums.RoleType`
- `Enums.ToolType`
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `dataclasses.dataclass`
- `dataclasses.field`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- ... and 2 more

---
*Auto-generated documentation*
