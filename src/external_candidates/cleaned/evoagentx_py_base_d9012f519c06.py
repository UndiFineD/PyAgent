# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\evoagentx.py\evoagentx.py\storages.py\vectore_stores.py\base_d9012f519c06.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\EvoAgentX\evoagentx\storages\vectore_stores\base.py

from abc import ABC, abstractmethod

from enum import Enum


from llama_index.core.vector_stores.types import BasePydanticVectorStore


class VectorStoreType(str, Enum):
    FAISS = "faiss"


class VectorStoreBase(ABC):
    """Base interface for vector stores."""

    @abstractmethod
    def get_vector_store(self) -> BasePydanticVectorStore:
        """Return the LlamaIndex-compatible vector store."""

        pass

    @abstractmethod
    async def aload(self):
        """Asynchronously load a single node into the vector store."""

        pass
