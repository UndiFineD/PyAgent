#!/usr/bin/env python3
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

r"""LLM_CONTEXT_START

## Source: src-old/core/base/logic/core/rag_core.description.md

# rag_core

**File**: `src\\core\base\\logic\\core\rag_core.py`  
**Type**: Python Module  
**Summary**: 12 classes, 0 functions, 15 imports  
**Lines**: 720  
**Complexity**: 4 (simple)

## Overview

RAG (Retrieval-Augmented Generation) Core

Implements advanced RAG patterns from AgentCloud for enhanced agent knowledge retrieval.
Supports multiple vector databases, retrieval strategies, and tool integration.
Based on AgentCloud's RAG tool implementation with pre/post processors.

## Classes (12)

### `VectorStoreType`

**Inherits from**: str, Enum

Supported vector store types.

### `RetrievalStrategy`

**Inherits from**: str, Enum

Retrieval strategies for RAG.

### `DocumentType`

**Inherits from**: str, Enum

Types of documents that can be stored.

### `Document`

Document for RAG storage.

### `RetrievalConfig`

Configuration for retrieval operations.

### `RAGToolConfig`

Configuration for RAG tool.

### `RetrievalResult`

Result of a retrieval operation.

### `RAGQuery`

RAG query with context.

### `VectorStoreInterface`

**Inherits from**: Protocol

Protocol for vector store implementations.

### `BaseVectorStore`

Base class for vector store implementations.

**Methods** (1):
- `__init__(self, config)`

### `RAGCore`

**Inherits from**: BaseCore

RAG (Retrieval-Augmented Generation) Core

Implements advanced RAG patterns from AgentCloud:
- Multiple vector store support (Qdrant, Pinecone, etc.)
- Advanced retrieval strategies (MMR, self-query, multi-query, time-weighted)
- Pre/post processing pipelines
- Document management and chunking
- Tool integration for agent use

Based on AgentCloud's sophisticated RAG tool implementation.

**Methods** (2):
- `__init__(self)`
- `_calculate_similarity(self, text1, text2)`

### `MockVectorStore`

**Inherits from**: BaseVectorStore

Mock vector store for testing and development.

**Methods** (1):
- `__init__(self, config)`

## Dependencies

**Imports** (15):
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `enum.Enum`
- `logging`
- `src.core.base.common.base_core.BaseCore`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Protocol`
- `typing.Union`
- `uuid`

---
*Auto-generated documentation*
## Source: src-old/core/base/logic/core/rag_core.improvements.md

# Improvements for rag_core

**File**: `src\\core\base\\logic\\core\rag_core.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 720 lines (large)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `rag_core_test.py` with pytest tests

### Code Organization
- [TIP] **12 classes in one file** - Consider splitting into separate modules

### File Complexity
- [!] **Large file** (720 lines) - Consider refactoring

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

"""
RAG (Retrieval-Augmented Generation) Core

Implements advanced RAG patterns from AgentCloud for enhanced agent knowledge retrieval.
Supports multiple vector databases, retrieval strategies, and tool integration.
Based on AgentCloud's RAG tool implementation with pre/post processors.
"""
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Protocol

from src.core.base.common.base_core import BaseCore


class VectorStoreType(str, Enum):
    """
    """
