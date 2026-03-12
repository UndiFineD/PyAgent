#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/context/VisualizationData.description.md

# VisualizationData

**File**: `src\classes\context\VisualizationData.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 18 imports  
**Lines**: 34  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `VisualizationData`

Data for context visualization.

Attributes:
    viz_type: Type of visualization.
    nodes: List of node data.
    edges: List of edge connections.
    layout: Layout algorithm to use.

## Dependencies

**Imports** (18):
- `VisualizationType.VisualizationType`
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `enum.Enum`
- `hashlib`
- `json`
- `logging`
- `pathlib.Path`
- `re`
- `src.classes.base_agent.BaseAgent`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- ... and 3 more

---
*Auto-generated documentation*
## Source: src-old/classes/context/VisualizationData.improvements.md

# Improvements for VisualizationData

**File**: `src\classes\context\VisualizationData.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 34 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `VisualizationData_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

"""Auto-extracted class from agent_context.py"""


from .VisualizationType import VisualizationType

from src.classes.base_agent import BaseAgent
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
