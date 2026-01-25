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

"""
Tool registry.py module.
"""

from __future__ import annotations

import asyncio
import inspect
import logging
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from .tool_core import ToolCore

if TYPE_CHECKING:
    from ..fleet.FleetManager import FleetManager


class ToolRegistry:
    """Central registry for managing and invoking PyAgent tools across all specialists."""

    def __init__(self, fleet: FleetManager | None = None) -> None:
        self.fleet = fleet
        self.tools: dict[str, list[dict[str, Any]]] = {}
        self.core = ToolCore()

    def register_tool(
        self,
        owner_name: str,
        func: Callable,
        category: str = "general",
        priority: int = 1,
    ) -> None:
        """Adds a tool function to the registry."""
        name = func.__name__
        if name not in self.tools:
            self.tools[name] = []

        # Check for duplicates
        if any(t["owner"] == owner_name for t in self.tools[name]):
            logging.debug(f"Tool {name} already registered for {owner_name}. Skipping.")
            return

        self.tools[name].append(
            {
                "owner": owner_name,
                "function": func,
                "category": category,
                "priority": priority,
                "sync": not inspect.iscoroutinefunction(func),
            }
        )
        # Sort by priority desc
        self.tools[name].sort(key=lambda x: x["priority"], reverse=True)
        logging.debug(f"Registered tool: {name} from {owner_name} (Priority: {priority})")

    def list_tools(self) -> list[Any]:
        """Returns metadata for all registered tools."""
        from collections import namedtuple

        ToolMeta = namedtuple("ToolMeta", ["name", "owner", "category", "priority", "sync"])

        meta = []
        for name, variations in self.tools.items():
            for v in variations:
                meta.append(
                    ToolMeta(
                        name,
                        v["owner"],
                        v["category"],
                        v["priority"],
                        v.get("sync", True),
                    )
                )
        return meta

    def get_tool(self, name: str) -> Callable | None:
        """Retrieves the highest priority tool function by name."""
        if name in self.tools and self.tools[name]:
            return self.tools[name][0]["function"]
        return None

    async def call_tool(self, name: str, **kwargs) -> Any:
        """Invoking a tool by name with provided arguments, filtering for supported ones."""
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found in registry.")

        filtered_kwargs = self.core.filter_arguments(tool, kwargs)
        logging.info(f"Invoking tool: {name} with filtered {filtered_kwargs}")

        if inspect.iscoroutinefunction(tool):
            return await tool(**filtered_kwargs)

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: tool(**filtered_kwargs))
