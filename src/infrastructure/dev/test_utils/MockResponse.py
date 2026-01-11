#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from .MockResponseType import MockResponseType

from dataclasses import dataclass
from typing import Optional

@dataclass
class MockResponse:
    """Mock AI backend response.

    Attributes:
        content: Response content.
        response_type: Type of response.
        latency_ms: Simulated latency.
        tokens_used: Simulated token count.
        error_message: Error message if applicable.
    """

    content: str = ""
    response_type: MockResponseType = MockResponseType.SUCCESS
    latency_ms: int = 100
    tokens_used: int = 0
    error_message: Optional[str] = None
