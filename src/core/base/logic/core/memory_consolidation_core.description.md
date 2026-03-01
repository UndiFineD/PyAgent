# memory_consolidation_core

**File**: `src\core\base\logic\core\memory_consolidation_core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 178  
**Complexity**: 6 (moderate)

## Overview

Core logic regarding Memory Consolidation.
Implements dream-inspired memory processing:
- Exponential decay for aging memories.
- Creative association discovery (REM-like).
- Semantic clustering for memory compression.

## Classes (1)

### `MemoryConsolidationCore`

Core engine for consolidating agent memories.
Inspired by biological memory patterns.

**Methods** (6):
- `__init__(self, base_decay_rate, importance_protection_threshold, grace_period_days, similarity_threshold)`
- `calculate_relevance(self, created_at, last_accessed, importance, relationship_count, confidence, current_time)`
- `discover_creative_associations(self, memories, similarity_threshold)`
- `_calculate_similarity(self, vec1, vec2)`
- `is_protected(self, memory_type, importance, age_days, is_manually_protected)`
- `get_summary_prompt(self, cluster)`

## Dependencies

**Imports** (11):
- `asyncio`
- `datetime.datetime`
- `datetime.timedelta`
- `datetime.timezone`
- `logging`
- `math`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
