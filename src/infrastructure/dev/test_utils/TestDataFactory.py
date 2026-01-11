#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from .TestDataType import TestDataType

from dataclasses import dataclass
from typing import Optional

@dataclass
class TestDataFactory:
    __test__ = False
    """Factory for generating test data.

    Attributes:
        data_type: Type of data to generate.
        template: Template for generation.
        variations: Number of variations to create.
        seed: Random seed for reproducibility.
    """

    data_type: TestDataType
    template: str = ""
    variations: int = 1
    seed: Optional[int] = None
