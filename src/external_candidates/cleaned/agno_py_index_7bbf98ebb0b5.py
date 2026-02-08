# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\agno.py\agno.py\vectordb.py\pgvector.py\index_7bbf98ebb0b5.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\vectordb\pgvector\index.py

from typing import Any, Dict, Optional

from pydantic import BaseModel

class Ivfflat(BaseModel):

    name: Optional[str] = None

    lists: int = 100

    probes: int = 10

    dynamic_lists: bool = True

    configuration: Dict[str, Any] = {

        "maintenance_work_mem": "2GB",

    }

class HNSW(BaseModel):

    name: Optional[str] = None

    m: int = 16

    ef_search: int = 5

    ef_construction: int = 200

    configuration: Dict[str, Any] = {

        "maintenance_work_mem": "2GB",

    }

