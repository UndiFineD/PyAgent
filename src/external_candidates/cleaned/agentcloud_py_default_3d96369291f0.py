# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentcloud.py\agent_backend.py\src.py\tools.py\retrievers.py\default_3d96369291f0.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\tools\retrievers\default.py

from langchain_core.embeddings import Embeddings

from langchain_core.vectorstores import VectorStore

from models.mongo import Tool

from .base import BaseToolRetriever

from .callback_handler import RetrieverCallbackHandler

from .similarity_search import SimilaritySearchRetriever


class DefaultRetriever(BaseToolRetriever):
    def __init__(self, tool: Tool, embedding: Embeddings, vector_store: VectorStore):

        self.tool = tool

        self.retriever = SimilaritySearchRetriever(
            embedding=embedding,
            vector_store=vector_store,
            k=tool.retriever_config.k,
            rag_filters=tool.ragFilters or {},
        )

        super().__init__()
