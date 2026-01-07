#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

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

class VisualizationType(Enum):
    """Types of context visualization."""
    DEPENDENCY_GRAPH = "dependency_graph"
    CALL_HIERARCHY = "call_hierarchy"
    FILE_TREE = "file_tree"
    MIND_MAP = "mind_map"
