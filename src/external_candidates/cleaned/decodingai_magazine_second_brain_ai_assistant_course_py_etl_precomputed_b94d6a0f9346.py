# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\decodingai_magazine_second_brain_ai_assistant_course.py\apps.py\second_brain_offline.py\pipelines.py\etl_precomputed_b94d6a0f9346.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\decodingai-magazine-second-brain-ai-assistant-course\apps\second-brain-offline\pipelines\etl_precomputed.py

from pathlib import Path

from steps.infrastructure import ingest_to_mongodb, read_documents_from_disk

from zenml import pipeline


@pipeline
def etl_precomputed(
    data_dir: Path,
    load_collection_name: str,
) -> None:
    crawled_data_dir = data_dir / "crawled"

    documents = read_documents_from_disk(data_directory=crawled_data_dir, nesting_level=0)

    ingest_to_mongodb(
        models=documents,
        collection_name=load_collection_name,
        clear_collection=True,
    )
