# ConsensusOrchestrator

**File**: `src\infrastructure\orchestration\ConsensusOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 137  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for ConsensusOrchestrator.

## Classes (1)

### `ConsensusOrchestrator`

Advanced orchestrator for resolving conflicts between agents using weighted voting
and a multi-turn debate system.

**Methods** (7):
- `__init__(self, fleet)`
- `resolve_conflict(self, task, agents)`
- `verify_state_block(self, task, decision)`
- `_collect_proposals(self, task, agents)`
- `_conduct_debate(self, task, proposals, rounds)`
- `_weighted_vote(self, proposals)`
- `update_reputation(self, agent_name, feedback_score)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `hashlib`
- `logging`
- `src.core.base.version.VERSION`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
