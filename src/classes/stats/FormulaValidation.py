#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from dataclasses import dataclass

@dataclass
class FormulaValidation:
    """Result of formula validation."""
    is_valid: bool = True
    error: str = ""
