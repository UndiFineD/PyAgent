from __future__ import annotations

from typing import Dict, Any, List

class BlackboardCore:
    """
    Pure logic for Blackboard operations.
    Handles data indexing and history tracking.
    """
    def __init__(self) -> None:
        self.data: Dict[str, Any] = {}
        self.history: List[Dict[str, Any]] = []

    def process_post(self, key: str, value: Any, agent_name: str) -> Dict[str, Any]:
        """Core logic for posting data."""
        self.data[key] = value
        entry = {"agent": agent_name, "key": key, "value": value}
        self.history.append(entry)
        return entry

    def get_value(self, key: str) -> Any:
        return self.data.get(key)

    def get_all_keys(self) -> List[str]:
        return list(self.data.keys())
