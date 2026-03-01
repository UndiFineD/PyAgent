# ToolIntegration

**File**: `src\observability\improvements\ToolIntegration.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 115  
**Complexity**: 6 (moderate)

## Overview

Auto-extracted class from agent_improvements.py

## Classes (1)

### `ToolIntegration`

Integrates with code analysis tools for suggestions.

Parses output from linters, type checkers, and other tools.

Attributes:
    tool_configs: Configuration for each tool.
    suggestions: List of tool suggestions.

**Methods** (6):
- `__init__(self)`
- `configure_tool(self, tool_name, tool_type, command)`
- `parse_pylint_output(self, output)`
- `parse_mypy_output(self, output)`
- `get_suggestions(self, tool_type)`
- `convert_to_improvements(self, suggestions)`

## Dependencies

**Imports** (10):
- `AnalysisToolType.AnalysisToolType`
- `ImprovementCategory.ImprovementCategory`
- `ToolSuggestion.ToolSuggestion`
- `__future__.annotations`
- `re`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
