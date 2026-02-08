# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\acontext.py\src.py\server.py\core.py\acontext_core.py\schema.py\embedding_ad353af7565d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\schema\embedding.py

import numpy as np

from pydantic import BaseModel, ConfigDict


class EmbeddingReturn(BaseModel):
    embedding: np.ndarray

    prompt_tokens: int

    total_tokens: int

    model_config = ConfigDict(arbitrary_types_allowed=True)
