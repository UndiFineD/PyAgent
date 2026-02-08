# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentkit.py\backend.py\app.py\tests.py\fake.py\vector_db_1b4d5407ea11.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentkit\backend\app\tests\fake\vector_db.py

# -*- coding: utf-8 -*-

from typing import List

from langchain.schema import Document

from langchain.vectorstores import VectorStore


class FakeVectorDB(VectorStore):
    docs: List[Document]

    def __init__(self, *args, **kwargs):
        self.docs = kwargs.get("docs", [])

    def add_texts(self):
        pass

    @classmethod
    def from_texts(cls):
        pass

    @classmethod
    def from_documents(cls, docs: List[Document]):
        return cls(docs=docs)

    def similarity_search(self, query: str, k: int = 1, **kwargs) -> List[Document]:
        return self.docs[:k]
