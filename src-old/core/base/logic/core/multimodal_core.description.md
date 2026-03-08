# multimodal_core

**File**: `src\core\base\logic\core\multimodal_core.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 8 imports  
**Lines**: 93  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for multimodal_core.

## Classes (2)

### `MultimodalChunk`

Represents a piece of interleaved data (text, audio, image).

### `MultimodalCore`

Implements interleaved multimodal token management for 'Omni' models.

Inspired by 'Stream-Omni' and 'FastFlowLM':
- Handles transition between raw media and model-specific tokens.
- Synchronizes audio and visual fragments.

**Methods** (7):
- `__init__(self)`
- `add_text(self, text)`
- `add_audio_token(self, token, timestamp_ms)`
- `add_image_patch(self, image_bytes, bbox)`
- `generate_interleaved_prompt(self, model_family)`
- `clear(self)`
- `get_token_count(self)`

## Dependencies

**Imports** (8):
- `base64`
- `dataclasses.dataclass`
- `dataclasses.field`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Union`

---
*Auto-generated documentation*
