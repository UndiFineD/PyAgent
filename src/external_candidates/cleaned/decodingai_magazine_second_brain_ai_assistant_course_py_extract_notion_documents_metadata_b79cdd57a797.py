# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\decodingai_magazine_second_brain_ai_assistant_course.py\apps.py\second_brain_offline.py\steps.py\collect_notion_data.py\extract_notion_documents_metadata_b79cdd57a797.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\decodingai-magazine-second-brain-ai-assistant-course\apps\second-brain-offline\steps\collect_notion_data\extract_notion_documents_metadata.py

from loguru import logger

from second_brain_offline.domain import DocumentMetadata

from second_brain_offline.infrastructure.notion import NotionDatabaseClient

from typing_extensions import Annotated

from zenml import get_step_context, step


@step
def extract_notion_documents_metadata(
    database_id: str,
) -> Annotated[list[DocumentMetadata], "notion_documents_metadata"]:
    """Extract metadata from Notion documents in a specified database.

    Args:

        database_id: The ID of the Notion database to query.

    Returns:

        A list of DocumentMetadata objects containing the extracted information.

    """

    client = NotionDatabaseClient()

    documents_metadata = client.query_notion_database(database_id)

    logger.info(f"Extracted {len(documents_metadata)} documents metadata from {database_id}")

    step_context = get_step_context()

    step_context.add_output_metadata(
        output_name="notion_documents_metadata",
        metadata={
            "database_id": database_id,
            "len_documents_metadata": len(documents_metadata),
        },
    )

    return documents_metadata
