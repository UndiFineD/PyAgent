#!/usr/bin/env python3
from __future__ import annotations
r"""LLM_CONTEXT_START

## Source: src-old/classes/context/SemanticSearchEngine.description.md

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
## Source: src-old/classes/context/SemanticSearchEngine.improvements.md

# Improvements for SemanticSearchEngine

**File**: `src\classes\context\SemanticSearchEngine.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 233 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SemanticSearchEngine_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END

"""


# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Phase 16: Rust acceleration for keyword matching and scoring

r"""Auto-extracted class from agent_context.py"""
