#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/orchestration/ToolRegistry.description.md

# ToolRegistry

**File**: `src\classes\orchestration\ToolRegistry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 65  
**Complexity**: 5 (moderate)

## Overview

Central registry for all agent tools and capabilities.

## Classes (1)

### `ToolRegistry`

A registry that allows agents to discover and invoke tools across the fleet.
Shell for ToolCore.

**Methods** (5):
- `__new__(cls)`
- `register_tool(self, owner_name, func, category, priority)`
- `list_tools(self, category)`
- `get_tool(self, name)`
- `call_tool(self, name)`

## Dependencies

**Imports** (10):
- `ToolCore.ToolCore`
- `ToolCore.ToolMetadata`
- `inspect`
- `logging`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Type`

---
*Auto-generated documentation*
## Source: src-old/classes/orchestration/ToolRegistry.improvements.md

# Improvements for ToolRegistry

**File**: `src\classes\orchestration\ToolRegistry.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 65 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ToolRegistry_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""Central registry for all agent tools and capabilities."""

import logging
from typing import Any, Callable, Dict, List, Optional

from .ToolCore import ToolCore, ToolMetadata


class ToolRegistry:
    """A registry that allows agents to discover and invoke tools across the fleet.
    Shell for ToolCore.
    """

    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "ToolRegistry":
        if not cls._instance:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
            cls._instance.tools: Dict[str, List[Dict[str, Any]]] = {}
            cls._instance.core = ToolCore()
        return cls._instance

    def register_tool(
        self,
        owner_name: str,
        func: Callable,
        category: str = "general",
        priority: int = 0,
    ) -> None:
        """Registers a function as a tool with priority scoring."""
        metadata = self.core.extract_metadata(owner_name, func, category, priority)

        if metadata.name not in self.tools:
            self.tools[metadata.name] = []

        self.tools[metadata.name].append({"metadata": metadata, "function": func})
        # Sort by priority descending
        self.tools[metadata.name].sort(
            key=lambda x: x["metadata"].priority, reverse=True
        )

        logging.info(
            f"Tool registered: {owner_name}.{metadata.name} (Priority: {priority})"
        )

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
