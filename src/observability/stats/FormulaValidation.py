#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from dataclasses import dataclass


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class FormulaValidation:
    """Result of formula validation."""
    is_valid: bool = True
    error: str = ""
