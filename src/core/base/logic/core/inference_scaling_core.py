#!/usr/bin/env python3
"""Minimal InferenceScalingCore used by tests."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


class ScalingStrategy:
    STATIC = "static"
    ADAPTIVE = "adaptive"


@dataclass
class InferenceScalingCore:
    strategy: str = ScalingStrategy.STATIC

    def __init__(self, strategy: str = ScalingStrategy.STATIC) -> None:
        self.strategy = strategy

    def select_workers(self, load: float) -> int:
        if self.strategy == ScalingStrategy.STATIC:
            return 1
        return max(1, int(load * 2))


__all__ = ["ScalingStrategy", "InferenceScalingCore"]
