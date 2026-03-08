# Class Breakdown: rag_core

**File**: `src\core\base\logic\core\rag_core.py`  
**Classes**: 12

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `VectorStoreType`

**Line**: 34  
**Inherits**: str, Enum  
**Methods**: 0

Supported vector store types.

[TIP] **Suggested split**: Move to `vectorstoretype.py`

---

### 2. `RetrievalStrategy`

**Line**: 43  
**Inherits**: str, Enum  
**Methods**: 0

Retrieval strategies for RAG.

[TIP] **Suggested split**: Move to `retrievalstrategy.py`

---

### 3. `DocumentType`

**Line**: 53  
**Inherits**: str, Enum  
**Methods**: 0

Types of documents that can be stored.

[TIP] **Suggested split**: Move to `documenttype.py`

---

### 4. `Document`

**Line**: 63  
**Methods**: 0

Document for RAG storage.

[TIP] **Suggested split**: Move to `document.py`

---

### 5. `RetrievalConfig`

**Line**: 75  
**Methods**: 0

Configuration for retrieval operations.

[TIP] **Suggested split**: Move to `retrievalconfig.py`

---

### 6. `RAGToolConfig`

**Line**: 86  
**Methods**: 0

Configuration for RAG tool.

[TIP] **Suggested split**: Move to `ragtoolconfig.py`

---

### 7. `RetrievalResult`

**Line**: 103  
**Methods**: 0

Result of a retrieval operation.

[TIP] **Suggested split**: Move to `retrievalresult.py`

---

### 8. `RAGQuery`

**Line**: 113  
**Methods**: 0

RAG query with context.

[TIP] **Suggested split**: Move to `ragquery.py`

---

### 9. `VectorStoreInterface`

**Line**: 121  
**Inherits**: Protocol  
**Methods**: 0

Protocol for vector store implementations.

[TIP] **Suggested split**: Move to `vectorstoreinterface.py`

---

### 10. `BaseVectorStore`

**Line**: 147  
**Methods**: 1

Base class for vector store implementations.

[TIP] **Suggested split**: Move to `basevectorstore.py`

---

### 11. `RAGCore`

**Line**: 177  
**Inherits**: BaseCore  
**Methods**: 2

RAG (Retrieval-Augmented Generation) Core

Implements advanced RAG patterns from AgentCloud:
- Multiple vector store support (Qdrant, Pinecone, etc.)
- Advanced retrieval strategies (MMR, self-query, ...

[TIP] **Suggested split**: Move to `ragcore.py`

---

### 12. `MockVectorStore`

**Line**: 657  
**Inherits**: BaseVectorStore  
**Methods**: 1

Mock vector store for testing and development.

[TIP] **Suggested split**: Move to `mockvectorstore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
