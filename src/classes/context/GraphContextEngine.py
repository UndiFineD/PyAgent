#!/usr/bin/env python3

"""Core engine for managing code relationships as a graph."""

import os
import json
import logging
import re
import ast
from pathlib import Path
from typing import Dict, List, Set, Any, Optional

class CodeGraphVisitor(ast.NodeVisitor):
    """AST visitor to extract imports, classes, and function calls."""
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.imports: Set[str] = set()
        self.classes: List[str] = []
        self.calls: Set[str] = set()
        self.bases: Dict[str, List[str]] = {}

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            self.imports.add(node.module)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.classes.append(node.name)
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(base.attr)
        self.bases[node.name] = bases
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name):
            self.calls.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.calls.add(node.func.attr)
        self.generic_visit(node)

class GraphContextEngine:
    """Manages an adjacency list of file and class dependencies."""
    
    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.graph: Dict[str, Set[str]] = {}
        self.metadata: Dict[str, Any] = {}
        self.symbols: Dict[str, Any] = {}
        self.persist_file = self.workspace_root / ".agent_graph.json"
        self.load()

    def add_edge(self, source: str, target: str, relationship: str = "imports") -> None:
        """Add a directed edge to the graph."""
        if source not in self.graph:
            self.graph[source] = set()
        self.graph[source].add(target)
        # Store metadata
        key = f"{source}->{target}"
        self.metadata[key] = {"type": relationship}

    def scan_project(self, start_path: Optional[Path] = None) -> None:
        """Scans files using AST to build a detailed relationship graph."""
        target = start_path or self.workspace_root
        logging.info(f"Scanning project graph from {target}")
        
        for py_file in target.rglob("*.py"):
            if any(p in str(py_file) for p in [".venv", "__pycache__", ".git"]):
                continue
            
            rel_path = str(py_file.relative_to(self.workspace_root))
            try:
                tree = ast.parse(py_file.read_text(encoding="utf-8"))
                visitor = CodeGraphVisitor(rel_path)
                visitor.visit(tree)
                
                # Add file level dependencies
                for imp in visitor.imports:
                    self.add_edge(rel_path, imp, "imports")
                
                # Store symbol info
                self.symbols[rel_path] = {
                    "classes": visitor.classes,
                    "inherits": visitor.bases,
                    "calls": list(visitor.calls)
                }
                
                # Add class level edges
                for cls, bases in visitor.bases.items():
                    for base in bases:
                        self.add_edge(f"{rel_path}::{cls}", base, "inherits")

            except Exception as e:
                logging.debug(f"Could not scan {rel_path}: {e}")

    def get_impact_radius(self, node: str, max_depth: int = 3) -> Set[str]:
        """Find all nodes that depend on the given node (inverse of graph)."""
        affected = set()
        to_visit = [(node, 0)]
        visited = {node}
        
        inverse_graph: Dict[str, Set[str]] = {}
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
                with open(self.persist_file, "r") as f:
                    data = json.load(f)
                self.graph = {k: set(v) for k, v in data.get("graph", {}).items()}
                self.metadata = data.get("metadata", {})
                self.symbols = data.get("symbols", {})
            except Exception as e:
                logging.error(f"Error loading graph: {e}")
