# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\vectordb\search.py
from enum import Enum


class SearchType(str, Enum):
    vector = "vector"
    keyword = "keyword"
    hybrid = "hybrid"
