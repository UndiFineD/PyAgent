#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class TestProfile:
    __test__ = False
    """A test configuration profile.

    Attributes:
        name: Profile name.
        settings: Profile settings.
        env_vars: Environment variables.
        enabled: Whether profile is enabled.
    """

    name: str
    settings: Dict[str, Any] = field(default_factory=lambda: {})
    env_vars: Dict[str, str] = field(default_factory=lambda: {})
    enabled: bool = True
