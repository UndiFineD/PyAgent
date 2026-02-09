# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\vectordb\distance.py
from enum import Enum


class Distance(str, Enum):
    cosine = "cosine"
    l2 = "l2"
    max_inner_product = "max_inner_product"
