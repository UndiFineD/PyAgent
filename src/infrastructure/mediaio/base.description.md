# base

**File**: `src\infrastructure\mediaio\base.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 13 imports  
**Lines**: 41  
**Complexity**: 2 (simple)

## Overview

Base loader class for all media types.

## Classes (1)

### `MediaLoader`

**Inherits from**: ABC

Abstract base class for media loaders.

**Methods** (2):
- `supports(self, media_type)`
- `compute_hash(self, data)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `hashlib`
- `models.AudioData`
- `models.ImageData`
- `models.MediaLoadConfig`
- `models.MediaType`
- `models.VideoData`
- `typing.BinaryIO`
- `typing.Optional`
- `typing.Tuple`
- `typing.Union`

---
*Auto-generated documentation*
