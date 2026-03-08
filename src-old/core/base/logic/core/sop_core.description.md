# sop_core

**File**: `src\core\base\logic\core\sop_core.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 7 imports  
**Lines**: 91  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for sop_core.

## Classes (3)

### `SopStep`

**Inherits from**: BaseModel

Class SopStep implementation.

### `SopManifest`

**Inherits from**: BaseModel

Class SopManifest implementation.

### `SopCore`

Manages 'Standard Operating Procedures' for autonomous workflows.
Pattern harvested from 'Acontext' and 'self_evolving_subagent'.

**Methods** (6):
- `__init__(self)`
- `create_sop(self, name, domain, steps)`
- `get_sop(self, name)`
- `update_sop_metrics(self, name, success)`
- `merge_sops(self, name_a, name_b, new_name)`
- `generate_agent_prompt(self, sop_name)`

## Dependencies

**Imports** (7):
- `pydantic.BaseModel`
- `pydantic.Field`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `uuid`

---
*Auto-generated documentation*
