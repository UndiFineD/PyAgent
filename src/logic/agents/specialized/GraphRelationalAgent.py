from __future__ import annotations
from typing import Any, List, Dict
from src.core.base.BaseAgent import BaseAgent
from src.core.base.BaseUtilities import as_tool


class GraphRelationalAgent(BaseAgent):
    """
    GraphRelationalAgent for PyAgent.
    Implements hybrid indexing using vector embeddings and structured knowledge graphs.
    """

    def __init__(self, workspace_root: str) -> None:
        super().__init__(workspace_root)
        self.entities: Dict[str, Any] = {}
        self.relations: List[Dict[str, Any]] = []

    @as_tool
    async def add_entity(
        self, name: str, type_: str, props: Dict[str, Any] = None
    ) -> str:
        if props is None:
            props = {}
        self.entities[name] = {"type": type_, "props": props}
        return f"Entity {name} established"

    @as_tool
    async def add_relation(self, source: str, type_: str, target: str) -> str:
        self.relations.append({"source": source, "type": type_, "target": target})
        return f"Relation {source}->{target} established"

    @as_tool
    async def query_relationships(self, source: str) -> List[Dict[str, Any]]:
        return [r for r in self.relations if r["source"] == source]
