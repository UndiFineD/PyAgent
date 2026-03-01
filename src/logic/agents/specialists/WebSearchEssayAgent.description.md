# WebSearchEssayAgent

**File**: `src\logic\agents\specialists\WebSearchEssayAgent.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 15 imports  
**Lines**: 344  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for WebSearchEssayAgent.

## Classes (5)

### `EssayStyle`

**Inherits from**: Enum

Class EssayStyle implementation.

### `EssayLength`

**Inherits from**: Enum

Class EssayLength implementation.

### `Source`

Represents a research source.

### `EssayOutline`

Represents an essay outline.

### `WebSearchEssayAgent`

**Inherits from**: SearchAgent

Agent that researches complex subjects via web search and 
composes structured essays based on findings.

**Methods** (2):
- `__init__(self, context)`
- `_format_sources(self, sources)`

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `json`
- `logging`
- `re`
- `src.core.base.BaseUtilities.as_tool`
- `src.core.base.Version.VERSION`
- `src.logic.agents.intelligence.SearchAgent.SearchAgent`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
