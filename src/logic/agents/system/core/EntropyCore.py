"""
Core logic for Entropy Measurement (Phase 172).
Calculates structural complexity metrics.
"""

import os
import ast

class EntropyCore:
    @staticmethod
    def calculate_cyclomatic_complexity(code: str) -> int:
        """
        Estimates cyclomatic complexity based on AST nodes.
        CC = E - N + 2P (approximate using decision points)
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return 0
            
        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.And, ast.Or, ast.ExceptHandler)):
                complexity += 1
        return complexity

    @staticmethod
    def get_file_metrics(file_path: str) -> dict:
        """
        Returns size and estimated complexity for a single file.
        """
        if not os.path.exists(file_path):
            return {}
            
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        return {
            "size_bytes": len(content),
            "lines": len(content.splitlines()),
            "complexity": EntropyCore.calculate_cyclomatic_complexity(content)
        }

    @staticmethod
    def scan_directory_metrics(directory: str) -> dict:
        """
        Scans a directory and returns aggregate metrics.
        """
        all_metrics = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    metrics = EntropyCore.get_file_metrics(os.path.join(root, file))
                    if metrics:
                        all_metrics.append(metrics)
                        
        if not all_metrics:
            return {}
            
        count = len(all_metrics)
        return {
            "avg_size": sum(m['size_bytes'] for m in all_metrics) / count,
            "avg_complexity": sum(m['complexity'] for m in all_metrics) / count,
            "max_complexity": max(m['complexity'] for m in all_metrics),
            "file_count": count
        }
