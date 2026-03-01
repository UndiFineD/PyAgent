# core

**File**: `src\infrastructure\conversation\context\core.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 21 imports  
**Lines**: 303  
**Complexity**: 22 (complex)

## Overview

Core conversation context classes.

## Classes (2)

### `ConversationContext`

**Inherits from**: ABC

Abstract base class for conversation context.

**Methods** (18):
- `__init__(self, context_id, config)`
- `state(self)`
- `turns(self)`
- `turn_count(self)`
- `total_tokens(self)`
- `is_active(self)`
- `add_system(self, content, tokens)`
- `add_user(self, content, tokens)`
- `add_assistant(self, content, tokens)`
- `add_tool_call(self, tool_calls, tokens)`
- ... and 8 more methods

### `AgenticContext`

**Inherits from**: ConversationContext

Context for agentic workflows with tool orchestration.

**Methods** (4):
- `__init__(self, context_id, config, tool_handler)`
- `tool_orchestrator(self)`
- `has_pending_tools(self)`
- `queue_tool_calls(self, tool_calls)`

## Dependencies

**Imports** (21):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `json`
- `models.ContextConfig`
- `models.ContextSnapshot`
- `models.ContextState`
- `models.ConversationTurn`
- `models.TokenMetrics`
- `models.ToolExecution`
- `models.TurnType`
- `orchestrator.ToolOrchestrator`
- `time`
- `tracker.TurnTracker`
- ... and 6 more

---
*Auto-generated documentation*
