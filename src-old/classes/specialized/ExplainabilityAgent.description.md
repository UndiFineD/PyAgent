# ExplainabilityAgent

**File**: `src\classes\specialized\ExplainabilityAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 113  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for ExplainabilityAgent.

## Classes (1)

### `ExplainabilityAgent`

**Inherits from**: BaseAgent

Explainability Agent: Provides autonomous tracing and justification of multi-agent 
reasoning chains. Enhanced with SAE (Sparse Autoencoder) neural interpretability.

**Methods** (5):
- `__init__(self, workspace_path, errors_only)`
- `generate_neural_trace(self, agent_name, decision_context)`
- `log_reasoning_step(self, workflow_id, agent_name, action, justification, context)`
- `get_explanation(self, workflow_id)`
- `justify_action(self, agent_name, action, result)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `json`
- `os`
- `random`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.core.InterpretableCore.InterpretableCore`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
