#!/usr/bin/env python3

"""Agent that maps the codebase into a graph of relationships."""

from src.classes.base_agent import BaseAgent
from .GraphContextEngine import GraphContextEngine
import logging
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

class NetworkContextAgent(BaseAgent):
    """Scans the codebase to build a graph of imports and class hierarchies."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.engine = GraphContextEngine(str(self.file_path.parent))
        self.graph_file = self.file_path.parent / ".agent_code_graph.json"
        
        self._system_prompt = (
            "You are the Network Context Agent (Graph Specialist). "
            "Internalize the codebase as a graph where nodes are files/classes and edges are relationships. "
            "You identify tightly coupled clusters and suggest separation of concerns."
        )

    def _get_default_content(self) -> str:
        return "# Codebase Network Analysis\n\n## Clusters\nPending scan...\n"

    def scan_project(self) -> str:
        """Perform a full scan of the project to build the graph."""
        root = self.file_path.parent
        
        # 1. Discover all python files as nodes
        py_files = []
        for p in root.rglob("*.py"):
            if any(part in str(p) for part in ["__pycache__", "venv", ".git", ".agent_cache"]):
                continue
            rel_path = str(p.relative_to(root))
            self.engine.add_node(rel_path, "file")
            py_files.append(p)

        # 2. Extract relationships (imports and class inheritance)
        for p in py_files:
            rel_path = str(p.relative_to(root))
            try:
                content = p.read_text(encoding="utf-8")
                
                # Find imports (from ... import ... or import ...)
                # Simple regex for module names
                imports = re.findall(r"^(?:from|import)\s+([\w\.]+)", content, re.MULTILINE)
                for imp in imports:
                    # Clean up dots to find potential local files
                    # e.g. from .classes.agent import Agent -> classes.agent
                    clean_imp = imp.lstrip('.')
                    potential_path = clean_imp.replace('.', '/') + ".py"
                    
                    # Search for this module in our known files
                    for other_rel in self.engine.graph.keys():
                        if potential_path in other_rel or other_rel.replace('\\', '/') in potential_path:
                            self.engine.add_edge(rel_path, other_rel, "imports")

                # Find Class hierarchy
                classes = re.findall(r"class\s+(\w+)(?:\(([\w,\s\.]+)\))?:", content)
                for cls_name, bases in classes:
                    cls_id = f"{rel_path}:{cls_name}"
                    self.engine.add_node(cls_id, "class", {"file": rel_path})
                    self.engine.add_edge(rel_path, cls_id, "contains")
                    
                    if bases:
                        for base in bases.split(','):
                            base = base.strip()
                            # Try to find the base class in same file or imports
                            # (Heuristic: search matching class names)
                            self.engine.add_edge(cls_id, f"base:{base}", "inherits")

            except Exception as e:
                logging.error(f"Scan error for {p}: {e}")

        self.engine.save(str(self.graph_file))
        logging.info(f"Scan complete. Graph saved to {self.graph_file}.")

    def analyze_impact(self, file_path: str) -> str:
        """Analyze the impact of changing a specific file."""
        self.engine.load(str(self.graph_file))
        rel_path = os.path.relpath(file_path, self.file_path.parent)
        
        impacted_nodes = self.engine.get_transitive_neighbors(rel_path, depth=3)
        
        report = [f"## Impact Analysis for {rel_path}"]
        if not impacted_nodes:
            report.append("No direct downstream dependencies found in the graph.")
        else:
            report.append(f"Found {len(impacted_nodes)} potentially impacted entities within 3 hops:")
            for node in sorted(list(impacted_nodes)):
                meta = self.engine.metadata.get(node, {})
                node_type = meta.get("type", "unknown")
                report.append(f"- **{node}** ({node_type})")
                
        return "\n".join(report)
