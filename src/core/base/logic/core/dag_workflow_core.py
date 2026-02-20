#!/usr/bin/env python3
"""
Parser-safe stub: DAG workflow core (conservative).

Minimal types and no-op functions to restore imports.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class WorkflowNode:
    id: str
    task_description: str


class DAGWorkflowCore:
    def __init__(self) -> None:
        self.nodes: Dict[str, WorkflowNode] = {}


__all__ = ["WorkflowNode", "DAGWorkflowCore"]
