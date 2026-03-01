# tracker

**File**: `src\infrastructure\conversation\context\tracker.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 110  
**Complexity**: 10 (moderate)

## Overview

Conversation turn tracking logic.

## Classes (1)

### `TurnTracker`

Track conversation turns and token usage.

**Methods** (10):
- `__init__(self, config)`
- `turns(self)`
- `turn_count(self)`
- `total_tokens(self)`
- `add_turn(self, turn_type, content, tokens, parent_id, metadata)`
- `get_turn(self, turn_id)`
- `get_messages(self, include_system, include_reasoning)`
- `get_recent(self, n)`
- `clear(self)`
- `truncate(self, max_turns)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `models.ContextConfig`
- `models.ConversationTurn`
- `models.TokenMetrics`
- `models.TurnType`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `uuid`

---
*Auto-generated documentation*
