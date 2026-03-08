# rag_core

**File**: `src\core\base\logic\core\rag_core.py`  
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
