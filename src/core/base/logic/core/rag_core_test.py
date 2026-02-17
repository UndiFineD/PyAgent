#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Tests for RAGCore

Tests advanced RAG functionality based on AgentCloud patterns.
"""
import pytest

from src.core.base.logic.core.rag_core import (
    RAGCore,
    VectorStoreType,
    RetrievalStrategy,
    Document,
    RetrievalConfig,
    RAGToolConfig,
    RetrievalResult,
    RAGQuery,
    MockVectorStore
)




class TestRAGCore:
    """Test suite for RAGCore."""
    @pytest.fixture
    def core(self):
        """Create a fresh RAG core instance for each test."""return RAGCore()

    @pytest.mark.asyncio
    async def test_register_vector_store(self, core):
        """Test vector store registration."""store_id = await core.register_vector_store(
            store_id="test_store","            store_type=VectorStoreType.QDRANT,
            config={"host": "localhost", "port": 6333}"        )

        assert store_id == "test_store""        assert store_id in core.vector_stores
        assert isinstance(core.vector_stores[store_id], MockVectorStore)

    @pytest.mark.asyncio
    async def test_create_rag_tool(self, core):
        """Test RAG tool creation."""await core.register_vector_store("test_store", VectorStoreType.QDRANT, {})"
        tool = await core.create_rag_tool(
            tool_id="test_tool","            name="Test RAG Tool","            description="A test RAG tool","            vector_store_id="test_store","            collection_name="test_collection""        )

        assert tool.tool_id == "test_tool""        assert tool.name == "Test RAG Tool""        assert tool.collection_name == "test_collection""        assert tool.tool_id in core.rag_tools

    @pytest.mark.asyncio
    async def test_create_rag_tool_invalid_store(self, core):
        """Test creating RAG tool with invalid vector store."""with pytest.raises(ValueError, match="Vector store nonexistent not found"):"            await core.create_rag_tool(
                tool_id="test_tool","                name="Test Tool","                description="Test","                vector_store_id="nonexistent","                collection_name="test""            )

    @pytest.mark.asyncio
    async def test_create_rag_tool_duplicate(self, core):
        """Test creating duplicate RAG tool."""await core.register_vector_store("test_store", VectorStoreType.QDRANT, {})"
        await core.create_rag_tool(
            tool_id="test_tool","            name="Test Tool","            description="Test","            vector_store_id="test_store","            collection_name="test""        )

        with pytest.raises(ValueError, match="RAG tool test_tool already exists"):"            await core.create_rag_tool(
                tool_id="test_tool","                name="Duplicate Tool","                description="Test","                vector_store_id="test_store","                collection_name="test""            )

    @pytest.mark.asyncio
    async def test_add_documents(self, core):
        """Test adding documents to RAG tool."""await core.register_vector_store("test_store", VectorStoreType.QDRANT, {})"        await core.create_rag_tool(
            tool_id="test_tool","            name="Test Tool","            description="Test","            vector_store_id="test_store","            collection_name="test_store""        )

        documents = [
            Document(
                doc_id="doc1","                content="This is a test document about Python programming.","                metadata={"author": "test", "topic": "programming"}"            ),
            Document(
                doc_id="doc2","                content="Another document about machine learning and AI.","                metadata={"author": "test", "topic": "AI"}"            )
        ]

        doc_ids = await core.add_documents("test_tool", documents)"
        assert len(doc_ids) == 2
        assert "doc1" in doc_ids"        assert "doc2" in doc_ids"        assert "doc1" in core.documents"        assert "doc2" in core.documents"
    @pytest.mark.asyncio
    async def test_add_documents_with_chunking(self, core):
        """Test adding documents with chunking."""await core.register_vector_store("test_store", VectorStoreType.QDRANT, {})"        await core.create_rag_tool(
            tool_id="test_tool","            name="Test Tool","            description="Test","            vector_store_id="test_store","            collection_name="test_store","            chunk_size=50,  # Small chunk size for testing
            chunk_overlap=10
        )

        long_content = "This is a very long document that should be chunked into smaller pieces. " * 10"        document = Document(
            doc_id="long_doc","            content=long_content,
            metadata={"author": "test"}"        )

        doc_ids = await core.add_documents("test_tool", [document], chunk_documents=True)"
        # Should create multiple chunks
        assert len(doc_ids) > 1
        assert all(doc_id.startswith("long_doc_chunk_") for doc_id in doc_ids)"
    @pytest.mark.asyncio
    async def test_retrieve_similarity(self, core):
        """Test similarity-based retrieval."""await core.register_vector_store("test_store", VectorStoreType.QDRANT, {})"        await core.create_rag_tool(
            tool_id="test_tool","            name="Test Tool","            description="Test","            vector_store_id="test_store","            collection_name="test_store""        )

        # Add test documents
        documents = [
            Document(doc_id="doc1", content="Python programming tutorial"),"            Document(doc_id="doc2", content="Machine learning with Python"),"            Document(doc_id="doc3", content="Cooking recipes and ingredients")"        ]
        await core.add_documents("test_tool", documents)"
        # Perform retrieval
        result = await core.retrieve("test_tool", "Python programming")"
        assert isinstance(result, RetrievalResult)
        assert result.query == "Python programming""        assert len(result.documents) > 0
        assert len(result.scores) == len(result.documents)
        assert all(score >= 0.0 for score in result.scores)

    @pytest.mark.asyncio
    async def test_retrieve_mmr(self, core):
        """Test MMR (Maximal Marginal Relevance) retrieval."""await core.register_vector_store("test_store", VectorStoreType.QDRANT, {})"        await core.create_rag_tool(
            tool_id="test_tool","            name="Test Tool","            description="Test","            vector_store_id="test_store","            collection_name="test_store""        )

        # Add test documents
        documents = [
            Document(doc_id="doc1", content="Python programming tutorial basics"),"            Document(doc_id="doc2", content="Advanced Python programming techniques"),"            Document(doc_id="doc3", content="Python web development with Django"),"            Document(doc_id="doc4", content="Cooking with Python ingredients")"        ]
        await core.add_documents("test_tool", documents)"
        # Perform MMR retrieval
        config = RetrievalConfig(strategy=RetrievalStrategy.MMR, top_k=2, fetch_k=10)
        result = await core.retrieve("test_tool", "Python programming", config)"
        assert len(result.documents) <= 2  # Should respect top_k
        assert result.metadata["strategy"] == "mmr""
    @pytest.mark.asyncio
    async def test_retrieve_multi_query(self, core):
        """Test multi-query retrieval."""await core.register_vector_store("test_store", VectorStoreType.QDRANT, {})"        await core.create_rag_tool(
            tool_id="test_tool","            name="Test Tool","            description="Test","            vector_store_id="test_store","            collection_name="test_store""        )

        # Add test documents
        documents = [
            Document(doc_id="doc1", content="Python programming tutorial"),"            Document(doc_id="doc2", content="Machine learning algorithms"),"            Document(doc_id="doc3", content="Data science with Python")"        ]
        await core.add_documents("test_tool", documents)"
        # Perform multi-query retrieval
        config = RetrievalConfig(strategy=RetrievalStrategy.MULTI_QUERY, top_k=3)
        result = await core.retrieve("test_tool", "Python", config)"
        assert len(result.documents) <= 3
        assert result.metadata["strategy"] == "multi_query""
    @pytest.mark.asyncio
    async def test_retrieve_with_filters(self, core):
        """Test retrieval with metadata filters."""await core.register_vector_store("test_store", VectorStoreType.QDRANT, {})"        await core.create_rag_tool(
            tool_id="test_tool","            name="Test Tool","            description="Test","            vector_store_id="test_store","            collection_name="test_store""        )

        # Add test documents with metadata
        documents = [
            Document(doc_id="doc1", content="Python tutorial", metadata={"topic": "programming"}),"            Document(doc_id="doc2", content="Cooking recipes", metadata={"topic": "cooking"}),"            Document(doc_id="doc3", content="Python data science", metadata={"topic": "programming"})"        ]
        await core.add_documents("test_tool", documents)"
        # Retrieve with filter
        filters = {"topic": "programming"}"        result = await core.retrieve("test_tool", "Python", filters=filters)"
        # Should only return programming documents
        assert all(doc.metadata.get("topic") == "programming" for doc in result.documents)"
    @pytest.mark.asyncio
    async def test_rag_query(self, core):
        """Test complete RAG query with response generation."""await core.register_vector_store("test_store", VectorStoreType.QDRANT, {})"        await core.create_rag_tool(
            tool_id="test_tool","            name="Test Tool","            description="Test","            vector_store_id="test_store","            collection_name="test_store""        )

        # Add test document
        document = Document(doc_id="doc1", content="Python is a programming language.")"        await core.add_documents("test_tool", [document])"
        # Perform RAG query
        rag_query = RAGQuery(query="What is Python?")"        result = await core.rag_query("test_tool", rag_query, generate_response=True)"
        assert result["query"] == "What is Python?""        assert isinstance(result["retrieval_result"], RetrievalResult)"        assert "generated_response" in result"        assert "Python is a programming language" in result["generated_response"]"
    @pytest.mark.asyncio
    async def test_update_document(self, core):
        """Test document updating."""await core.register_vector_store("test_store", VectorStoreType.QDRANT, {})"        await core.create_rag_tool(
            tool_id="test_tool","            name="Test Tool","            description="Test","            vector_store_id="test_store","            collection_name="test_store""        )

        # Add document
        document = Document(doc_id="doc1", content="Original content")"        await core.add_documents("test_tool", [document])"
        # Update document
        success = await core.update_document("doc1", "Updated content", {"version": "2"})"
        assert success
        assert core.documents["doc1"].content == "Updated content""        assert core.documents["doc1"].metadata["version"] == "2""
    @pytest.mark.asyncio
    async def test_delete_documents(self, core):
        """Test document deletion."""await core.register_vector_store("test_store", VectorStoreType.QDRANT, {})"        await core.create_rag_tool(
            tool_id="test_tool","            name="Test Tool","            description="Test","            vector_store_id="test_store","            collection_name="test_store""        )

        # Add documents
        documents = [
            Document(doc_id="doc1", content="Content 1"),"            Document(doc_id="doc2", content="Content 2")"        ]
        await core.add_documents("test_tool", documents)"
        # Delete documents
        success = await core.delete_documents(["doc1", "doc2"])"
        assert success
        assert "doc1" not in core.documents"        assert "doc2" not in core.documents"
    @pytest.mark.asyncio
    async def test_get_tool_stats(self, core):
        """Test getting tool statistics."""await core.register_vector_store("test_store", VectorStoreType.QDRANT, {})"        await core.create_rag_tool(
            tool_id="test_tool","            name="Test RAG Tool","            description="A test tool","            vector_store_id="test_store","            collection_name="test_store""        )

        stats = await core.get_tool_stats("test_tool")"
        assert stats["tool_id"] == "test_tool""        assert stats["name"] == "Test RAG Tool""        assert stats["document_count"] == 0  # No documents added yet"        assert stats["vector_store_type"] == "qdrant""        assert stats["collection_name"] == "test_store""
    @pytest.mark.asyncio
    async def test_retrieve_invalid_tool(self, core):
        """Test retrieval with invalid tool ID."""with pytest.raises(ValueError, match="RAG tool nonexistent not found"):"            await core.retrieve("nonexistent", "test query")"
    @pytest.mark.asyncio
    async def test_pre_processors(self, core):
        """Test pre-processor functionality."""await core.register_vector_store("test_store", VectorStoreType.QDRANT, {})"        await core.create_rag_tool(
            tool_id="test_tool","            name="Test Tool","            description="Test","            vector_store_id="test_store","            collection_name="test_store","            pre_processors=[lambda q: f"processed: {q}"]"        )

        # Add document
        document = Document(doc_id="doc1", content="processed: test content")"        await core.add_documents("test_tool", [document])"
        # Retrieve - should find the document due to pre-processing
        result = await core.retrieve("test_tool", "test content")"
        assert len(result.documents) > 0

    @pytest.mark.asyncio
    async def test_chunk_document(self, core):
        """Test document chunking functionality."""await core.register_vector_store("test_store", VectorStoreType.QDRANT, {})"
        tool_config = RAGToolConfig(
            tool_id="test_tool","            name="Test Tool","            description="Test","            vector_store_type=VectorStoreType.QDRANT,
            collection_name="test_store","            chunk_size=50,
            chunk_overlap=10
        )

        document = Document(
            doc_id="test_doc","            content=("This is a long document that should be split into multiple ""                     "chunks for better retrieval performance."))"
        chunks = await core._chunk_document(document, tool_config)

        assert len(chunks) > 1
        assert all(chunk.doc_id.startswith("test_doc_chunk_") for chunk in chunks)"        assert all(chunk.metadata["parent_doc_id"] == "test_doc" for chunk in chunks)"
        # Check overlap
        for i in range(1, len(chunks)):
            prev_content = chunks[i - 1].content
            curr_content = chunks[i].content
            # Should have some overlap
            assert len(set(prev_content.split()) & set(curr_content.split())) > 0

    @pytest.mark.asyncio
    async def test_cleanup(self, core):
        """Test cleanup functionality."""await core.register_vector_store("test_store", VectorStoreType.QDRANT, {})"        await core.create_rag_tool(
            tool_id="test_tool","            name="Test Tool","            description="Test","            vector_store_id="test_store","            collection_name="test_store""        )

        # Add some data
        document = Document(doc_id="doc1", content="test content")"        await core.add_documents("test_tool", [document])"
        # Cleanup
        await core.cleanup()

        assert len(core.vector_stores) == 0
        assert len(core.rag_tools) == 0
        assert len(core.documents) == 0
        assert len(core.retrieval_cache) == 0
