# manager

**File**: `src\infrastructure\conversation\context\manager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 4 functions, 15 imports  
**Lines**: 179  
**Complexity**: 10 (moderate)

## Overview

Context manager for coordinating multiple conversation contexts.

## Classes (1)

### `ContextManager`

Registry and lifecycle manager for conversation contexts.

**Methods** (6):
- `__init__(self, default_config)`
- `active_contexts_count(self)`
- `create_context(self, context_id, config, context_class)`
- `get_context(self, context_id)`
- `remove_context(self, context_id)`
- `list_contexts(self, state)`

## Functions (4)

### `get_context_manager()`

Get or create singleton instance.

### `create_context(context_id, config, context_class)`

Convenience function to create a context using the global manager.

### `merge_contexts(primary, secondary, deduplicate)`

Merge turns from secondary into primary context.

### `restore_context(snapshot)`

Restore context from a snapshot.

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `asyncio`
- `core.AgenticContext`
- `core.ConversationContext`
- `logging`
- `models.ContextConfig`
- `models.ContextSnapshot`
- `models.ContextState`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Type`
- `typing.TypeVar`

---
*Auto-generated documentation*
