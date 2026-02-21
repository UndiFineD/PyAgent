#!/usr/bin/env python3
"""Minimal stub for asynchronous_agent_pipeline_core used during repairs."""

from __future__ import annotations


class AsynchronousAgentPipelineCore:
    """Repair-time stub of AsynchronousAgentPipelineCore."""

    def __init__(self, *args, **kwargs) -> None:
        pass


__all__ = ["AsynchronousAgentPipelineCore"]

#!/usr/bin/env python3
"""
Parser-safe stub: Asynchronous agent pipeline core (conservative).

Provides minimal async pipeline types and a no-op call implementation.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Dict


@dataclass
class ToolCall:
    name: str
    args: Dict[str, Any]


@dataclass
class ToolResult:
    success: bool
    output: Any = None


class AsynchronousAgentPipelineCore:
    async def call_tool(self, call: ToolCall) -> ToolResult:
        return ToolResult(success=False, output=None)


__all__ = ["ToolCall", "ToolResult", "AsynchronousAgentPipelineCore"]
