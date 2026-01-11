import hashlib
from .storage_base import KnowledgeStore
from typing import Any, Dict, List, Optional
import json
from pathlib import Path

class GraphKnowledgeStore(KnowledgeStore):
    """
    Sharded Graph storage for relational and ontological knowledge.
    Scales to trillions of triples by sharding nodes across the filesystem.
    """
    
    def _hash_node(self, node_id: str) -> str:
        return hashlib.md5(node_id.encode()).hexdigest()

    def _get_node_path(self, node_id: str) -> Path:
        """Hierarchical Sharding for Graph Nodes (Phase 130)."""
        hash_val = self._hash_node(node_id)
        tier1 = hash_val[:2]
        tier2 = hash_val[2:4]
        
        shard_dir = self.storage_path / tier1 / tier2
        shard_dir.mkdir(exist_ok=True, parents=True)
        return shard_dir / f"{node_id}.json"

    def store(self, node: str, target: Any, relationship: str = "related_to") -> bool:
        path = self._get_node_path(node)
        
        if path.exists():
            with open(path, "r") as f:
                data = json.load(f)
        else:
            data = {"id": node, "edges": []}
            
        data["edges"].append({"to": target, "type": relationship})
        
        with open(path, "w") as f:
            json.dump(data, f)
        return True

    def retrieve(self, node: str, limit: int = 5) -> List[Any]:
        path = self._get_node_path(node)
        if path.exists():
            with open(path, "r") as f:
                return json.load(f).get("edges", [])[:limit]
        return []

    def delete(self, node: str) -> bool:
        path = self._get_node_path(node)
        if path.exists():
            path.unlink()
            return True
        return False
