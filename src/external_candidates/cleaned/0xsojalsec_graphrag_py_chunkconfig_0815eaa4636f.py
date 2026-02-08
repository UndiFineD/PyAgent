# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_graphrag.py\config.py\chunkconfig_0815eaa4636f.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-GraphRAG\Config\ChunkConfig.py

from Core.Utils.YamlModel import YamlModel


class ChunkConfig(YamlModel):
    chunk_token_size: int = 1200

    chunk_overlap_token_size: int = 100

    chunk_method: str = "chunking_by_token_size"
