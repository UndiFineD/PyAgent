#!/usr/bin/env python3

"""GraphRelationalAgent for PyAgent.
Implements hybrid indexing using vector embeddings and structured knowledge graphs.
Focuses on tracking entity relationships (e.g., Agent -> depends_on -> Tool).
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool

class GraphRelationalAgent(BaseAgent):
    """Hybrid RAG agent combining Graph-based relationships and Vector search."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.graph_store_path = Path("agent_store/knowledge_graph.json")
        self.entities: Dict[str, Dict[str, Any]] = {}
        self.relations: List[Dict[str, str]] = []
        self._load_graph()
        self._system_prompt = (
            "You are the Graph Relational Agent. You map structured dependencies and "
            "relationships across the fleet workspace. You excel at answering structural "
            "questions about how components interact."
        )

    def _load_graph(self) -> None:
        if self.graph_store_path.exists():
            try:
                with open(self.graph_store_path, "r") as f:
                    data = json.load(f)
                    self.entities = data.get("entities", {})
                    self.relations = data.get("relations", [])
            except Exception as e:
                logging.error(f"GraphRelationalAgent: Failed to load graph: {e}")

    def _save_graph(self) -> None:
        try:
            self.graph_store_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.graph_store_path, "w") as f:
                json.dump({"entities": self.entities, "relations": self.relations}, f, indent=4)
        except Exception as e:
            logging.error(f"GraphRelationalAgent: Failed to save graph: {e}")

    @as_tool
    def add_entity(self, name: str, entity_type: str, properties: Optional[Dict[str, Any]] = None) -> str:
        """Adds a node to the knowledge graph."""
        self.entities[name] = {"type": entity_type, "properties": properties or {}}
        self._save_graph()
        return f"Entity '{name}' ({entity_type}) added to graph."

    @as_tool
    def add_relation(self, source: str, relation_type: str, target: str) -> str:
        """Adds a directed edge between two entities."""
        if source not in self.entities or target not in self.entities:
            return f"Error: Source '{source}' or Target '{target}' not in graph."
        
        rel = {"source": source, "type": relation_type, "target": target}
        if rel not in self.relations:
            self.relations.append(rel)
            self._save_graph()
        return f"Relation '{source}' --[{relation_type}]--> '{target}' established."

    @as_tool
    def query_relationships(self, entity_name: str) -> List[Dict[str, str]]:
        """Finds all relationships for a given entity."""
        return [r for r in self.relations if r["source"] == entity_name or r["target"] == entity_name]

    @as_tool
    def hybrid_search(self, query: str) -> Dict[str, Any]:
        """Performs a combined vector-graph search (Simulated)."""
        # In a real system, this would call ChromaDB for vectors and then cross-reference with self.entities
        return {
            "query": query,
            "vector_results": ["Related code snippet from src/classes/base_agent.py"],
            "graph_context": self.query_relationships(query) if query in self.entities else "No direct graph matches."
        }

    def improve_content(self, input_text: str) -> str:
        return f"Graph currently holds {len(self.entities)} entities and {len(self.relations)} relations."

if __name__ == "__main__":
    from src.classes.base_agent.utilities import create_main_function
    main = create_main_function(GraphRelationalAgent, "Graph Relational Agent", "Hybrid knowledge graph RAG")
    main()
