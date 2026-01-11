from .storage_base import KnowledgeStore
from typing import Any, Dict, List, Optional
import os

class VectorKnowledgeStore(KnowledgeStore):
    """
    Handles vector-based knowledge storage using ChromaDB.
    Isolated per agent.
    """
    
    def __init__(self, agent_id: str, storage_path: Any) -> None:
        super().__init__(agent_id, storage_path)
        try:
            import chromadb
            self.client = chromadb.PersistentClient(path=str(self.storage_path))
            self.collection = self.client.get_or_create_collection(name=f"{agent_id}_knowledge")
        except ImportError:
            self.client = None
            print("ChromaDB not installed, VectorKnowledgeStore will be disabled.")

    def store(self, key: str, value: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        if not self.client: return False
        self.collection.add(
            documents=[value],
            metadatas=[metadata] if metadata else [{}],
            ids=[key]
        )
        return True

    def retrieve(self, query: str, limit: int = 5) -> List[Any]:
        if not self.client: return []
        results = self.collection.query(
            query_texts=[query],
            n_results=limit
        )
        return results.get("documents", [[]])[0]

    def delete(self, key: str) -> bool:
        if not self.client: return False
        self.collection.delete(ids=[key])
        return True
