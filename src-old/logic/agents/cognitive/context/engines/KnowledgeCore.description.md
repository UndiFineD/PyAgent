# KnowledgeCore

**File**: `src\logic\agents\cognitive\context\engines\KnowledgeCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 38  
**Complexity**: 1 (simple)

## Overview

KnowledgeCore logic for specialized workspace analysis.
Contains pure regex and indexing logic for fast symbol discovery.
This file is optimized for Rust migration (Phase 114).

## Classes (1)

### `KnowledgeCore`

**Inherits from**: KnowledgeSymbolMixin, KnowledgeSearchMixin, KnowledgeProcessMixin

KnowledgeCore performs pure computational analysis of workspace symbols.
No I/O or database operations are allowed here to ensure Rust portability.

**Methods** (1):
- `__init__(self, fleet)`

## Dependencies

**Imports** (5):
- `knowledge_mixins.KnowledgeProcessMixin.KnowledgeProcessMixin`
- `knowledge_mixins.KnowledgeSearchMixin.KnowledgeSearchMixin`
- `knowledge_mixins.KnowledgeSymbolMixin.KnowledgeSymbolMixin`
- `src.core.base.Version.VERSION`
- `typing.Any`

---
*Auto-generated documentation*
