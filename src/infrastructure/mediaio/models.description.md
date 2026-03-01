# models

**File**: `src\infrastructure\mediaio\models.py`  
**Type**: Python Module  
**Summary**: 10 classes, 0 functions, 11 imports  
**Lines**: 153  
**Complexity**: 5 (moderate)

## Overview

Models and configurations for media loading.

## Classes (10)

### `MediaType`

**Inherits from**: Enum

Supported media types.

### `ImageFormat`

**Inherits from**: Enum

Supported image formats.

### `VideoFormat`

**Inherits from**: Enum

Supported video formats.

### `AudioFormat`

**Inherits from**: Enum

Supported audio formats.

### `ResizeMode`

**Inherits from**: Enum

Image resize modes.

### `MediaMetadata`

Metadata for loaded media.

### `ImageData`

Loaded image data.

**Methods** (3):
- `shape(self)`
- `height(self)`
- `width(self)`

### `VideoData`

Loaded video data.

**Methods** (1):
- `frame_count(self)`

### `AudioData`

Loaded audio data.

**Methods** (1):
- `duration(self)`

### `MediaLoadConfig`

Configuration for media loading.

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `numpy`
- `typing.Any`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`
- `typing.Union`

---
*Auto-generated documentation*
