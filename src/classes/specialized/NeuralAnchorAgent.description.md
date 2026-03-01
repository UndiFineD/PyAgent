# NeuralAnchorAgent

**File**: `src\classes\specialized\NeuralAnchorAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 84  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for NeuralAnchorAgent.

## Classes (1)

### `NeuralAnchorAgent`

**Inherits from**: BaseAgent

Agent responsible for anchoring reasoning to verified external sources of truth.
Validates agent statements against documentation, specifications, and issues.

**Methods** (4):
- `__init__(self, file_path)`
- `load_anchor_source(self, source_name, content, source_type)`
- `validate_claim(self, claim, context_sources)`
- `anchor_reasoning_step(self, reasoning_chain, sources)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `re`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
