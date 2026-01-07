#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict
import time

@dataclass
class TestBaseline:
    __test__ = False
    """A test baseline for comparison.

    Attributes:
        name: Baseline name.
        values: Baseline values.
        created_at: Creation timestamp.
        version: Baseline version.
    """

    name: str
    values: Dict[str, Any]
    created_at: float = field(default_factory=time.time)
    version: int = 1
