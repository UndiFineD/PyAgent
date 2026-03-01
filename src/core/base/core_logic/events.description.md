# events

**File**: `src\core\base\core_logic\events.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 32  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for events.

## Classes (1)

### `EventCore`

Class EventCore implementation.

**Methods** (4):
- `trigger_event(self, event, data, hooks)`
- `filter_events(self, events, event_type)`
- `format_history_for_prompt(self, history)`
- `build_prompt_with_history(self, prompt, history, system_prompt)`

## Dependencies

**Imports** (8):
- `logging`
- `src.core.base.models.ConversationMessage`
- `src.core.base.models.EventType`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
