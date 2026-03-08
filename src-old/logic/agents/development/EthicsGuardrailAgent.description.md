# EthicsGuardrailAgent

**File**: `src\logic\agents\development\EthicsGuardrailAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 97  
**Complexity**: 5 (moderate)

## Overview

Ethics Guardrail Agent for PyAgent.
Reviews task requests and agent actions against constitutional AI principles.

## Classes (1)

### `EthicsGuardrailAgent`

**Inherits from**: BaseAgent

Reviews requests for ethical compliance and safety. 
Version 2: Real-time swarm monitoring and safety protocol enforcement.

**Methods** (5):
- `__init__(self, path)`
- `monitor_swarm_decision(self, decision)`
- `enforce_protocol(self, action_context)`
- `review_task(self, task)`
- `review_action(self, agent_name, action, result)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `logging`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
