# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\decodingai_magazine_second_brain_ai_assistant_course.py\apps.py\second_brain_offline.py\src.py\second_brain_offline.py\infrastructure.py\mongo.py\indexes_a750de0111f1.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\decodingai-magazine-second-brain-ai-assistant-course\apps\second-brain-offline\src\second_brain_offline\infrastructure\mongo\indexes.py

from langchain_mongodb.index import create_fulltext_search_index

from second_brain_offline.infrastructure.mongo.service import MongoDBService


class MongoDBIndex:
    def __init__(
        self,
        retriever,
        mongodb_client: MongoDBService,
    ) -> None:
        self.retriever = retriever

        self.mongodb_client = mongodb_client

    def create(
        self,
        embedding_dim: int,
        is_hybrid: bool = False,
    ) -> None:
        vectorstore = self.retriever.vectorstore

        vectorstore.create_vector_search_index(
            dimensions=embedding_dim,
        )

        if is_hybrid:
            create_fulltext_search_index(
                collection=self.mongodb_client.collection,
                field=vectorstore._text_key,
                index_name=self.retriever.search_index_name,
            )
