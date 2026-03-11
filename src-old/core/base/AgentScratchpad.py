#!/usr/bin/env python3
from __future__ import annotations

"""Compatibility shim exposing `AgentScratchpad` at
`src.core.base.AgentScratchpad` to match older import paths.
"""

from src.core.base.state.agent_scratchpad import AgentScratchpad  # type: ignore

__all__ = ["AgentScratchpad"]
