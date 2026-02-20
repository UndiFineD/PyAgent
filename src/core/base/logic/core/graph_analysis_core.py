#!/usr/bin/env python3
"""Minimal GraphAnalysisCore used for tests."""
try:
    from __future__ import annotations
except ImportError:
    from __future__ import annotations


try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass

try:
    from typing import Any, Dict, List
except ImportError:
    from typing import Any, Dict, List



@dataclass
class GraphAnalysisCore:
    storage_path: str = "data/graphs"

    def __init__(self, storage_path: str = "data/graphs") -> None:
        self.storage_path = storage_path

    def analyze(self, graph: Dict[str, List[str]]) -> Dict[str, Any]:
        # Return simple metrics for tests
        return {"nodes": len(graph), "edges": sum(len(v) for v in graph.values())}


__all__ = ["GraphAnalysisCore"]
