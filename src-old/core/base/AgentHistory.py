#!/usr/bin/env python3
from __future__ import annotations

from src.core.base.state.agent_history import AgentConversationHistory  # type: ignore

__all__ = ["AgentConversationHistory"]

"""Compatibility shim exposing `AgentConversationHistory` at
`src.core.base.AgentHistory` to match older import paths.
"""
