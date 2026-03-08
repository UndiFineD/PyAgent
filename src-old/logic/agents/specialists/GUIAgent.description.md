# GUIAgent

**File**: `src\logic\agents\specialists\GUIAgent.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 15 imports  
**Lines**: 288  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for GUIAgent.

## Classes (5)

### `Framework`

**Inherits from**: Enum

Class Framework implementation.

### `ElementType`

**Inherits from**: Enum

Class ElementType implementation.

### `UIElement`

Represents a UI element with properties.

### `UIAction`

Represents an action to perform on a UI.

### `GUIAgent`

**Inherits from**: BaseAgent

Agent specializing in interacting with and designing GUIs.
Can generate layout code (Qt, React, Tkinter) and interpret UI snapshots.

**Methods** (3):
- `__init__(self, file_path)`
- `get_cached_elements(self)`
- `get_action_history(self)`

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `json`
- `logging`
- `re`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.BaseUtilities.as_tool`
- `src.core.base.Version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
