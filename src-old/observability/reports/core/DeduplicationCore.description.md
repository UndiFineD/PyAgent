# DeduplicationCore

**File**: `src\observability\reports\core\DeduplicationCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 53  
**Complexity**: 3 (simple)

## Overview

Core logic for Report Deduplication (Phase 183).
Handles similarity calculations and JSONL export.

## Classes (1)

### `DeduplicationCore`

Class DeduplicationCore implementation.

**Methods** (3):
- `jaccard_similarity(s1, s2)`
- `deduplicate_items(items, key, threshold)`
- `export_to_jsonl(items, output_path)`

## Dependencies

**Imports** (4):
- `json`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
