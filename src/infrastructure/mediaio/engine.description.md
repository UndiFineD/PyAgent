# engine

**File**: `src\infrastructure\mediaio\engine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 1 functions, 20 imports  
**Lines**: 161  
**Complexity**: 6 (moderate)

## Overview

Unified media loading engine.

## Classes (1)

### `MediaIOEngine`

Unified media loading engine.

**Methods** (5):
- `__init__(self, config)`
- `register_loader(self, media_type, loader)`
- `_detect_media_type(self, source)`
- `_compute_cache_key(self, source, media_type)`
- `clear_cache(self)`

## Functions (1)

### `create_media_engine(target_size, normalize, use_gpu)`

Create media IO engine with default config.

## Dependencies

**Imports** (20):
- `__future__.annotations`
- `asyncio`
- `audio.AudioLoader`
- `base.MediaLoader`
- `hashlib`
- `image.ImageLoader`
- `models.AudioData`
- `models.ImageData`
- `models.MediaLoadConfig`
- `models.MediaType`
- `models.VideoData`
- `pathlib.Path`
- `typing.Any`
- `typing.BinaryIO`
- `typing.Dict`
- ... and 5 more

---
*Auto-generated documentation*
