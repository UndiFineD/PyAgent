# base_pattern

**File**: `src\core\base\work_patterns\base_pattern.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 62  
**Complexity**: 3 (simple)

## Overview

Base Work Pattern for PyAgent swarm collaboration patterns.

## Classes (1)

### `WorkPattern`

**Inherits from**: ABC

Abstract base class for work patterns in PyAgent swarm.

Work patterns define how multiple agents collaborate on tasks,
inspired by agentUniverse PEER pattern and other collaborative frameworks.

**Methods** (3):
- `__init__(self, name, description)`
- `validate_agents(self)`
- `get_required_agents(self)`

## Dependencies

**Imports** (6):
- `abc.ABC`
- `abc.abstractmethod`
- `src.core.base.common.models.communication_models.CascadeContext`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
