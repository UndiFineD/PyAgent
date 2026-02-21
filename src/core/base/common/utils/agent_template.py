#!/usr/bin/env python3
"""Minimal, import-safe agent template used by tests and repair runs."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AgentTemplate:
    """Simple agent template placeholder.

    Keeping this minimal avoids heavy runtime deps while repairs run.
    """
    name: str = "unknown"
    description: str = ""
    agents: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)
    file_patterns: List[str] = field(default_factory=lambda: ["*.py"])
