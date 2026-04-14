#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
    """A registered CLI tool."""

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


def deregister_tool(name: str) -> None:
    """Remove a tool from the registry by exact name.

    Uses a copy-on-write dict swap so that any in-flight references to the old
    registry snapshot remain valid until their next read barrier.

    Args:
        name: Exact registered name of the tool to remove.
            No-op if the tool is not currently registered.

    """
    global _REGISTRY
    _REGISTRY = {k: v for k, v in _REGISTRY.items() if k != name}


async def async_run_tool(name: str, args: list[str] | None = None) -> int:
    """Await a tool's main coroutine or call it synchronously.

    Unlike :func:`run_tool`, this function is itself a coroutine so it must be
    awaited inside an existing event loop.  It never calls
    ``asyncio.run()`` internally.

    Args:
        name: Exact registered name of the tool to invoke.
        args: CLI-style argument list forwarded to the tool's ``main``
            callable.  Defaults to ``None`` (tool receives no arguments).

    Returns:
        The integer return value produced by the tool's ``main`` callable.

    Raises:
        KeyError: If *name* is not present in the registry.

    """
    spec = _REGISTRY.get(name)
    if spec is None:
        raise KeyError(f"Tool '{name}' not registered")
    result = spec.main(args)
    if asyncio.iscoroutine(result):
        return await result
    return result  # type: ignore[return-value]
