#!/usr/bin/env python3

"""
GraphCore logic for PyAgent.
Pure logic for AST-based code relationship analysis and graph management.
"""

import ast
from typing import Dict, List, Set, Any, Optional, Tuple

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

class GraphCore:
    """Pure logic for managing code relationship graphs."""

    @staticmethod
    def parse_python_content(rel_path: str, content: str) -> Dict[str, Any]:
        """Parses Python code and returns extracted symbols and relationships."""
        try:
            tree = ast.parse(content)
            visitor = CodeGraphVisitor(rel_path)
            visitor.visit(tree)
            return {
                "rel_path": rel_path,
                "imports": list(visitor.imports),
                "classes": visitor.classes,
                "inherits": visitor.bases,
                "calls": list(visitor.calls)
            }
        except Exception:
            return {
                "rel_path": rel_path,
                "imports": [],
                "classes": [],
                "inherits": {},
                "calls": []
            }

    @staticmethod
    def build_edges(analysis: Dict[str, Any]) -> List[Tuple[str, str, str]]:
        """
        Builds graph edges from analysis results.
        Returns list of (source, target, relationship_type).
        """
        edges = []
        rel_path = analysis["rel_path"]
        
        # File level dependencies
        for imp in analysis["imports"]:
            edges.append((rel_path, imp, "imports"))
            
        # Class level edges
        for cls, bases in analysis["inherits"].items():
            for base in bases:
                edges.append((f"{rel_path}::{cls}", base, "inherits"))
                
        return edges
