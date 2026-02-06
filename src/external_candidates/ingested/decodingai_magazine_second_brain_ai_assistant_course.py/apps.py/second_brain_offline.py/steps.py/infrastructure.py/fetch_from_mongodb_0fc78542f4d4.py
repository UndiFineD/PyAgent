# Extracted from: C:\DEV\PyAgent\.external\decodingai-magazine-second-brain-ai-assistant-course\apps\second-brain-offline\steps\infrastructure\fetch_from_mongodb.py
from second_brain_offline.domain import Document
from second_brain_offline.infrastructure.mongo import MongoDBService
from typing_extensions import Annotated
from zenml.steps import get_step_context, step


@step
def fetch_from_mongodb(
    collection_name: str,
    limit: int,
) -> Annotated[list[dict], "documents"]:
    with MongoDBService(model=Document, collection_name=collection_name) as service:
        documents = service.fetch_documents(limit, query={})

    step_context = get_step_context()
    step_context.add_output_metadata(
        output_name="documents",
        metadata={
            "count": len(documents),
        },
    )

    return documents
