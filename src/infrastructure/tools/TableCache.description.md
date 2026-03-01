# TableCache

**File**: `src\infrastructure\tools\TableCache.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 5 imports  
**Lines**: 76  
**Complexity**: 6 (moderate)

## Overview

TableCache: Trie-based metadata precomputation for Text-to-SQL.
Implemented based on arXiv:2601.08743 (Jan 2026).

## Classes (3)

### `TableMetadata`

Class TableMetadata implementation.

### `TableTrieNode`

Class TableTrieNode implementation.

**Methods** (1):
- `__init__(self)`

### `TableCacheManager`

Manages a Trie-based cache of database schema metadata.
Enables 3.6x TTFT speedup for Text-to-SQL tasks by pre-filtering schema.

**Methods** (5):
- `__init__(self)`
- `insert(self, table_name, columns)`
- `search_prefix(self, prefix)`
- `_collect_metadata(self, node, results)`
- `prune_schema(self, query)`

## Dependencies

**Imports** (5):
- `dataclasses`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
