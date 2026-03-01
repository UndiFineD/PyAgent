# registry

**File**: `src\infrastructure\multimodal\processor\registry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 2 functions, 15 imports  
**Lines**: 186  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for registry.

## Classes (1)

### `MultiModalRegistry`

Central registry for multimodal processors.

**Methods** (5):
- `__init__(self)`
- `register_processor(self, modality, processor)`
- `get_processor(self, modality)`
- `create_processor(self, modality, config)`
- `process_inputs(self, mm_data, config)`

## Functions (2)

### `process_multimodal_inputs(mm_data, config)`

### `get_placeholder_tokens(mm_inputs, modality, token_id)`

## Dependencies

**Imports** (15):
- `audio.AudioProcessor`
- `base.BaseMultiModalProcessor`
- `base.ModalityType`
- `base.MultiModalConfig`
- `base.MultiModalData`
- `base.MultiModalInputs`
- `base.PlaceholderInfo`
- `embed.TextEmbedProcessor`
- `image.ImageProcessor`
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `video.VideoProcessor`

---
*Auto-generated documentation*
