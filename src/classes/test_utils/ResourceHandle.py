#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class ResourceHandle:
    """A handle representing an acquired resource from ResourcePool."""

    name: str
