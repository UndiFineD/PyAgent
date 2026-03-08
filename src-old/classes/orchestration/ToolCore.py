"""
LLM_CONTEXT_START

## Source: src-old/classes/orchestration/ToolCore.description.md

# ToolCore

**File**: `src\classes\orchestration\ToolCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 7 imports  
**Lines**: 52  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for ToolCore.

## Classes (2)

### `ToolMetadata`

**Inherits from**: BaseModel

Metadata for a registered tool.

### `ToolCore`

Pure logic for tool registration and invocation.
Handles parameter introspection and argument filtering.

**Methods** (2):
- `extract_metadata(self, owner_name, func, category, priority)`
- `filter_arguments(self, func, args_dict)`

## Dependencies

**Imports** (7):
- `inspect`
- `pydantic.BaseModel`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/orchestration/ToolCore.improvements.md

# Improvements for ToolCore

**File**: `src\classes\orchestration\ToolCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 52 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ToolCore_test.py` with pytest tests

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

import inspect
from typing import Dict, List, Any, Callable, Optional
from pydantic import BaseModel


class ToolMetadata(BaseModel):
    """Metadata for a registered tool."""

    name: str
    description: str
    parameters: Dict[str, Any]
    owner: str  # Name of the agent providing this tool
    category: str = "general"
    priority: int = 0


class ToolCore:
    """
    Pure logic for tool registration and invocation.
    Handles parameter introspection and argument filtering.
    """

    def extract_metadata(
        self, owner_name: str, func: Callable, category: str, priority: int = 0
    ) -> ToolMetadata:
        """Extracts ToolMetadata from a function signature."""
        name: str = func.__name__
        doc: str = func.__doc__ or "No description provided."

        # Simple parameter extraction
        sig = inspect.signature(func)
        params: Dict[str, str] = {}
        for p_name, param in sig.parameters.items():
            if p_name == "self":
                continue  # Skip self
            params[p_name] = (
                str(param.annotation)
                if param.annotation != inspect.Parameter.empty
                else "Any"
            )

        return ToolMetadata(
            name=name,
            description=doc.split("\n")[0].strip(),
            parameters=params,
            owner=owner_name,
            category=category,
            priority=priority,
        )

    def filter_arguments(
        self, func: Callable, args_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Filters input dictionary to only include keys supported by the function."""
        sig = inspect.signature(func)
        has_kwargs: bool = any(
            p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
        )

        if has_kwargs:
            return args_dict

        return {k: v for k, v in args_dict.items() if k in sig.parameters}
