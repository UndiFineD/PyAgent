# MemoryCore

**File**: `src\classes\context\MemoryCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 50  
**Complexity**: 5 (moderate)

## Overview

MemoryCore logic for PyAgent.
Handles episode structuring, utility scoring, and rank-based filtering.

## Classes (1)

### `MemoryCore`

Class MemoryCore implementation.

**Methods** (5):
- `__init__(self, baseline_utility)`
- `create_episode(self, agent_name, task, outcome, success, metadata)`
- `format_for_indexing(self, episode)`
- `calculate_new_utility(self, old_score, increment)`
- `filter_relevant_memories(self, memories, min_utility)`

## Dependencies

**Imports** (5):
- `datetime.datetime`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
