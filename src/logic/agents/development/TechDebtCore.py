from __future__ import annotations

import ast
from typing import Dict, List, Any, Optional
from src.core.base.version import VERSION

__version__ = VERSION

class TechDebtCore:
    """
    Pure logic for analyzing technical debt from AST.
    Ready for Rust conversion.
    """

    @staticmethod
    def analyze_ast_debt(tree: ast.AST) -> List[Dict[str, Any]]:
        """
        Analyzes an AST tree for technical debt markers.
        
        Args:
            tree: The pre-parsed AST tree.
            
        Returns:
            A list of identified issues.
        """
        issues = []
        
        # Check for missing docstrings
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                if not ast.get_docstring(node):
                    issues.append({
                        "type": "Missing Docstring",
                        "name": getattr(node, 'name', 'Module'),
                        "severity": "Low"
                    })
        
        # Check for high node density (complexity proxy)
        node_count = sum(1 for _ in ast.walk(tree))
        if node_count > 1000:
            issues.append({
                "type": "High Complexity",
                "detail": f"Structure contains {node_count} AST nodes.",
                "severity": "Medium"
            })
            
        return issues

    @staticmethod
    def identify_hotspots(reports: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
        """Sorts and returns major technical debt hotspots."""
        return sorted(reports, key=lambda x: x.get('issue_count', 0), reverse=True)[:limit]
