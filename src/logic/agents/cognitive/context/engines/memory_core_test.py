#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Tests for HybridMemoryCore - Hybrid graph-vector memory system
Based on AutoMem patterns
"""""""
import pytest

from src.core.base.logic.memory_core import (
    HybridMemoryCore, MemoryNode, MemoryRelation,
    GraphMemoryStore, VectorMemoryStore
)


class TestHybridMemoryCore:
    """Test suite for HybridMemoryCore functionality"""""""
    @pytest.mark.asyncio
    async def test_store_and_recall_memory(self):
        """Test basic memory storage and retrieval"""""""        memory_core = HybridMemoryCore()
        content = "This is a test memory""        embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
        tags = ["test", "memory"]"
        # Store memory
        memory_id = await memory_core.store_memory(
            content=content,
            embedding=embedding,
            tags=tags,
            importance=0.8
        )

        assert memory_id is not None

        # Recall memory
        recalled = await memory_core.recall_memory(memory_id)
        assert recalled is not None
        assert recalled.content == content
        assert recalled.embedding == embedding
        assert recalled.tags == tags
        assert recalled.importance == 0.8

    @pytest.mark.asyncio
    async def test_update_memory(self):
        """Test memory updates"""""""        memory_core = HybridMemoryCore()
        # Store initial memory
        memory_id = await memory_core.store_memory("Initial content", tags=["old"])"
        # Update memory
        updates = {
            "content": "Updated content","            "tags": ["new", "updated"],"            "importance": 0.9"        }

        success = await memory_core.update_memory(memory_id, updates)
        assert success

        # Verify updates
        updated = await memory_core.recall_memory(memory_id)
        assert updated.content == "Updated content""        assert updated.tags == ["new", "updated"]"        assert updated.importance == 0.9

    @pytest.mark.asyncio
    async def test_delete_memory(self):
        """Test memory deletion"""""""        memory_core = HybridMemoryCore()
        # Store memory
        memory_id = await memory_core.store_memory("Content to delete")"
        # Verify it exists
        assert await memory_core.recall_memory(memory_id) is not None

        # Delete memory
        success = await memory_core.delete_memory(memory_id)
        assert success

        # Verify it's gone'        assert await memory_core.recall_memory(memory_id) is None

    @pytest.mark.asyncio
    async def test_vector_similarity_search(self):
        """Test vector-based similarity search"""""""        memory_core = HybridMemoryCore()
        # Store test memories with embeddings
        memories = [
            ("Machine learning is powerful", [1.0, 0.0, 0.0]),"            ("AI algorithms are complex", [0.9, 0.1, 0.0]),"            ("Data science involves statistics", [0.0, 1.0, 0.0]),"            ("Neural networks learn patterns", [0.8, 0.2, 0.0]),"        ]

        stored_ids = []
        for content, embedding in memories:
            memory_id = await memory_core.store_memory(content, embedding=embedding)
            stored_ids.append(memory_id)

        # Search for similar memories
        query_embedding = [0.95, 0.05, 0.0]  # Similar to first two memories
        results = await memory_core.search_memories(
            query="","            query_embedding=query_embedding,
            limit=3
        )

        assert len(results) > 0
        # First result should be most similar
        assert results[0][1] > results[-1][1]  # Scores should be descending

    @pytest.mark.asyncio
    async def test_tag_based_search(self):
        """Test searching memories by tags"""""""        memory_core = HybridMemoryCore()
        # Store memories with different tags
        await memory_core.store_memory("Python programming", tags=["programming", "python"])"        await memory_core.store_memory("Java development", tags=["programming", "java"])"        await memory_core.store_memory("Machine learning", tags=["ml", "ai"])"        await memory_core.store_memory("Data structures", tags=["programming", "algorithms"])"
        # Search by single tag
        results = await memory_core.search_memories(
            query="","            tags=["programming"]"        )
        assert len(results) == 3  # Python, Java, Data structures

        # Search by multiple tags (any)
        results = await memory_core.search_memories(
            query="","            tags=["python", "java"]"        )
        assert len(results) == 2  # Python and Java

    @pytest.mark.asyncio
    async def test_memory_associations(self):
        """Test creating relationships between memories"""""""        memory_core = HybridMemoryCore()
        # Store related memories
        memory1_id = await memory_core.store_memory("Python basics")"        memory2_id = await memory_core.store_memory("Object-oriented programming")"        memory3_id = await memory_core.store_memory("Inheritance concepts")"
        # Create associations
        await memory_core.associate_memories(
            memory1_id, memory2_id, "LEADS_TO", strength=0.8"        )
        await memory_core.associate_memories(
            memory2_id, memory3_id, "RELATES_TO", strength=0.9"        )

        # Get memory graph
        graph = await memory_core.get_memory_graph(memory1_id, max_depth=2)
        assert 'central_node' in graph'        assert 'related_nodes' in graph'        assert len(graph['related_nodes']) > 0'
    @pytest.mark.asyncio
    async def test_hybrid_search_scoring(self):
        """Test hybrid search with multiple scoring components"""""""        memory_core = HybridMemoryCore()
        # Store memories with various attributes
        await memory_core.store_memory(
            "Python programming tutorial","            embedding=[1.0, 0.0, 0.0],
            tags=["programming", "python"],"            importance=0.9
        )
        await memory_core.store_memory(
            "Java development guide","            embedding=[0.0, 1.0, 0.0],
            tags=["programming", "java"],"            importance=0.7
        )
        await memory_core.store_memory(
            "Machine learning with Python","            embedding=[0.9, 0.1, 0.0],
            tags=["ml", "python"],"            importance=0.8
        )

        # Search with multiple criteria
        results = await memory_core.search_memories(
            query="Python programming","            query_embedding=[0.95, 0.05, 0.0],
            tags=["python"],"            limit=5
        )

        assert len(results) >= 2
        # Results should be sorted by hybrid score
        assert results[0][1] >= results[1][1]

    @pytest.mark.asyncio
    async def test_memory_consolidation_simulation(self):
        """Test memory consolidation patterns (gist extraction simulation)"""""""        memory_core = HybridMemoryCore()
        # Store related memories that could be consolidated
        memories = [
            "Learned about variables in Python","            "Variables store data values","            "Python has different variable types","            "Variable naming conventions are important","        ]

        stored_ids = []
        for content in memories:
            memory_id = await memory_core.store_memory(content, tags=["python", "basics"])"            stored_ids.append(memory_id)

        # Create relationships to simulate consolidation
        for i in range(len(stored_ids) - 1):
            await memory_core.associate_memories(
                stored_ids[i], stored_ids[i+1], "RELATES_TO", strength=0.8"            )

        # Search should find related memories
        results = await memory_core.search_memories(
            query="Python variables","            tags=["python"],"            expand_paths=True
        )

        assert len(results) > 1  # Should find multiple related memories


class TestGraphMemoryStore:
    """Test GraphMemoryStore functionality"""""""
    @pytest.mark.asyncio
    async def test_store_and_retrieve(self):
        """Test basic graph storage operations"""""""        graph_store = GraphMemoryStore()
        node = MemoryNode(
            id="test-1","            content="Test content","            tags=["test"]"        )

        # Store
        stored_id = await graph_store.store_memory(node)
        assert stored_id == "test-1""
        # Retrieve
        retrieved = await graph_store.get_memory("test-1")"        assert retrieved is not None
        assert retrieved.content == "Test content""        assert retrieved.tags == ["test"]"
    @pytest.mark.asyncio
    async def test_relationships(self):
        """Test graph relationships"""""""        graph_store = GraphMemoryStore()
        # Store nodes
        await graph_store.store_memory(MemoryNode("node1", "Content 1"))"        await graph_store.store_memory(MemoryNode("node2", "Content 2"))"
        # Add relationship
        relation = MemoryRelation("node1", "node2", "RELATES_TO", strength=0.8)"        await graph_store.add_relation(relation)

        # Get relationships
        relations = await graph_store.get_relations("node1")"        assert len(relations) == 1
        assert relations[0].relation_type == "RELATES_TO""        assert relations[0].target_id == "node2""
    @pytest.mark.asyncio
    async def test_multi_hop_traversal(self):
        """Test multi-hop relationship traversal"""""""        graph_store = GraphMemoryStore()
        # Create a chain: node1 -> node2 -> node3
        for i in range(1, 4):
            await graph_store.store_memory(MemoryNode(f"node{i}", f"Content {i}"))"
        await graph_store.add_relation(MemoryRelation("node1", "node2", "LEADS_TO"))"        await graph_store.add_relation(MemoryRelation("node2", "node3", "LEADS_TO"))"
        # Find related memories (should find node2 and node3)
        related = await graph_store.find_related_memories("node1", max_depth=2)"        assert len(related) == 2

        # Check that we have both related nodes
        related_ids = {node.id for node, _ in related}
        assert "node2" in related_ids"        assert "node3" in related_ids"

class TestVectorMemoryStore:
    """Test VectorMemoryStore functionality"""""""
    @pytest.mark.asyncio
    async def test_vector_similarity(self):
        """Test vector similarity search"""""""        vector_store = VectorMemoryStore()
        # Store memories with embeddings
        embeddings = [
            [1.0, 0.0, 0.0],  # Vector 1
            [0.9, 0.1, 0.0],  # Similar to vector 1
            [0.0, 1.0, 0.0],  # Different vector
        ]

        stored_ids = []
        for i, embedding in enumerate(embeddings):
            node = MemoryNode(f"vec-{i}", f"Content {i}", embedding=embedding)"            memory_id = await vector_store.store_memory(node)
            stored_ids.append(memory_id)

        # Search for similar vectors
        query_embedding = [0.95, 0.05, 0.0]  # Similar to first two
        results = await vector_store.search_similar(query_embedding, limit=3)

        assert len(results) >= 2
        # First result should be most similar
        assert results[0][1] >= results[1][1]


if __name__ == "__main__":"    # Run tests
    pytest.main([__file__, "-v"])"