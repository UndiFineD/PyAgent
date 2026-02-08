# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\agno.py\agno.py\vectordb.py\weaviate.py\index_637f3d8c21d4.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\vectordb\weaviate\index.py

from enum import Enum


class VectorIndex(Enum):
    HNSW = "hnsw"

    FLAT = "flat"

    DYNAMIC = "dynamic"


class Distance(Enum):
    COSINE = "cosine"

    DOT = "dot"

    L2_SQUARED = "l2-squared"

    HAMMING = "hamming"

    MANHATTAN = "manhattan"
