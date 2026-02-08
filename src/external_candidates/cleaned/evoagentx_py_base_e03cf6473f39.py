# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\evoagentx.py\evoagentx.py\rag.py\chunkers.py\base_e03cf6473f39.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\EvoAgentX\evoagentx\rag\chunkers\base.py

from abc import ABC, abstractmethod

from enum import Enum

from typing import List


from evoagentx.rag.schema import Corpus, Document


class ChunkingStrategy(str, Enum):
    SIMPLE = "simple"

    SEMANTIC = "semantic"

    HIERARCHICAL = "hierarchical"


class BaseChunker(ABC):
    """Abstract base class for chunking documents into smaller segments.



    This class defines the interface for chunking strategies in the RAG pipeline,

    converting Documents into a Corpus of Chunks.

    """

    @abstractmethod
    def chunk(self, documents: List[Document], **kwargs) -> Corpus:
        """Chunk documents into a Corpus of Chunks.



        Args:

            documents (List[Document]): List of Document objects to chunk.

            **kwargs: Additional parameters specific to the chunking strategy.



        Returns:

            Corpus: A collection of Chunk objects.

        """

        pass
