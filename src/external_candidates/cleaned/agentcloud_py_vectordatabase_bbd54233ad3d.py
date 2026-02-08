# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentcloud.py\agent_backend.py\src.py\models.py\vectordatabase_bbd54233ad3d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\models\vectordatabase.py

from enum import Enum


class VectorDatabase(str, Enum):
    Qdrant = "qdrant"

    Pinecone = "pinecone"
