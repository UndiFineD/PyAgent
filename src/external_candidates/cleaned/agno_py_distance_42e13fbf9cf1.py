# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\agno.py\agno.py\vectordb.py\distance_42e13fbf9cf1.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\vectordb\distance.py

from enum import Enum

class Distance(str, Enum):

    cosine = "cosine"

    l2 = "l2"

    max_inner_product = "max_inner_product"

