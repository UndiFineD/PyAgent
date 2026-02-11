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

import asyncio
from src.core.base.logic.core.rag_core import RAGCore, Document, VectorStoreType

async def run():
    core = RAGCore()
    await core.register_vector_store("test_store", VectorStoreType.QDRANT, {})
    await core.create_rag_tool(
        tool_id="test_tool",
        name="Test Tool",
        description="Test",
        vector_store_id="test_store",
        collection_name="test_store",
        chunk_size=50,
        chunk_overlap=10
    )

    long_content = "This is a very long document that should be chunked into smaller pieces. " * 10
    document = Document(
        doc_id="long_doc",
        content=long_content,
        metadata={"author": "test"}
    )

    doc_ids = await core.add_documents("test_tool", [document], chunk_documents=True)
    print('doc_ids:', doc_ids)

asyncio.run(run())
