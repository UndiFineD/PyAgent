# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\decodingai_magazine_second_brain_ai_assistant_course.py\workshops.py\rag.py\solution.py\src.py\rag_workshop.py\embeddings_cad572639fe5.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\decodingai-magazine-second-brain-ai-assistant-course\workshops\rag\solution\src\rag_workshop\embeddings.py

from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model(
    model_id: str,
    device: str = "cpu",
) -> HuggingFaceEmbeddings:
    """Gets an instance of the HuggingFace embedding model.



    Args:

        model_id (str): The ID/name of the HuggingFace embedding model to use

        device (str, optional): The device to use for the embedding model. Defaults to "cpu"



    Returns:

        HuggingFaceEmbeddings: A HuggingFace embedding model instance

    """

    return HuggingFaceEmbeddings(
        model_name=model_id,
        model_kwargs={"device": device, "trust_remote_code": True},
        encode_kwargs={"normalize_embeddings": False},
    )
