#!/usr/bin/env python3
from __future__ import annotations



# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
"""
Minimal ToolRegistry shim for tests and importability.

"""
This provides a small registry to register and call tool functions.
"""
import asyncio
import inspect
import logging
from collections import defaultdict
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from .tool_core import ToolCore

if TYPE_CHECKING:
    from ..fleet.FleetManager import FleetManager


class ToolRegistry:
"""
A simple in-process tool registry used by tests.

    Tools are stored by name with a list of implementations and metadata.
"""
def __init__(self, fleet: Optional["FleetManager"] = None) -> None:
        self.fleet = fleet
        # tools[name] -> list of dicts with metadata and function
        self.tools: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.core = ToolCore()

    def register_tool(self, owner_name: str, func: Callable, category: str = "general", priority: int = 1) -> None:
        name = getattr(func, "__name__", "<anonymous>")
        if any(t["owner"] == owner_name and t["function"] is func for t in self.tools[name]):
            logging.debug("Tool %s already registered for %s. Skipping.", name, owner_name)
            return

        entry = {
            "owner": owner_name,
            "function": func,
            "category": category,
            "priority": int(priority),
            "sync": not inspect.iscoroutinefunction(func),
        }
        self.tools[name].append(entry)
        # sort by priority descending
        self.tools[name].sort(key=lambda x: x["priority"], reverse=True)
        logging.debug("Registered tool: %s from %s (Priority: %s)", name, owner_name, priority)

    def list_tools(self) -> List[Dict[str, Any]]:
        meta: List[Dict[str, Any]] = []
        for name, variations in self.tools.items():
            for v in variations:
                meta.append({
                    "name": name,
                    "owner": v.get("owner"),
                    "category": v.get("category"),
                    "priority": v.get("priority"),
                    "sync": v.get("sync", True),
                })
        return meta

    def get_tool(self, name: str) -> Optional[Callable]:
        if name in self.tools and self.tools[name]:
            return self.tools[name][0]["function"]
        return None

    async def call_tool(self, name: str, **kwargs) -> Any:
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found in registry.")

        filtered_kwargs = self.core.filter_arguments(tool, kwargs)
        logging.info("Invoking tool: %s with filtered %s", name, filtered_kwargs)

        if inspect.iscoroutinefunction(tool):
            return await tool(**filtered_kwargs)

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: tool(**filtered_kwargs))
