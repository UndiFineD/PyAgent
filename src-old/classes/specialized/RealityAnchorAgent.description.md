# RealityAnchorAgent

**File**: `src\classes\specialized\RealityAnchorAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 90  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for RealityAnchorAgent.

## Classes (1)

### `RealityAnchorAgent`

**Inherits from**: BaseAgent

Agent specializing in zero-hallucination execution by cross-referencing
factual claims against verified 'Reality Graphs' (compiler outputs, documentation, tests).

**Methods** (4):
- `__init__(self, file_path)`
- `check_physics_constraints(self, action, environment_state)`
- `verify_claim(self, claim, evidence_sources)`
- `anchor_context(self, context_snippet)`

## Dependencies

**Imports** (8):
- `json`
- `logging`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
