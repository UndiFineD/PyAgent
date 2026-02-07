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
