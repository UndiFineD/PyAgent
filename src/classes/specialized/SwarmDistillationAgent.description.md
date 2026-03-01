# SwarmDistillationAgent

**File**: `src\classes\specialized\SwarmDistillationAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 84  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for SwarmDistillationAgent.

## Classes (1)

### `SwarmDistillationAgent`

Compresses and distills knowledge from multiple specialized agents 
into a unified "Master" context for more efficient retrieval.
Integrated with LessonCore for failure mode propagation.

**Methods** (6):
- `__init__(self, workspace_path)`
- `distill_agent_knowledge(self, agent_id, knowledge_data)`
- `register_failure_lesson(self, error, cause, fix)`
- `check_for_prior_art(self, error_msg)`
- `get_unified_context(self)`
- `prune_master_context(self, threshold)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `src.logic.agents.swarm.core.LessonCore.Lesson`
- `src.logic.agents.swarm.core.LessonCore.LessonCore`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
