# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\models\vectordatabase.py
from enum import Enum


class VectorDatabase(str, Enum):
    Qdrant = "qdrant"
    Pinecone = "pinecone"
