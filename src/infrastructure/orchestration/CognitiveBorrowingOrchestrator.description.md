# CognitiveBorrowingOrchestrator

**File**: `src\infrastructure\orchestration\CognitiveBorrowingOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 59  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for CognitiveBorrowingOrchestrator.

## Classes (1)

### `CognitiveBorrowingOrchestrator`

Enables agents to 'borrow' high-level cognitive patterns or skills from peers in real-time.
When an agent encounters a task outside its direct specialization, it can request
a 'Cognitive Bridge' to a more specialized peer.

**Methods** (4):
- `__init__(self, fleet)`
- `establish_bridge(self, target_agent, source_agent)`
- `borrow_skill(self, agent_name, skill_description)`
- `dissolve_bridge(self, agent_name)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `logging`
- `src.core.base.version.VERSION`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
