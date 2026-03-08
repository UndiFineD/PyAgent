# ClassificationAgent

**File**: `src\logic\agents\specialists\ClassificationAgent.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 15 imports  
**Lines**: 291  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for ClassificationAgent.

## Classes (4)

### `ClassificationType`

**Inherits from**: Enum

Class ClassificationType implementation.

### `ClassificationResult`

Represents a classification result with confidence.

### `Taxonomy`

Represents a hierarchical category taxonomy.

### `ClassificationAgent`

**Inherits from**: BaseAgent

Agent specializing in classifying text, code, or images into predefined categories.
Supports single-label, multi-label, and hierarchical classification.

**Methods** (5):
- `__init__(self, file_path)`
- `_build_single_label_prompt(self, content, categories, descriptions)`
- `_build_multi_label_prompt(self, content, categories, descriptions, top_k)`
- `_build_hierarchical_prompt(self, content, categories, hierarchy, descriptions)`
- `_build_binary_prompt(self, content, categories)`

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
