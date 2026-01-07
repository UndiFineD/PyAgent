#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class ParameterizedTestCase:
    """A parameterized test case.

    Attributes:
        name: Test case name.
        params: Parameters for the test.
        expected: Expected result.
        tags: Optional tags for filtering.
    """

    name: str
    params: Dict[str, Any]
    expected: Any
    tags: List[str] = field(default_factory=lambda: [])
