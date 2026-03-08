# KnowledgeCore

**File**: `src\logic\agents\cognitive\context\utils\KnowledgeCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 118  
**Complexity**: 5 (moderate)

## Overview

KnowledgeCore logic for specialized workspace analysis.
Contains pure regex and indexing logic for fast symbol discovery.

## Classes (1)

### `KnowledgeCore`

KnowledgeCore logic for specialized workspace analysis.
Uses SQLite FTS5 for extreme scalability (Trillion-Parameter compatible).

**Methods** (5):
- `__init__(self, workspace_root)`
- `_init_db(self)`
- `extract_symbols_from_python(self, content)`
- `extract_backlinks_from_markdown(self, content)`
- `build_symbol_map(self, root, extension_patterns)`

## Dependencies

**Imports** (9):
- `json`
- `logging`
- `pathlib.Path`
- `re`
- `sqlite3`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
