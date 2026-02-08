# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\decodingai_magazine_second_brain_ai_assistant_course.py\workshops.py\rag.py\template.py\src.py\rag_workshop.py\splitters_b8afb171c578.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\decodingai-magazine-second-brain-ai-assistant-course\workshops\rag\template\src\rag_workshop\splitters.py

from langchain_text_splitters import RecursiveCharacterTextSplitter

from loguru import logger


def get_splitter(
    chunk_size: int,
) -> RecursiveCharacterTextSplitter:
    """Returns a token-based text splitter with overlap.



    Args:

        chunk_size: Number of tokens for each text chunk.



    Returns:

        RecursiveCharacterTextSplitter: A configured text splitter instance that splits text

            into chunks with 15% overlap between consecutive chunks.

    """

    chunk_overlap = int(0.15 * chunk_size)

    logger.info(f"Getting splitter with chunk size: {chunk_size} and overlap: {chunk_overlap}")

    # TODO: Implement splitter

    return splitter
