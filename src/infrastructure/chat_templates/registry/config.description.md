# config

**File**: `src\infrastructure\chat_templates\registry\config.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 7 imports  
**Lines**: 209  
**Complexity**: 3 (simple)

## Overview

Configuration and built-in templates for chat template management.

## Classes (5)

### `TemplateType`

**Inherits from**: Enum

Chat template types.

### `ModelType`

**Inherits from**: Enum

Model types for template resolution.

### `TemplateConfig`

Chat template configuration.

**Methods** (1):
- `to_dict(self)`

### `TemplateInfo`

Template metadata.

**Methods** (1):
- `to_dict(self)`

### `RenderOptions`

Template rendering options.

**Methods** (1):
- `to_dict(self)`

## Dependencies

**Imports** (7):
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
