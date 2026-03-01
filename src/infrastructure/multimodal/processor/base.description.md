# base

**File**: `src\infrastructure\multimodal\processor\base.py`  
**Type**: Python Module  
**Summary**: 6 classes, 0 functions, 21 imports  
**Lines**: 143  
**Complexity**: 11 (moderate)

## Overview

Python module containing implementation for base.

## Classes (6)

### `ModalityType`

**Inherits from**: Enum

Supported modality types for multimodal inputs.

### `MultiModalConfig`

Configuration for multimodal processing.

**Methods** (2):
- `get_limit(self, modality)`
- `get_media_kwargs(self, modality)`

### `PlaceholderInfo`

Information about a placeholder in the token sequence.

**Methods** (1):
- `end_idx(self)`

### `MultiModalData`

Raw multimodal data before processing.

**Methods** (2):
- `is_empty(self)`
- `get_modality_count(self, modality)`

### `MultiModalInputs`

Processed multimodal inputs ready for model consumption.

**Methods** (2):
- `has_multimodal(self)`
- `get_placeholder_count(self)`

### `BaseMultiModalProcessor`

**Inherits from**: ABC, Unknown

Abstract base class for modality-specific processors.

**Methods** (4):
- `__init__(self, config)`
- `process(self, data)`
- `get_placeholder_count(self, data)`
- `compute_hash(self, data)`

## Dependencies

**Imports** (21):
- `PIL.Image`
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `hashlib`
- `logging`
- `numpy`
- `typing.Any`
- `typing.Dict`
- `typing.Generic`
- `typing.List`
- ... and 6 more

---
*Auto-generated documentation*
