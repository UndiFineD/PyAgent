from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pathlib import Path

class KnowledgeStore(ABC):
    """Base interface for all knowledge storage types."""
    
    def __init__(self, agent_id: str, storage_path: Path) -> None:
        self.agent_id = agent_id
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def store(self, key: str, value: Any, metadata: Optional[Dict[str, Any]] = None) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def retrieve(self, query: Any, limit: int = 5) -> List[Any]:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, key: str) -> bool:
        raise NotImplementedError()
