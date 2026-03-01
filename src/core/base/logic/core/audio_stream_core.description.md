# audio_stream_core

**File**: `src\core\base\logic\core\audio_stream_core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 61  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for audio_stream_core.

## Classes (1)

### `AudioStreamCore`

Core logic for real-time audio processing and codec conversion.
Harvested from .external/Asterisk-AI-Voice-Agent.

**Methods** (5):
- `__init__(self, target_sample_rate, target_width)`
- `convert_ulaw_to_pcm(self, ulaw_data)`
- `resample(self, pcm_data, source_rate)`
- `normalize_volume(self, pcm_data, target_rms)`
- `detect_voice(self, pcm_data, threshold)`

## Dependencies

**Imports** (3):
- `audioop`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
