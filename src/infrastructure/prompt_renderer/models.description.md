# models

**File**: `src\infrastructure\prompt_renderer\models.py`  
**Type**: Python Module  
**Summary**: 8 classes, 0 functions, 11 imports  
**Lines**: 124  
**Complexity**: 4 (simple)

## Overview

Models for Prompt Rendering.

## Classes (8)

### `TruncationStrategy`

**Inherits from**: Enum

Prompt truncation strategies.

### `InputType`

**Inherits from**: Enum

Input types for prompt rendering.

### `RenderMode`

**Inherits from**: Enum

Rendering modes.

### `PromptConfig`

Configuration for prompt rendering.

**Methods** (1):
- `to_dict(self)`

### `TruncationResult`

Result of prompt truncation.

**Methods** (1):
- `truncation_ratio(self)`

### `RenderResult`

Result of prompt rendering.

**Methods** (1):
- `is_multimodal(self)`

### `EmbeddingInput`

Embedding input for direct embedding injection.

### `MultimodalInput`

Multimodal input container.

**Methods** (1):
- `is_empty(self)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`
- `typing.Union`

---
*Auto-generated documentation*
