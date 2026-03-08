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

"""
Core logic for Entropy Measurement (Phase 172).
Calculates structural complexity metrics.
"""

import ast
import os

try:
    import rust_core as rc

    HAS_RUST = True
except ImportError:
    HAS_RUST = False


class EntropyCore:
    """Core logic for calculating code complexity and entropy."""

    @staticmethod
    def calculate_cyclomatic_complexity(code: str) -> int:
        """
        Estimates cyclomatic complexity based on AST nodes.
        CC = E - N + 2P (approximate using decision points)
        """
        try:
            import rust_core

            return rust_core.calculate_cyclomatic_complexity(code)  # type: ignore[attr-defined]
        except (ImportError, AttributeError):
            pass

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

        with open(file_path, encoding="utf-8", errors="ignore") as f:
            content = f.read()

        return {
            "size_bytes": len(content),
            "lines": len(content.splitlines()),
            "complexity": EntropyCore.calculate_cyclomatic_complexity(content),
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

        # Rust-accelerated aggregation
        if HAS_RUST:
            try:
                metrics_tuples = [(m["lines"], m["complexity"]) for m in all_metrics]
                # type: ignore[attr-defined]
                avg_size, avg_complexity, max_complexity, count = rc.aggregate_file_metrics_rust(
                    metrics_tuples
                )
                return {
                    "avg_size": avg_size,
                    "avg_complexity": avg_complexity,
                    "max_complexity": max_complexity,
                    "file_count": count,
                }
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                pass

        count = len(all_metrics)
        return {
            "avg_size": sum(m["size_bytes"] for m in all_metrics) / count,
            "avg_complexity": sum(m["complexity"] for m in all_metrics) / count,
            "max_complexity": max(m["complexity"] for m in all_metrics),
            "file_count": count,
        }
