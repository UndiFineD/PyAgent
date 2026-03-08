# LinguisticAgent

**File**: `src\classes\specialized\LinguisticAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 41  
**Complexity**: 3 (simple)

## Overview

Agent specializing in linguistic articulation and epistemic subordination.
Ensures that the LLM only verbalizes grounded results and never hallucinates new technical facts.

## Classes (1)

### `LinguisticAgent`

**Inherits from**: BaseAgent

The linguistic surface layer of the PyAgent OS.

**Methods** (3):
- `__init__(self, file_path)`
- `articulate_results(self, technical_report, user_query)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (3):
- `logging`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`

---
*Auto-generated documentation*
