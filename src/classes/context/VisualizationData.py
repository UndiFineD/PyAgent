#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

from .VisualizationType import VisualizationType

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import re
import zlib

@dataclass
class VisualizationData:
    """Data for context visualization.

    Attributes:
        viz_type: Type of visualization.
        nodes: List of node data.
        edges: List of edge connections.
        layout: Layout algorithm to use.
    """
    viz_type: VisualizationType
    nodes: List[Dict[str, Any]] = field(default_factory=lambda: [])
    edges: List[Tuple[str, str]] = field(default_factory=lambda: [])
    layout: str = "hierarchical"
