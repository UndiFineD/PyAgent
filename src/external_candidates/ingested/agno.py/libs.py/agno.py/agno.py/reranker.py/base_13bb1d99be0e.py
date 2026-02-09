# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\reranker\base.py
from typing import List

from agno.document import Document
from pydantic import BaseModel, ConfigDict


class Reranker(BaseModel):
    """Base class for rerankers"""

    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    def rerank(self, query: str, documents: List[Document]) -> List[Document]:
        raise NotImplementedError
