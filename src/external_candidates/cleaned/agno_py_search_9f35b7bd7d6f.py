# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\agno.py\agno.py\vectordb.py\search_9f35b7bd7d6f.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\vectordb\search.py

from enum import Enum

class SearchType(str, Enum):

    vector = "vector"

    keyword = "keyword"

    hybrid = "hybrid"

