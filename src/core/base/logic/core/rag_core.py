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

"""
RAG (Retrieval-Augmented Generation) Core

Implements advanced RAG patterns from AgentCloud for enhanced agent knowledge retrieval.
Supports multiple vector databases, retrieval strategies, and tool integration.
Based on AgentCloud's RAG tool implementation with pre/post processors.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Callable, Union, Protocol
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid

from src.core.base.common.base_core import BaseCore


class VectorStoreType(str, Enum):
    """Supported vector store types."""
    QDRANT = "qdrant"
    PINECONE = "pinecone"
    CHROMA = "chroma"
    WEAVIATE = "weaviate"
    MILVUS = "milvus"


class RetrievalStrategy(str, Enum):
    """Retrieval strategies for RAG."""
    SIMILARITY = "similarity"
    MMR = "mmr"  # Maximal Marginal Relevance
    SELF_QUERY = "self_query"
    MULTI_QUERY = "multi_query"
    TIME_WEIGHTED = "time_weighted"
    CONTEXTUAL_COMPRESSION = "contextual_compression"


class DocumentType(str, Enum):
    """Types of documents that can be stored."""
    TEXT = "text"
    PDF = "pdf"
    WEBPAGE = "webpage"
    CODE = "code"
    MARKDOWN = "markdown"


@dataclass
class Document:
    """Document for RAG storage."""
    doc_id: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    doc_type: DocumentType = DocumentType.TEXT
    embedding: Optional[List[float]] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class RetrievalConfig:
    """Configuration for retrieval operations."""
    strategy: RetrievalStrategy = RetrievalStrategy.SIMILARITY
    top_k: int = 5
    score_threshold: float = 0.0
    fetch_k: int = 20  # For MMR and other strategies
    lambda_mult: float = 0.5  # For MMR diversity
    search_kwargs: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RAGToolConfig:
    """Configuration for RAG tool."""
    tool_id: str
    name: str
    description: str
    vector_store_type: VectorStoreType
    collection_name: str
    retrieval_config: RetrievalConfig = field(default_factory=RetrievalConfig)
    pre_processors: List[Callable] = field(default_factory=list)
    post_processors: List[Callable] = field(default_factory=list)
    embedding_model: str = "text-embedding-ada-002"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class RetrievalResult:
    """Result of a retrieval operation."""
    query: str
    documents: List[Document]
    scores: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)
    retrieved_at: datetime = field(default_factory=datetime.now)


@dataclass
class RAGQuery:
    """RAG query with context."""
    query: str
    filters: Dict[str, Any] = field(default_factory=dict)
    retrieval_config: Optional[RetrievalConfig] = None
    context: Dict[str, Any] = field(default_factory=dict)


class VectorStoreInterface(Protocol):
    """Protocol for vector store implementations."""

    async def add_documents(self, documents: List[Document]) -> List[str]:
        """Add documents to the vector store."""
        ...

    async def similarity_search(
        self,
        query: str,
        k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[tuple[Document, float]]:
        """Perform similarity search."""
        ...

    async def delete_documents(self, doc_ids: List[str]) -> bool:
        """Delete documents from vector store."""
        ...

    async def update_document(self, doc_id: str, document: Document) -> bool:
        """Update a document in the vector store."""
        ...


class BaseVectorStore:
    """Base class for vector store implementations."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

    async def add_documents(self, documents: List[Document]) -> List[str]:
        """Add documents to the vector store."""
        raise NotImplementedError

    async def similarity_search(
        self,
        query: str,
        k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[tuple[Document, float]]:
        """Perform similarity search."""
        raise NotImplementedError

    async def delete_documents(self, doc_ids: List[str]) -> bool:
        """Delete documents from vector store."""
        raise NotImplementedError

    async def update_document(self, doc_id: str, document: Document) -> bool:
        """Update a document in the vector store."""
        raise NotImplementedError


class RAGCore(BaseCore):
    """
    RAG (Retrieval-Augmented Generation) Core

    Implements advanced RAG patterns from AgentCloud:
    - Multiple vector store support (Qdrant, Pinecone, etc.)
    - Advanced retrieval strategies (MMR, self-query, multi-query, time-weighted)
    - Pre/post processing pipelines
    - Document management and chunking
    - Tool integration for agent use

    Based on AgentCloud's sophisticated RAG tool implementation.
    """

    def __init__(self):
        super().__init__()
        self.vector_stores: Dict[str, BaseVectorStore] = {}
        self.rag_tools: Dict[str, RAGToolConfig] = {}
        self.documents: Dict[str, Document] = {}
        self.retrieval_cache: Dict[str, RetrievalResult] = {}

        # Text processing components
        self.text_splitters: Dict[str, Callable] = {}
        self.embedders: Dict[str, Callable] = {}

        self.logger = logging.getLogger(__name__)

    async def register_vector_store(
        self,
        store_id: str,
        store_type: VectorStoreType,
        config: Dict[str, Any]
    ) -> str:
        """
        Register a vector store instance.

        Args:
            store_id: Unique identifier for the store
            store_type: Type of vector store
            config: Configuration for the store

        Returns:
            Store ID
        """
        # In a real implementation, this would instantiate the actual vector store
        # For now, we'll create a mock implementation
        store = MockVectorStore(config)
        self.vector_stores[store_id] = store
        self.logger.info(f"Registered vector store {store_id} of type {store_type}")
        return store_id

    async def create_rag_tool(
        self,
        tool_id: str,
        name: str,
        description: str,
        vector_store_id: str,
        collection_name: str,
        **kwargs
    ) -> RAGToolConfig:
        """
        Create a RAG tool configuration.

        Args:
            tool_id: Unique tool identifier
            name: Tool name
            description: Tool description
            vector_store_id: ID of vector store to use
            collection_name: Collection name in vector store
            **kwargs: Additional configuration

        Returns:
            RAG tool configuration
        """
        if vector_store_id not in self.vector_stores:
            raise ValueError(f"Vector store {vector_store_id} not found")

        if tool_id in self.rag_tools:
            raise ValueError(f"RAG tool {tool_id} already exists")

        tool_config = RAGToolConfig(
            tool_id=tool_id,
            name=name,
            description=description,
            vector_store_type=VectorStoreType.QDRANT,  # Default, would be determined by store
            collection_name=collection_name,
            **kwargs
        )

        self.rag_tools[tool_id] = tool_config
        self.logger.info(f"Created RAG tool {tool_id}")
        return tool_config

    async def add_documents(
        self,
        tool_id: str,
        documents: List[Document],
        chunk_documents: bool = True
    ) -> List[str]:
        """
        Add documents to a RAG tool.

        Args:
            tool_id: RAG tool to add documents to
            documents: Documents to add
            chunk_documents: Whether to chunk documents

        Returns:
            List of document IDs added
        """
        if tool_id not in self.rag_tools:
            raise ValueError(f"RAG tool {tool_id} not found")

        tool_config = self.rag_tools[tool_id]
        vector_store = self.vector_stores.get(tool_config.collection_name)

        if not vector_store:
            raise ValueError(f"Vector store for tool {tool_id} not found")

        # Process documents (chunking, preprocessing)
        processed_docs = []
        for doc in documents:
            if chunk_documents and len(doc.content) > tool_config.chunk_size:
                chunks = await self._chunk_document(doc, tool_config)
                processed_docs.extend(chunks)
            else:
                processed_docs.append(doc)

            # Store in document registry
            self.documents[doc.doc_id] = doc

        # Add to vector store
        doc_ids = await vector_store.add_documents(processed_docs)
        self.logger.info(f"Added {len(doc_ids)} documents to RAG tool {tool_id}")
        return doc_ids

    async def retrieve(
        self,
        tool_id: str,
        query: str,
        retrieval_config: Optional[RetrievalConfig] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> RetrievalResult:
        """
        Retrieve relevant documents for a query.

        Args:
            tool_id: RAG tool to query
            query: Search query
            retrieval_config: Retrieval configuration
            filters: Additional filters

        Returns:
            Retrieval results
        """
        if tool_id not in self.rag_tools:
            raise ValueError(f"RAG tool {tool_id} not found")

        tool_config = self.rag_tools[tool_id]
        config = retrieval_config or tool_config.retrieval_config

        # Apply pre-processors
        processed_query = query
        for processor in tool_config.pre_processors:
            if asyncio.iscoroutinefunction(processor):
                processed_query = await processor(processed_query)
            else:
                res = processor(processed_query)
                if asyncio.iscoroutine(res):
                    processed_query = await res
                else:
                    processed_query = res

        # Perform retrieval based on strategy
        vector_store = self.vector_stores.get(tool_config.collection_name)
        if not vector_store:
            raise ValueError(f"Vector store for tool {tool_id} not found")

        results = await self._perform_retrieval(
            vector_store, processed_query, config, filters
        )

        # Apply post-processors
        processed_results = results
        for processor in tool_config.post_processors:
            processed_results = await processor(processed_results)

        # Create retrieval result
        documents, scores = zip(*processed_results) if processed_results else ([], [])
        result = RetrievalResult(
            query=query,
            documents=list(documents),
            scores=list(scores),
            metadata={"tool_id": tool_id, "strategy": config.strategy.value}
        )

        # Cache result
        cache_key = f"{tool_id}:{hash(query)}"
        self.retrieval_cache[cache_key] = result

        return result

    async def rag_query(
        self,
        tool_id: str,
        rag_query: RAGQuery,
        generate_response: bool = True
    ) -> Dict[str, Any]:
        """
        Perform a complete RAG query with optional response generation.

        Args:
            tool_id: RAG tool to use
            rag_query: RAG query object
            generate_response: Whether to generate a response

        Returns:
            RAG query results with optional generated response
        """
        # Retrieve relevant documents
        retrieval_result = await self.retrieve(
            tool_id=tool_id,
            query=rag_query.query,
            retrieval_config=rag_query.retrieval_config,
            filters=rag_query.filters
        )

        result = {
            "query": rag_query.query,
            "retrieval_result": retrieval_result,
            "context": rag_query.context
        }

        if generate_response:
            # In a real implementation, this would call an LLM
            # For now, we'll create a mock response
            context_text = "\n".join([doc.content for doc in retrieval_result.documents])
            result["generated_response"] = f"Based on the retrieved information: {context_text[:500]}..."

        return result

    async def update_document(self, doc_id: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Update an existing document.

        Args:
            doc_id: Document ID to update
            content: New content
            metadata: New metadata

        Returns:
            Success status
        """
        if doc_id not in self.documents:
            return False

        doc = self.documents[doc_id]
        doc.content = content
        doc.updated_at = datetime.now()
        if metadata:
            doc.metadata.update(metadata)

        # Update in vector stores (would need to find which tools contain this doc)
        # This is simplified - in practice, you'd track document-tool relationships

        self.logger.info(f"Updated document {doc_id}")
        return True

    async def delete_documents(self, doc_ids: List[str]) -> bool:
        """
        Delete documents from all tools and stores.

        Args:
            doc_ids: Document IDs to delete

        Returns:
            Success status
        """
        success = True
        for doc_id in doc_ids:
            if doc_id in self.documents:
                del self.documents[doc_id]

                # Delete from vector stores (simplified)
                for store in self.vector_stores.values():
                    try:
                        await store.delete_documents([doc_id])
                    except Exception as e:
                        self.logger.warning(f"Failed to delete {doc_id} from store: {e}")
                        success = False

        self.logger.info(f"Deleted {len(doc_ids)} documents")
        return success

    async def get_tool_stats(self, tool_id: str) -> Dict[str, Any]:
        """Get statistics for a RAG tool."""
        if tool_id not in self.rag_tools:
            raise ValueError(f"RAG tool {tool_id} not found")

        tool_config = self.rag_tools[tool_id]

        # Count documents in this tool (simplified)
        doc_count = len([d for d in self.documents.values()
                        if tool_id in d.metadata.get("tools", [])])

        return {
            "tool_id": tool_id,
            "name": tool_config.name,
            "document_count": doc_count,
            "vector_store_type": tool_config.vector_store_type.value,
            "collection_name": tool_config.collection_name,
            "retrieval_strategy": tool_config.retrieval_config.strategy.value
        }

    async def _chunk_document(self, document: Document, config: RAGToolConfig) -> List[Document]:
        """Chunk a document into smaller pieces."""
        content = document.content
        chunk_size = config.chunk_size
        overlap = config.chunk_overlap
        
        # Ensure we don't have infinite loops with bad config
        if chunk_size <= overlap:
            overlap = max(0, chunk_size - 1)

        chunks = []
        start = 0

        while start < len(content):
            # 1. Initial hard limit
            end = min(start + chunk_size, len(content))
            
            # Find a good break point if not at the end
            if end < len(content):
                # Ensure we make progress: next start should be > current start
                # next_start = end - overlap
                # we want end - overlap > start  =>  end > start + overlap
                min_end = start + overlap + 1
                
                # Check for sentence delimiters
                # Look backwards from 'end' down to 'min_end'
                # Limit lookback to reasonable amount (e.g. 100 chars)
                found_break = False
                search_end = end
                
                # Try sentence boundaries first
                limit = max(min_end, search_end - 100)
                curr = search_end
                while curr > limit:
                     # Check character at curr-1
                     idx = curr - 1
                     if content[idx] in ".!?" and (curr >= len(content) or content[curr].isspace()):
                         end = curr
                         found_break = True
                         break
                     curr -= 1
                
                if not found_break:
                     # Try word boundaries
                     curr = search_end
                     while curr > min_end:
                         if content[curr-1].isspace():
                             end = curr
                             found_break = True
                             break
                         curr -= 1
                     
                     # If still not found, we keep the hard break at 'end' (start + chunk_size)
                     # which satisfies > start + overlap
            
            chunk_content = content[start:end].strip()
            if chunk_content:
                chunk = Document(
                    doc_id=f"{document.doc_id}_chunk_{len(chunks)}",
                    content=chunk_content,
                    metadata=document.metadata.copy(),
                    doc_type=document.doc_type
                )
                chunk.metadata["parent_doc_id"] = document.doc_id
                chunk.metadata["chunk_index"] = len(chunks)
                chunks.append(chunk)

            # Stop if we have reached the end of content
            if end == len(content):
                break

            # Advance start
            next_start = end - overlap
            
            # Absolute safety guarantee against infinite loops
            if next_start <= start:
                next_start = start + 1
                
            start = next_start

        return chunks

    async def _perform_retrieval(
        self,
        vector_store: BaseVectorStore,
        query: str,
        config: RetrievalConfig,
        filters: Optional[Dict[str, Any]]
    ) -> List[tuple[Document, float]]:
        """Perform retrieval based on strategy."""
        if config.strategy == RetrievalStrategy.SIMILARITY:
            return await vector_store.similarity_search(
                query=query,
                k=config.top_k,
                filters=filters,
                **config.search_kwargs
            )

        elif config.strategy == RetrievalStrategy.MMR:
            # Maximal Marginal Relevance - diversify results
            candidates = await vector_store.similarity_search(
                query=query,
                k=config.fetch_k,
                filters=filters
            )

            # Simple MMR implementation
            selected = []
            remaining = candidates.copy()

            for _ in range(min(config.top_k, len(candidates))):
                if not remaining:
                    break

                # Select document with highest MMR score
                best_score = -float('inf')
                best_doc = None

                for doc, score in remaining:
                    # Calculate MMR: relevance - lambda * max_similarity_to_selected
                    relevance = score
                    max_sim = 0.0

                    for selected_doc, _ in selected:
                        # Simplified similarity calculation
                        sim = self._calculate_similarity(doc.content, selected_doc.content)
                        max_sim = max(max_sim, sim)

                    mmr_score = relevance - config.lambda_mult * max_sim

                    if mmr_score > best_score:
                        best_score = mmr_score
                        best_doc = (doc, score)

                if best_doc:
                    selected.append(best_doc)
                    remaining.remove(best_doc)

            return selected

        elif config.strategy == RetrievalStrategy.SELF_QUERY:
            # Self-querying retrieval (would need metadata filtering)
            return await vector_store.similarity_search(
                query=query,
                k=config.top_k,
                filters=filters,
                **config.search_kwargs
            )

        elif config.strategy == RetrievalStrategy.MULTI_QUERY:
            # Multi-query expansion (would generate multiple queries)
            queries = await self._expand_query(query)
            all_results = []

            for q in queries:
                results = await vector_store.similarity_search(
                    query=q,
                    k=config.top_k // len(queries) + 1,
                    filters=filters
                )
                all_results.extend(results)

            # Remove duplicates and sort by score
            seen_docs = set()
            unique_results = []
            for doc, score in sorted(all_results, key=lambda x: x[1], reverse=True):
                if doc.doc_id not in seen_docs:
                    unique_results.append((doc, score))
                    seen_docs.add(doc.doc_id)
                    if len(unique_results) >= config.top_k:
                        break

            return unique_results

        else:
            # Default to similarity search
            return await vector_store.similarity_search(
                query=query,
                k=config.top_k,
                filters=filters,
                **config.search_kwargs
            )

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity (Jaccard similarity)."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union) if union else 0.0

    async def _expand_query(self, query: str) -> List[str]:
        """Expand a query into multiple related queries."""
        # Simple query expansion - in practice, this would use an LLM
        expansions = [
            query,
            f"What is {query}?",
            f"Explain {query}",
            f"Details about {query}",
            f"Information on {query}"
        ]
        return expansions

    async def cleanup(self):
        """Cleanup all resources."""
        self.vector_stores.clear()
        self.rag_tools.clear()
        self.documents.clear()
        self.retrieval_cache.clear()
        self.text_splitters.clear()
        self.embedders.clear()


class MockVectorStore(BaseVectorStore):
    """Mock vector store for testing and development."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.documents: Dict[str, Document] = {}
        self.embeddings: Dict[str, List[float]] = {}

    async def add_documents(self, documents: List[Document]) -> List[str]:
        """Add documents to mock store."""
        doc_ids = []
        for doc in documents:
            self.documents[doc.doc_id] = doc
            # Mock embedding
            self.embeddings[doc.doc_id] = [0.1] * 384  # Mock 384-dim embedding
            doc_ids.append(doc.doc_id)
        return doc_ids

    async def similarity_search(
        self,
        query: str,
        k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[tuple[Document, float]]:
        """Perform mock similarity search."""
        # Simple keyword matching for mock
        query_words = set(query.lower().split())
        results = []

        for doc in self.documents.values():
            if filters:
                # Apply filters
                skip = False
                for key, value in filters.items():
                    if doc.metadata.get(key) != value:
                        skip = True
                        break
                if skip:
                    continue

            doc_words = set(doc.content.lower().split())
            similarity = len(query_words & doc_words) / len(query_words | doc_words) if query_words | doc_words else 0.0

            if similarity > 0.0:
                results.append((doc, similarity))

        # Sort by similarity and return top k
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]

    async def delete_documents(self, doc_ids: List[str]) -> bool:
        """Delete documents from mock store."""
        for doc_id in doc_ids:
            self.documents.pop(doc_id, None)
            self.embeddings.pop(doc_id, None)
        return True

    async def update_document(self, doc_id: str, document: Document) -> bool:
        """Update document in mock store."""
        if doc_id in self.documents:
            self.documents[doc_id] = document
            return True
        return False
