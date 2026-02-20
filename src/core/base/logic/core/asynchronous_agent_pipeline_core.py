#!/usr/bin/env python3
"""Minimal asynchronous agent pipeline core for tests."""
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


@dataclass
class Trajectory:
    steps: List[str]


class AsynchronousAgentPipelineCore:
    def __init__(self) -> None:
        self.tools: Dict[str, Any] = {}

    def register_tool(self, name: str, func: Any) -> None:
        self.tools[name] = func

    async def call_tool(self, call: ToolCall) -> ToolResult:
        fn = self.tools.get(call.name)
        if fn:
            try:
                return ToolResult(success=True, output=fn(**call.args))
            except Exception:
                return ToolResult(success=False, output=None)
        return ToolResult(success=False, output=None)


__all__ = ["ToolCall", "ToolResult", "Trajectory", "AsynchronousAgentPipelineCore"]
