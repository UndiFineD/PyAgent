# ai_talking_head_core

**File**: `src\core\base\logic\core\ai_talking_head_core.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 16 imports  
**Lines**: 501  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for ai_talking_head_core.

## Classes (5)

### `TalkingHeadRequest`

Request for talking head video generation

### `TalkingHeadResult`

Result of talking head generation

### `FaceAlignmentResult`

Face alignment and pose estimation result

### `AudioFeatures`

Extracted audio features for lip sync

### `AITalkingHeadCore`

**Inherits from**: BaseCore

AI Talking Head Core for audio-visual controlled video generation.

Provides capabilities for generating natural talking head videos from audio,
text, and reference images using advanced diffusion and state space models.

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (16):
- `PIL.Image`
- `asyncio`
- `base64`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `io`
- `json`
- `numpy`
- `src.core.base.logic.core.base_core.BaseCore`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`
- ... and 1 more

---
*Auto-generated documentation*
