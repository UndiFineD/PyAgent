# IntelligenceCore

**File**: `src\infrastructure\orchestration\IntelligenceCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 9 imports  
**Lines**: 83  
**Complexity**: 5 (moderate)

## Overview

IntelligenceCore: Pure logic for Swarm Collective Intelligence.
Handles weight calculation, insight distillation, and pattern matching.

## Classes (2)

### `SwarmInsight`

Class SwarmInsight implementation.

**Methods** (1):
- `format_for_pool(self)`

### `IntelligenceCore`

Logic-only core for swarm intelligence synthesis.

**Methods** (4):
- `__init__(self, workspace_root)`
- `filter_relevant_insights(self, pool, limit)`
- `generate_synthesis_prompt(self, insights, sql_lessons)`
- `extract_actionable_patterns(self, raw_patterns)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
