# GlobalContextEngine

**File**: `src\classes\context\GlobalContextEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 64  
**Complexity**: 1 (simple)

## Overview

Advanced Long-Term Memory (LTM) for agents.
Consolidates episodic memories into semantic knowledge and persistent preferences.
Inspired by mem0 and BabyAGI patterns.

## Classes (1)

### `GlobalContextEngine`

**Inherits from**: ContextShardMixin, ContextDataMixin, ContextEntityMixin, ContextConsolidationMixin

Manages persistent project-wide knowledge and agent preferences.
Shell for GlobalContextCore.

**Methods** (1):
- `__init__(self, workspace_root, fleet)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `mixins.ContextConsolidationMixin.ContextConsolidationMixin`
- `mixins.ContextDataMixin.ContextDataMixin`
- `mixins.ContextEntityMixin.ContextEntityMixin`
- `mixins.ContextShardMixin.ContextShardMixin`
- `pathlib.Path`
- `src.core.base.Version.VERSION`
- `src.logic.agents.cognitive.context.engines.GlobalContextCore.GlobalContextCore`
- `typing.Any`

---
*Auto-generated documentation*
