# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_graphrag.py\config.py\embconfig_4cbee1be00f1.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-GraphRAG\Config\EmbConfig.py

from enum import Enum

from typing import Optional

from pydantic import field_validator

from Core.Utils.YamlModel import YamlModel


class EmbeddingType(Enum):
    OPENAI = "openai"

    HF = "hf"

    OLLAMA = "ollama"


class EmbeddingConfig(YamlModel):
    """Option for Embedding.

    Examples:

    ---------

    """

    api_type: Optional[EmbeddingType] = None

    api_key: Optional[str] = None

    base_url: Optional[str] = None

    api_version: Optional[str] = None

    model: Optional[str] = None

    cache_folder: Optional[str] = None

    embed_batch_size: Optional[int] = None

    dimensions: Optional[int] = None  # output dimension of embedding model

    @field_validator("api_type", mode="before")
    @classmethod
    def check_api_type(cls, v):
        if v == "":
            return None

        return v
