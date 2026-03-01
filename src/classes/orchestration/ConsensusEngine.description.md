# ConsensusEngine

**File**: `src\classes\orchestration\ConsensusEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 48  
**Complexity**: 3 (simple)

## Overview

Engine for Multi-agent 'Society of Mind' consensus protocols.
Agents vote on proposed solutions to ensure higher quality and redundancy.

## Classes (1)

### `ConsensusEngine`

Manages voting and agreement between multiple agents.
Shell for ConsensusCore.

**Methods** (3):
- `__init__(self, fleet_manager)`
- `request_consensus(self, task, agent_names)`
- `get_consensus_report(self)`

## Dependencies

**Imports** (6):
- `ConsensusCore.ConsensusCore`
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
