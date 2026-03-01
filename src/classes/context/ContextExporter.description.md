# ContextExporter

**File**: `src\classes\context\ContextExporter.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 89  
**Complexity**: 6 (moderate)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `ContextExporter`

Exports context to documentation systems.

Provides functionality to export context to various formats.

Example:
    >>> exporter=ContextExporter()
    >>> exported=exporter.export(content, ExportFormat.HTML)

**Methods** (6):
- `__init__(self, default_format)`
- `set_format(self, format)`
- `get_supported_formats(self)`
- `export(self, content, format)`
- `_to_html(self, content)`
- `_to_rst(self, content)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `datetime.datetime`
- `re`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.context.models.ExportFormat.ExportFormat`
- `src.logic.agents.cognitive.context.models.ExportedContext.ExportedContext`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
