#!/usr/bin/env python3

"""Central registry for all agent tools and capabilities."""

import inspect
import logging
from typing import Dict, List, Any, Callable, Optional, Type
from pydantic import BaseModel, Field

class ToolMetadata(BaseModel):
    """Metadata for a registered tool."""
    name: str
    description: str
    parameters: Dict[str, Any]
    owner: str # Name of the agent providing this tool
    category: str = "general"

from .ToolCore import ToolCore, ToolMetadata

class ToolRegistry:
    """
    A registry that allows agents to discover and invoke tools across the fleet.
    Shell for ToolCore.
    """
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
            cls._instance.tools = {}
            cls._instance.core = ToolCore()
        return cls._instance

    def register_tool(self, owner_name: str, func: Callable, category: str = "general"):
        """Registers a function as a tool."""
        metadata = self.core.extract_metadata(owner_name, func, category)
        self.tools[metadata.name] = {
            "metadata": metadata,
            "function": func
        }
        logging.info(f"Tool registered: {owner_name}.{metadata.name}")

    def list_tools(self, category: Optional[str] = None) -> List[ToolMetadata]:
        """Lists all registered tools."""
        results = []
        for t in self.tools.values():
            meta = t["metadata"]
            if category is None or meta.category == category:
                results.append(meta)
        return results

    def get_tool(self, name: str) -> Optional[Callable]:
        """Retrieves a tool function by name."""
        if name in self.tools:
            return self.tools[name]["function"]
        return None

    def call_tool(self, name: str, **kwargs) -> Any:
        """Invoking a tool by name with provided arguments, filtering for supported ones."""
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found in registry.")
        
        filtered_kwargs = self.core.filter_arguments(tool, kwargs)
        logging.info(f"Invoking tool: {name} with filtered {filtered_kwargs}")
        return tool(**filtered_kwargs)
