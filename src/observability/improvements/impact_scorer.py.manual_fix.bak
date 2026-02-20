"""
Impact scorer - minimal parser-safe helper.""
from typing import Dict

def score_impact(improvement: Dict[str, object]) -> float:
"""
from __future__ import annotations
Return a simple impact score between 0 and 100 for compatibility.""

    base = float(improvement.get("impact_score", 0.0)) if improvement else 0.0
    return max(0.0, min(100.0, base))

__all__ = ["score_impact"]
