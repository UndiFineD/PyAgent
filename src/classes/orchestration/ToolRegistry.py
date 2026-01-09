#!/usr/bin/env python3

"""Central registry for all agent tools and capabilities."""

import inspect
import logging
from typing import Dict, List, Any, Callable, Optional, Type
from .ToolCore import ToolCore, ToolMetadata

class ToolRegistry:
    """
    A registry that allows agents to discover and invoke tools across the fleet.
    Shell for ToolCore.
    """
    
    _instance = None
    
    def __new__(cls, *args: Any, **kwargs: Any) -> "ToolRegistry":
        if not cls._instance:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
            cls._instance.tools: Dict[str, List[Dict[str, Any]]] = {}
            cls._instance.core = ToolCore()
        return cls._instance

    def register_tool(self, owner_name: str, func: Callable, category: str = "general", priority: int = 0) -> None:
        """Registers a function as a tool with priority scoring."""
        metadata = self.core.extract_metadata(owner_name, func, category, priority)
        
        if metadata.name not in self.tools:
            self.tools[metadata.name] = []
            
        self.tools[metadata.name].append({
            "metadata": metadata,
            "function": func
        })
        # Sort by priority descending
        self.tools[metadata.name].sort(key=lambda x: x["metadata"].priority, reverse=True)
        
        logging.info(f"Tool registered: {owner_name}.{metadata.name} (Priority: {priority})")

    def list_tools(self, category: Optional[str] = None) -> List[ToolMetadata]:
        """Lists all registered tools."""
        results = []
        for tool_list in self.tools.values():
            for t in tool_list:
                meta = t["metadata"]
                if category is None or meta.category == category:
                    results.append(meta)
        return results

    def get_tool(self, name: str) -> Optional[Callable]:
        """Retrieves the highest priority tool function by name."""
        if name in self.tools and self.tools[name]:
            return self.tools[name][0]["function"]
        return None

    def call_tool(self, name: str, **kwargs) -> Any:
        """Invoking a tool by name with provided arguments, filtering for supported ones."""
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found in registry.")
        
        filtered_kwargs = self.core.filter_arguments(tool, kwargs)
        logging.info(f"Invoking tool: {name} with filtered {filtered_kwargs}")
        return tool(**filtered_kwargs)
