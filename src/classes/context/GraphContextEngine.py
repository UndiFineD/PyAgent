#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Core engine for managing code relationships as a graph."""

from __future__ import annotations
from src.core.base.version import VERSION
import json
import logging
from pathlib import Path
from typing import Dict, Set, Any, Optional
from src.logic.agents.cognitive.context.engines.GraphCore import GraphCore

__version__ = VERSION

class GraphContextEngine:
    """Manages an adjacency list of file and class dependencies."""
    
    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.graph: dict[str, set[str]] = {}
        self.metadata: dict[str, Any] = {}
        self.symbols: dict[str, Any] = {}
        self.persist_file = self.workspace_root / ".agent_graph.json"
        self.core = GraphCore()
        self.load()

    def add_edge(self, source: str, target: str, relationship: str = "imports") -> None:
        """Add a directed edge to the graph."""
        if source not in self.graph:
            self.graph[source] = set()
        self.graph[source].add(target)
        # Store metadata
        key = f"{source}->{target}"
        self.metadata[key] = {"type": relationship}

    def scan_project(self, start_path: Path | None = None) -> None:
        """Scans files using AST to build a detailed relationship graph."""
        target = start_path or self.workspace_root
        logging.info(f"Scanning project graph from {target}")
        
        for py_file in target.rglob("*.py"):
            if any(p in str(py_file) for p in [".venv", "__pycache__", ".git"]):
                continue
            
            rel_path = str(py_file.relative_to(self.workspace_root))
            try:
                content = py_file.read_text(encoding="utf-8")
                analysis = self.core.parse_python_content(rel_path, content)
                
                # Store symbol info
                self.symbols[rel_path] = {
                    "classes": analysis["classes"],
                    "inherits": analysis["inherits"],
                    "calls": analysis["calls"]
                }

                # Build and add edges
                edges = self.core.build_edges(analysis)
                for source, target, rel in edges:
                    self.add_edge(source, target, rel)

            except Exception as e:
                logging.error(f"GraphContextEngine: Failed to scan {rel_path}: {e}")
        
        self.save()

    def get_impact_radius(self, node: str, max_depth: int = 3) -> set[str]:
        """Find all nodes that depend on the given node (inverse of graph)."""
        affected = set()
        to_visit = [(node, 0)]
        visited = {node}
        
        inverse_graph: dict[str, set[str]] = {}
        for src, targets in self.graph.items():
            for t in targets:
                if t not in inverse_graph:
                    inverse_graph[t] = set()
                inverse_graph[t].add(src)
        
        while to_visit:
            curr, depth = to_visit.pop(0)
            if depth >= max_depth:
                continue
                
            for depender in inverse_graph.get(curr, set()):
                if depender not in visited:
                    visited.add(depender)
                    affected.add(depender)
                    to_visit.append((depender, depth + 1))
                    
        return affected

    def save(self) -> None:
        """Serialize graph to disk."""
        data = {
            "graph": {k: list(v) for k, v in self.graph.items()},
            "metadata": self.metadata,
            "symbols": self.symbols
        }
        with open(self.persist_file, "w") as f:
            json.dump(data, f, indent=2)

    def load(self) -> None:
        """Load graph from disk."""
        if self.persist_file.exists():
            try:
                with open(self.persist_file) as f:
                    data = json.load(f)
                self.graph = {k: set(v) for k, v in data.get("graph", {}).items()}
                self.metadata = data.get("metadata", {})
                self.symbols = data.get("symbols", {})
            except Exception as e:
                logging.error(f"Error loading graph: {e}")