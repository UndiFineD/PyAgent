# Extracted from: C:\DEV\PyAgent\.external\EvoAgentX\evoagentx\rag\retrievers\base.py
import logging
from abc import ABC, abstractmethod
from enum import Enum

from llama_index.core.retrievers import BaseRetriever

from ..schema import Query, RagResult


class RetrieverType(str, Enum):
    VECTOR = "vector"
    GRAPH = "graph"


class BaseRetrieverWrapper(ABC):
    """Base interface for retriever wrappers."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def retrieve(self, query: Query) -> RagResult:
        """Retrieve results for a query."""
        pass

    @abstractmethod
    def get_retriever(self) -> BaseRetriever:
        """Return the LlamaIndex-compatible retriever."""
        pass
