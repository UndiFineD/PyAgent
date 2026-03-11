#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/coder/SvgAgent.description.md

# SvgAgent

**File**: `src\classes\coder\SvgAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 29  
**Complexity**: 2 (simple)

## Overview

Agent specializing in 2D SVG image generation and optimization.

## Classes (1)

### `SvgAgent`

**Inherits from**: CoderAgent

Agent for generating and optimizing 2D SVG vector graphics.

**Methods** (2):
- `__init__(self, file_path)`
- `_get_default_content(self)`

## Dependencies

**Imports** (3):
- `CoderAgent.CoderAgent`
- `logging`
- `src.classes.base_agent.utilities.create_main_function`

---
*Auto-generated documentation*
## Source: src-old/classes/coder/SvgAgent.improvements.md

# Improvements for SvgAgent

**File**: `src\classes\coder\SvgAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 29 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SvgAgent_test.py` with pytest tests

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

"""Agent specializing in 2D SVG image generation and optimization."""


from src.classes.base_agent.utilities import create_main_function

from .CoderAgent import CoderAgent


class SvgAgent(CoderAgent):
    """Agent for generating and optimizing 2D SVG vector graphics."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._language = "xml"  # SVG is XML-based
        self._system_prompt = (
            "You are an SVG Graphic Designer and Vector Optimization Expert. "
            "You generate high-quality, clean, and optimized 2D SVG code. "
            "Focus on semantic tags, proper viewports, path optimization, and CSS styling within the SVG. "
            "Avoid bloated markup and use minimal precision for coordinates."
        )

    def _get_default_content(self) -> str:
        return '<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">\n  <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />\n</svg>\n'


if __name__ == "__main__":
    main = create_main_function(SvgAgent, "SVG Agent", "Path to SVG file (.svg)")
    main()
