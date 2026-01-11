#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_improvements.py"""

from .Improvement import Improvement

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

class ImpactScorer:
    """Scores improvements based on weighted impact factors."""

    def __init__(self) -> None:
        self.weights: Dict[str, float] = {
            "complexity": 0.34,
            "reach": 0.33,
            "urgency": 0.33,
        }

    def set_weights(self, weights: Dict[str, float]) -> None:
        self.weights = dict(weights)

    def calculate_weighted_score(self, factors: Dict[str, float]) -> float:
        score = 0.0
        for key, weight in self.weights.items():
            score += float(factors.get(key, 0.0)) * float(weight)
        return score

    def calculate_score(self, improvement: Improvement) -> float:
        """Compute a 0..100 score based on simple heuristics."""
        text = f"{improvement.title} {improvement.description}".lower()

        urgency = 80.0 if "urgent" in text or "critical" in text else 50.0
        reach = 75.0 if "api" in text or "endpoint" in text else 55.0
        complexity = 60.0 if "refactor" in text or "architecture" in text else 45.0

        # Nudge by priority when present.
        try:
            urgency += float(getattr(improvement.priority, "value", 0)) * 2
        except Exception:
            pass

        base = self.calculate_weighted_score({
            "complexity": complexity,
            "reach": reach,
            "urgency": urgency,
        })
        return float(max(0.0, min(100.0, base)))
