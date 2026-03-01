# ConversationManagers

**File**: `src\classes\base_agent\managers\ConversationManagers.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 27  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for ConversationManagers.

## Classes (1)

### `ConversationHistory`

Manages a conversation history with message storage and retrieval.

**Methods** (4):
- `__init__(self, max_messages)`
- `add(self, role, content)`
- `get_context(self)`
- `clear(self)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `models.ConversationMessage`
- `models.MessageRole`
- `typing.Any`
- `typing.List`

---
*Auto-generated documentation*
