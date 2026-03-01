# MemoryConsolidatorCore

**File**: `src\classes\cognitive\MemoryConsolidatorCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 87  
**Complexity**: 4 (simple)

## Overview

MemoryConsolidatorCore logic for PyAgent.
Pure logic for distilling interactions into insights.
No I/O or side effects.

## Classes (1)

### `MemoryConsolidatorCore`

Pure logic core for memory consolidation.

**Methods** (4):
- `create_interaction_entry(agent, task, outcome)`
- `distill_buffer(buffer)`
- `filter_memory_by_query(memory, query)`
- `format_daily_memory(insights)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `src.core.base.version.VERSION`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
