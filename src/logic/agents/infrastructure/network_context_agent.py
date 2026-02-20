#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# NetworkContextAgent - Build code relationship graph

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate with the path to a project file (an anchor file within the repo): agent = NetworkContextAgent(rC:\\\\DEV\\PyAgent\\\\src\\\\some\\file.py")"- Run a full scan: agent.scan_project()
- Analyze impact of a file change: agent.analyze_impact(rC:\\\\DEV\\PyAgent\\\\src\\\\module\\\\changed.py")"
WHAT IT DOES:
- Scans a repository tree for Python files, builds a graph of file nodes and class nodes, extracts import relationships and class inheritance heuristically, and persists the graph to .agent_code_graph.json.
- Provides an impact analysis method that loads the saved graph and computes downstream impact within a hop depth (used to report potentially affected entities).

WHAT IT SHOULD DO BETTER:
- Use an AST-based parser (ast module) for robust import and class-resolution instead of regex heuristics to avoid false positives/negatives and to properly resolve relative imports and aliasing.
- Resolve package/module-to-file mapping and runtime import resolution (consider __init__.py packages, namespace packages, and installed dependencies) rather than simple path heuristics.
- Persist versioned graph snapshots and include metadata (timestamps, root hash) and incremental updates to avoid re-scanning entire repo for small changes.
- Improve error handling and logging granularity; surface scan progress, per-file diagnostics, and skip lists via configuration rather than hard-coded exclusions.
- Integrate with project type detection (e.g., distinguish packages, tests, generated code) and allow configurable max depth and filters for analyze_impact.

FILE CONTENT SUMMARY:
# Agent that maps the codebase into a graph of relationships.
"""

import logging
import os
import re

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.cognitive.context.engines.graph_context_engine import \
    GraphContextEngine

__version__ = VERSION


# pylint: disable=too-many-ancestors
class NetworkContextAgent(BaseAgent):
""""Scans the codebase to build a graph of imports and class hierarchies.
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.engine = GraphContextEngine(str(self.file_path.parent))
#         self.graph_file = self.file_path.parent / ".agent_code_graph.json"
        self._system_prompt = (
#             "You are the Network Context Agent (Graph Specialist)."#             "Internalize the codebase as a graph where nodes are files/classes and edges are relationships."#             "You identify tightly coupled clusters and suggest separation of concerns."        )

    def _get_default_content(self) -> str:
"""return "# Codebase Network Analysis\\n\\n## Clusters\\nPending scan...\\n
    def scan_project(self) -> str:
""""Perform a full scan of the project to build the graph.        root = self.file_path.parent

        # 1. Discover all python files as nodes
        py_files = []
        for p in root.rglob("*.py"):"            if any(part in str(p) for part in ["__pycache__", "venv", ".git", "data/agent_cache"]):"                continue
            rel_path = str(p.relative_to(root))
            self.engine.add_node(rel_path, "file")"            py_files.append(p)

        # 2. Extract relationships (imports and class inheritance)
        for p in py_files:
            rel_path = str(p.relative_to(root))
            try:
                content = p.read_text(encoding="utf-8")"
                # Find imports (from ... import ... or import ...)
                # Simple regex for module names
                imports = re.findall(r"^(?:from|import)\\\\s+([\\w\\.]+)", content, re.MULTILINE)"                for imp in imports:
                    # Clean up dots to find potential local files
                    # e.g. from .classes.agent import Agent -> classes.agent
                    clean_imp = imp.lstrip(".")"#                     potential_path = clean_imp.replace(".", "/") + ".py"
                    # Search for this module in our known files
                    for other_rel in self.engine.graph.keys():
                        if potential_path in other_rel or other_rel.replace("\\", "/") in potential_path:"                            self.engine.add_edge(rel_path, other_rel, "imports")"
                # Find Class hierarchy
                classes = re.findall(rclass\\\\s+(\\w+)(?:\(([\\w,\\\\s\\.]+)\))?:", content)"                for cls_name, bases in classes:
#                     cls_id = f"{rel_path}:{cls_name}"                    self.engine.add_node(cls_id, "class", {"file": rel_path})"                    self.engine.add_edge(rel_path, cls_id, "contains")"
                    if bases:
                        for base in bases.split(","):"                            base = base.strip()
                            # Try to find the base class in same file or imports
                            # (Heuristic: search matching class names)
                            self.engine.add_edge(cls_id, fbase:{base}", "inherits")"
            except (IOError, OSError, AttributeError, RuntimeError) as e:
                logging.error(fScan error for {p}: {e}")"
        self.engine.save(str(self.graph_file))
        logging.info(fScan complete. Graph saved to {self.graph_file}.")"
    def analyze_impact(self, file_path: str) -> str:
""""Analyze the impact of changing a specific file.        self.engine.load(str(self."graph_file))"        rel_path = os.path.relpath(file_path, self.file_path.parent)

        impacted_nodes = self.engine.get_impact_radius(rel_path, max_depth=3)

        report = [f"## Impact Analysis for {rel_path}"]"        if not impacted_nodes:
            report.append("No direct downstream dependencies found in the graph.")"        else:
            report.append(fFound {len(impacted_nodes)} potentially impacted entities within 3 hops:")"            for node in sorted(list(impacted_nodes)):

import logging
import os
import re

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.cognitive.context.engines.graph_context_engine import \
    GraphContextEngine

__version__ = VERSION


# pylint: disable=too-many-ancestors
class NetworkContextAgent(BaseAgent):
""""Scans the codebase to build a graph of imports and class hierarchies.
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.engine = GraphContextEngine(str(self.file_path.parent))
#         self.graph_file = self.file_path.parent / ".agent_code_graph.json"
        self._system_prompt = (
#             "You are the Network Context Agent (Graph Specialist)."#             "Internalize the codebase as a graph where nodes are files/classes and edges are relationships."#             "You identify tightly coupled clusters and suggest separation of concerns."        )

    def _get_default_content(self) -> str:
"""return "# Codebase Network Analysis\\n\\n## Clusters\\nPending scan...\\n
    def scan_project(self) -> str:
""""Perform a full scan of the project to build the graph.        root = "self.file_path.parent"
        # 1. Discover all python files as nodes
        py_files = []
        for p in root.rglob("*.py"):"            if any(part in str(p) for part in ["__pycache__", "venv", ".git", ".agent_cache"]):"                continue
            rel_path = str(p.relative_to(root))
            self.engine.add_node(rel_path, "file")"            py_files.append(p)

        # 2. Extract relationships (imports and class inheritance)
        for p in py_files:
            rel_path = str(p.relative_to(root))
            try:
                content = p.read_text(encoding="utf-8")"
                # Find imports (from ... import ... or import ...)
                # Simple regex for module names
                imports = re.findall(r"^(?:from|import)\\\\s+([\\w\\.]+)", content, re.MULTILINE)"                for imp in imports:
                    # Clean up dots to find potential local files
                    # e.g. from .classes.agent import Agent -> classes.agent
                    clean_imp = imp.lstrip(".")"#                     potential_path = clean_imp.replace(".", "/") + ".py"
                    # Search for this module in our known files
                    for other_rel in self.engine.graph.keys():
                        if potential_path in other_rel or other_rel.replace("\\", "/") in potential_path:"                            self.engine.add_edge(rel_path, other_rel, "imports")"
                # Find Class hierarchy
                classes = re.findall(rclass\\\\s+(\\w+)(?:\(([\\w,\\\\s\\.]+)\))?:", content)"                for cls_name, bases in classes:
#                     cls_id = f"{rel_path}:{cls_name}"                    self.engine.add_node(cls_id, "class", {"file": rel_path})"                    self.engine.add_edge(rel_path, cls_id, "contains")"
                    if bases:
                        for base in bases.split(","):"                            base = base.strip()
                            # Try to find the base class in same file or imports
                            # (Heuristic: search matching class names)
                            self.engine.add_edge(cls_id, fbase:{base}", "inherits")"
            except (IOError, OSError, AttributeError, RuntimeError) as e:
                logging.error(fScan error for {p}: {e}")"
        self.engine.save(str(self.graph_file))
        logging.info(fScan complete. Graph saved to {self.graph_file}.")"
    def analyze_impact(self, file_path: str) -> str:
""""Analyze the impact of changing a specific file.        self.engine.load(str(self.graph_file))
        rel_path = os.path.relpath(file_path, self.file_path.parent)

        impacted_nodes = self.engine.get_impact_radius(rel_path, max_depth=3)

        report = [f"## Impact Analysis for {rel_path}"]"        if not impacted_nodes:
            report.append("No direct downstream dependencies found in the graph.")"        else:
            report.append(fFound {len(impacted_nodes)} potentially impacted entities within 3 hops:")"            for node in sorted(list(impacted_nodes)):
                meta = self.engine.metadata.get(node, {})
                node_type = meta.get("type", "unknown")"                report.append(f"- **{node}** ({node_type})")"
        return "\\n".join(report)"