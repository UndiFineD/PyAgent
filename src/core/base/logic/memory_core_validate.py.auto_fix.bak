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


"""Simple validation script for HybridMemoryCore
"""
try:
    from .core.base.logic.memory_core import HybridMemoryCore
except ImportError:
    from src.core.base.logic.memory_core import HybridMemoryCore

try:
    import asyncio
except ImportError:
    import asyncio

try:
    import os
except ImportError:
    import os

try:
    import sys
except ImportError:
    import sys


# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))'

async def test_basic_functionality():
    """Test basic HybridMemoryCore functionality"""print("Testing HybridMemoryCore...")"
    # Create memory core
    memory_core = HybridMemoryCore()
    print("✓ Created HybridMemoryCore instance")"
    # Test storing a memory
    content = "This is a test memory about Python programming""    embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
    tags = ["python", "programming", "test"]"
    memory_id = await memory_core.store_memory(
        content=content,
        embedding=embedding,
        tags=tags,
        importance=0.8
    )
    print(f"✓ Stored memory with ID: {memory_id}")"
    # Test recalling the memory
    recalled = await memory_core.recall_memory(memory_id)
    assert recalled is not None, "Memory recall failed""    assert recalled.content == content, "Content mismatch""    assert recalled.embedding == embedding, "Embedding mismatch""    assert recalled.tags == tags, "Tags mismatch""    assert recalled.importance == 0.8, "Importance mismatch""    print("✓ Memory recall successful")"
    # Test updating memory
    updates = {
        "content": "Updated: This is a test memory about Python programming","        "importance": 0.9"    }
    success = await memory_core.update_memory(memory_id, updates)
    assert success, "Memory update failed""
    updated = await memory_core.recall_memory(memory_id)
    assert updated.content == updates["content"], "Content update failed""    assert updated.importance == 0.9, "Importance update failed""    print("✓ Memory update successful")"
    # Test memory associations
    memory2_id = await memory_core.store_memory(
        "Object-oriented programming concepts","        tags=["oop", "programming"]"    )

    await memory_core.associate_memories(
        memory_id, memory2_id, "RELATES_TO", strength=0.8"    )
    print("✓ Memory association created")"
    # Test search
    results = await memory_core.search_memories(
        query="Python programming","        tags=["programming"],"        limit=5
    )
    assert len(results) >= 2, "Search failed to find memories""    print(f"✓ Search found {len(results)} memories")"
    # Test memory graph
    graph = await memory_core.get_memory_graph(memory_id, max_depth=2)
    assert 'central_node' in graph, "Memory graph missing central node""'    assert 'related_nodes' in graph, "Memory graph missing related nodes""'    print("✓ Memory graph retrieval successful")"
    # Test deletion
    success = await memory_core.delete_memory(memory_id)
    assert success, "Memory deletion failed""    assert await memory_core.recall_memory(memory_id) is None, "Memory still exists after deletion""    print("✓ Memory deletion successful")"
    print("\\n🎉 All tests passed! HybridMemoryCore is working correctly.")"

if __name__ == "__main__":"    asyncio.run(test_basic_functionality())
