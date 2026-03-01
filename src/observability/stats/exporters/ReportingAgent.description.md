# ReportingAgent

**File**: `src\observability\stats\exporters\ReportingAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 36 imports  
**Lines**: 161  
**Complexity**: 3 (simple)

## Overview

Agent specializing in executive summaries and progress tracking dashboards.

## Classes (1)

### `ReportingAgent`

**Inherits from**: BaseAgent

Generates the unified progress dashboard by coordinating other agents.

**Methods** (3):
- `__init__(self, file_path)`
- `generate_dashboard(self)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (36):
- `datetime.datetime`
- `json`
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.create_main_function`
- `src.classes.coder.DocumentationAgent.DocumentationAgent`
- `src.classes.coder.LintingAgent.LintingAgent`
- `src.classes.coder.QualityGateAgent.QualityGateAgent`
- `src.classes.coder.ReasoningAgent.ReasoningAgent`
- `src.classes.coder.SecurityGuardAgent.SecurityGuardAgent`
- `src.classes.coder.SelfHealingAgent.SelfHealingAgent`
- `src.classes.coder.SelfOptimizerAgent.SelfOptimizerAgent`
- `src.classes.coder.TestAgent.TestAgent`
- `src.classes.coder.TypeSafetyAgent.TypeSafetyAgent`
- ... and 21 more

---
*Auto-generated documentation*
