# SearchMeshCore

**File**: `src\logic\agents\intelligence\core\SearchMeshCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 75  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for SearchMeshCore.

## Classes (1)

### `SearchMeshCore`

SearchMeshCore implements federated search result aggregation and ranking.
It synthesizes results from multiple providers (Google, Bing, Perplexity, Tavily).

**Methods** (3):
- `__init__(self, weights)`
- `aggregate_results(self, raw_results)`
- `filter_redundant(self, results, remembered_urls)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
