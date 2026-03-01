# models

**File**: `src\infrastructure\conversation\context\models.py`  
**Type**: Python Module  
**Summary**: 8 classes, 0 functions, 9 imports  
**Lines**: 223  
**Complexity**: 11 (moderate)

## Overview

Conversation context models and enums.

## Classes (8)

### `ContextState`

**Inherits from**: Enum

Conversation context state.

### `TurnType`

**Inherits from**: Enum

Conversation turn type.

### `ToolExecutionPolicy`

**Inherits from**: Enum

Tool execution policy.

### `TokenMetrics`

Token usage metrics.

**Methods** (4):
- `total_tokens(self)`
- `effective_input_tokens(self)`
- `add(self, other)`
- `to_dict(self)`

### `ConversationTurn`

Single conversation turn.

**Methods** (2):
- `to_message(self)`
- `to_dict(self)`

### `ToolExecution`

Tool execution record.

**Methods** (2):
- `duration_ms(self)`
- `is_complete(self)`

### `ContextConfig`

Context configuration.

**Methods** (1):
- `to_dict(self)`

### `ContextSnapshot`

Snapshot of context state.

**Methods** (2):
- `to_dict(self)`
- `from_dict(cls, data)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
