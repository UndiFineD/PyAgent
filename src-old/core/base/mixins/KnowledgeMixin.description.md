# KnowledgeMixin

**File**: `src\core\base\mixins\KnowledgeMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 87  
**Complexity**: 12 (moderate)

## Overview

Python module containing implementation for KnowledgeMixin.

## Classes (1)

### `KnowledgeMixin`

Handles knowledge engines, memory, sharded storage, and templates.

**Methods** (12):
- `__init__(self, agent_name, workspace_root)`
- `take_note(self, content)`
- `get_notes(self)`
- `clear_notes(self)`
- `register_template(self, name, template)`
- `get_template(self, name)`
- `add_to_history(self, role, content)`
- `clear_history(self)`
- `get_history(self)`
- `_build_prompt_with_history(self, prompt)`
- ... and 2 more methods

## Dependencies

**Imports** (6):
- `pathlib.Path`
- `src.core.base.ShardedKnowledgeCore.ShardedKnowledgeCore`
- `src.core.knowledge.knowledge_engine.KnowledgeEngine`
- `src.logic.agents.cognitive.LongTermMemory.LongTermMemory`
- `src.logic.agents.cognitive.context.engines.GlobalContextEngine.GlobalContextEngine`
- `typing.Any`

---
*Auto-generated documentation*
