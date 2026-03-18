#!/usr/bin/env python3
"""Tool registration and dispatch utilities.

Each tool module should register itself by calling `register_tool()` at import time.
This enables a single CLI entrypoint to enumerate and execute tools.

Example:

    from src.tools.tool_registry import register_tool

    def main(args: list[str] | None = None) -> int:
        ...

    register_tool("git-utils", main, "Git/GitHub helper utilities")
"""

from __future__ import annotations

import asyncio
import inspect
from dataclasses import dataclass
from typing import Any, Callable, Coroutine, Dict, List, Optional, Union


ToolMain = Callable[[list[str] | None], Union[int, Coroutine[Any, Any, int]]]


@dataclass(frozen=True)
class Tool:
    name: str
    main: ToolMain
    description: str


_REGISTRY: Dict[str, Tool] = {}


def register_tool(name: str, main: ToolMain, description: str) -> None:
    """Register a tool for use by the shared CLI launcher."""
    existing = _REGISTRY.get(name)
    if existing is not None:
        # Some test harnesses re-import modules dynamically; allow idempotent re-registration
        # as long as the tool description is unchanged.
        if existing.description == description:
            return
        raise ValueError(f"Tool '{name}' is already registered")
    _REGISTRY[name] = Tool(name=name, main=main, description=description)


def list_tools() -> List[Tool]:
    """Return all registered tools."""
    return sorted(_REGISTRY.values(), key=lambda t: t.name)


def get_tool(name: str) -> Optional[Tool]:
    """Get a registered tool by name."""
    return _REGISTRY.get(name)


def run_tool(name: str, args: list[str] | None = None) -> int:
    """Execute a registered tool by name."""
    tool = get_tool(name)
    if tool is None:
        raise KeyError(f"Unknown tool: {name}")

    result = tool.main(args)
    if inspect.isawaitable(result):
        return asyncio.run(result)
    return result
