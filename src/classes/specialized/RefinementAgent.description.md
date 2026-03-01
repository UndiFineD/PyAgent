# RefinementAgent

**File**: `src\classes\specialized\RefinementAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 81  
**Complexity**: 5 (moderate)

## Overview

Agent specializing in Recursive Self-Refinement.
Optimizes system prompts, tool descriptions, and agent logic based on performance telemetry.

## Classes (1)

### `RefinementAgent`

**Inherits from**: BaseAgent

Refines the swarm's core logic and instructions through performance feedback.

**Methods** (5):
- `__init__(self, file_path)`
- `analyze_performance_gaps(self, failure_logs)`
- `propose_prompt_update(self, agent_class_name, performance_feedback)`
- `update_agent_source(self, file_path, new_logic_snippet)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (11):
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `src.classes.base_agent.utilities.create_main_function`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
