# hasher

**File**: `src\infrastructure\multimodal\cache\hasher.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 13 imports  
**Lines**: 143  
**Complexity**: 7 (moderate)

## Overview

Content-aware hasher for multimodal data.

## Classes (1)

### `MultiModalHasher`

Content-aware hasher for multimodal data.

Supports:
- Blake3 for fast cryptographic hashing
- SHA256 for compatibility
- Perceptual hashing for similar image detection

**Methods** (7):
- `__init__(self, algorithm, perceptual_size)`
- `hash_bytes(self, data)`
- `hash_image(self, image_data)`
- `hash_audio(self, audio_data, sample_rate)`
- `hash_video(self, video_data, frame_count)`
- `hash_embedding(self, embedding)`
- `perceptual_hash(self, image_data)`

## Dependencies

**Imports** (13):
- `PIL.Image`
- `blake3`
- `data.MediaHash`
- `enums.HashAlgorithm`
- `enums.MediaType`
- `hashlib`
- `io`
- `numpy`
- `struct`
- `typing.Any`
- `typing.Optional`
- `typing.Tuple`
- `typing.Union`

---
*Auto-generated documentation*
