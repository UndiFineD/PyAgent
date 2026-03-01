# image

**File**: `src\infrastructure\mediaio\image.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 19 imports  
**Lines**: 217  
**Complexity**: 5 (moderate)

## Overview

Image loader implementation.

## Classes (1)

### `ImageLoader`

**Inherits from**: MediaLoader

Load and process images.

**Methods** (5):
- `__init__(self)`
- `supports(self, media_type)`
- `_detect_format(self, data)`
- `_resize_pil(self, img, target, mode)`
- `_resize_cv2(self, img, target, mode)`

## Dependencies

**Imports** (19):
- `PIL.Image`
- `__future__.annotations`
- `aiohttp`
- `base.MediaLoader`
- `cv2`
- `io`
- `models.ImageData`
- `models.ImageFormat`
- `models.MediaLoadConfig`
- `models.MediaMetadata`
- `models.MediaType`
- `models.ResizeMode`
- `numpy`
- `pathlib.Path`
- `typing.BinaryIO`
- ... and 4 more

---
*Auto-generated documentation*
