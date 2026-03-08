# MetacognitiveMonitor

**File**: `src\classes\cognitive\MetacognitiveMonitor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 72  
**Complexity**: 4 (simple)

## Overview

Shell for MetacognitiveMonitor, handling logging and alerting.

## Classes (1)

### `MetacognitiveMonitor`

Evaluates the internal consistency and certainty of agent reasoning.

Acts as the I/O Shell for MetacognitiveCore.

**Methods** (4):
- `__init__(self)`
- `calibrate_agent(self, agent_name, reported_conf, actual_correct)`
- `evaluate_reasoning(self, agent_name, task, reasoning_chain)`
- `get_summary(self)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `logging`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.core.MetacognitiveCore.MetacognitiveCore`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
