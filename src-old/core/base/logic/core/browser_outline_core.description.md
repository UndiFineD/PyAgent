# browser_outline_core

**File**: `src\core\base\logic\core\browser_outline_core.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 6 imports  
**Lines**: 78  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for browser_outline_core.

## Classes (2)

### `BrowserElement`

Class BrowserElement implementation.

### `BrowserOutlineCore`

Transforms raw DOM/CDP data into a high-density 'Outline' for efficient LLM navigation.
Reduces token usage by replacing complex selectors with simple labels (e.g., [l1]).
Harvested from .external/AI-Auto-browser pattern.

**Methods** (3):
- `__init__(self)`
- `generate_outline(self, raw_elements)`
- `resolve_label(self, label)`

## Dependencies

**Imports** (6):
- `dataclasses.dataclass`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
