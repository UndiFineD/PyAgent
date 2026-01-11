#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_improvements.py"""

from .EffortEstimate import EffortEstimate
from .EffortEstimateResult import EffortEstimateResult
from .Improvement import Improvement
from .ImprovementCategory import ImprovementCategory

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, cast
import hashlib
import json
import logging
import re
import subprocess
import time


































from src.core.base.version import VERSION
__version__ = VERSION

class EffortEstimator:
    """Estimates effort for improvements."""

    def __init__(self) -> None:
        self.base_rates: Dict[str, float] = {
            "low": 2.0,
            "medium": 6.0,
            "high": 16.0,
        }
        self.historical_data: Dict[str, List[float]] = {}

    def add_historical_data(self, category: str, actual_hours: float) -> None:
        self.historical_data.setdefault(category, []).append(float(actual_hours))

    def estimate(self, improvement: Improvement, **kwargs: Any) -> EffortEstimateResult:
        complexity = str(kwargs.get("complexity", "medium")).lower()
        category = kwargs.get("category")
        if isinstance(category, ImprovementCategory):
            category_key = category.value
        else:
            category_key = str(category) if category is not None else ""

        if category_key and category_key in self.historical_data and self.historical_data[category_key]:
            base = sum(self.historical_data[category_key]) / len(self.historical_data[category_key])
        else:
            base = float(self.base_rates.get(complexity, self.base_rates["medium"]))

        # If an EffortEstimate enum is present, bias the base.
        effort = getattr(improvement, "effort", None)
        if isinstance(effort, EffortEstimate):
            scale = {
                EffortEstimate.TRIVIAL: 0.5,
                EffortEstimate.SMALL: 0.75,
                EffortEstimate.MEDIUM: 1.0,
                EffortEstimate.LARGE: 2.0,
                EffortEstimate.EPIC: 4.0,
            }.get(effort, 1.0)
            base *= scale

        return EffortEstimateResult(hours=float(base))
