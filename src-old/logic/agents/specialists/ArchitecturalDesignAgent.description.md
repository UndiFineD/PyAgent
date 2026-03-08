# ArchitecturalDesignAgent

**File**: `src\logic\agents\specialists\ArchitecturalDesignAgent.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 13 imports  
**Lines**: 245  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for ArchitecturalDesignAgent.

## Classes (3)

### `DesignPhase`

**Inherits from**: Enum

Class DesignPhase implementation.

### `DesignExpertise`

**Inherits from**: Enum

Class DesignExpertise implementation.

### `ArchitecturalDesignAgent`

**Inherits from**: BaseAgent

Agent specializing in hierarchical architectural design workflows.
Implements the 5-stage framework identified in 2026 empirical studies
(arXiv:2601.10696, ScienceDirect S2090447925006203) regarding cognitive load 
reduction and performance enhancement in AI-aided design.

**Methods** (3):
- `__init__(self, file_path, expertise)`
- `get_dpo_metrics(self)`
- `get_acceleration_metrics(self)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `asyncio`
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

---
*Auto-generated documentation*
