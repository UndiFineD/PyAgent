# cort_core

**File**: `src\core\reasoning\cort_core.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 16 imports  
**Lines**: 386  
**Complexity**: 3 (simple)

## Overview

PyAgent Chain-of-Recursive-Thoughts (CoRT) Reasoning System.

Based on the Chain-of-Recursive-Thoughts framework for breakthrough
problem-solving and response quality through recursive thinking.

## Classes (4)

### `ThinkingRound`

Represents a single round of thinking.

### `CoRTResult`

Result of a CoRT reasoning process.

### `CoRTReasoningCore`

Chain-of-Recursive-Thoughts reasoning system.

Implements dynamic evaluation, adaptive thinking rounds, and
multi-path reasoning for breakthrough problem-solving.

**Methods** (2):
- `__init__(self, inference_engine)`
- `_extract_reasoning_chain(self, thinking_history)`

### `CoRTAgentMixin`

Mixin to add CoRT reasoning capabilities to agents.

Integrates CoRT reasoning into the agent workflow.

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (16):
- `__future__.annotations`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `json`
- `logging`
- `re`
- `src.core.base.models.communication_models.CascadeContext`
- `src.inference.engine.InferenceEngine`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`
- ... and 1 more

---
*Auto-generated documentation*
