# TheoryOfMind

**File**: `src\classes\cognitive\TheoryOfMind.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 61  
**Complexity**: 5 (moderate)

## Overview

Shell for TheoryOfMind, managing agent profiles and state.

## Classes (1)

### `TheoryOfMind`

Models the mental states and knowledge domains of other agents.

Acts as the I/O Shell for TheoryOfMindCore.

**Methods** (5):
- `__init__(self)`
- `update_model(self, agent_name, observations)`
- `estimate_knowledge(self, agent_name, topic)`
- `suggest_collaborator(self, task)`
- `get_mental_map(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `src.core.base.version.VERSION`
- `src.logic.cognitive.TheoryOfMindCore.TheoryOfMindCore`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
