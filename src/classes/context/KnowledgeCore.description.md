# KnowledgeCore

**File**: `src\classes\context\KnowledgeCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 111  
**Complexity**: 7 (moderate)

## Overview

KnowledgeCore logic for specialized workspace analysis.
Contains pure regex and indexing logic for fast symbol discovery.
This file is optimized for Rust migration (Phase 114).

## Classes (1)

### `KnowledgeCore`

KnowledgeCore performs pure computational analysis of workspace symbols.
No I/O or database operations are allowed here to ensure Rust portability.

**Methods** (7):
- `__init__(self, fleet)`
- `extract_symbols(self, content, pattern)`
- `extract_python_symbols(self, content)`
- `extract_markdown_backlinks(self, content)`
- `build_symbol_map(self, root, patterns)`
- `process_file_content(self, rel_path, content, extension)`
- `compute_similarity(self, text_a, text_b)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `re`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
