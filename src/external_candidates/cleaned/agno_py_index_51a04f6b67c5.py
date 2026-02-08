# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\agno.py\agno.py\vectordb.py\clickhouse.py\index_51a04f6b67c5.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\vectordb\clickhouse\index.py

from typing import Literal

from pydantic import BaseModel


class HNSW(BaseModel):
    quantization: Literal["f64", "f32", "f16", "bf16", "i8"] = "bf16"

    hnsw_max_connections_per_layer: int = 32

    hnsw_candidate_list_size_for_construction: int = 128
