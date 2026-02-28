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
