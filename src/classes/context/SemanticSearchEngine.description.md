# SemanticSearchEngine

**File**: `src\classes\context\SemanticSearchEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 233  
**Complexity**: 7 (moderate)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `SemanticSearchEngine`

Performs semantic code search using embeddings.

Provides functionality to search code using semantic similarity
rather than just keyword matching.

Attributes:
    results: List of search results.
    index: Index of embedded content.

Example:
    >>> engine=SemanticSearchEngine()
    >>> results=engine.search("function that handles authentication")

**Methods** (7):
- `__init__(self, persist_directory)`
- `_get_collection(self)`
- `set_algorithm(self, algorithm)`
- `add_document(self, doc_id, content)`
- `clear(self)`
- `index_content(self, file_path, content)`
- `search(self, query, algorithm)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `chromadb`
- `chromadb.utils.embedding_functions`
- `logging`
- `pydantic`
- `pydantic_settings.BaseSettings`
- `rust_core`
- `src.core.base.Version.VERSION`
- `src.logic.agents.cognitive.context.models.SemanticSearchResult.SemanticSearchResult`
- `src.logic.agents.cognitive.context.utils.SearchAlgorithm.SearchAlgorithm`
- `typing.Any`

---
*Auto-generated documentation*
