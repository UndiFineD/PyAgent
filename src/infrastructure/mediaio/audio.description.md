# audio

**File**: `src\infrastructure\mediaio\audio.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 16 imports  
**Lines**: 150  
**Complexity**: 4 (simple)

## Overview

Audio loader implementation.

## Classes (1)

### `AudioLoader`

**Inherits from**: MediaLoader

Load and process audio.

**Methods** (4):
- `__init__(self)`
- `supports(self, media_type)`
- `_detect_format(self, data)`
- `_resample(self, waveform, orig_sr, target_sr)`

## Dependencies

**Imports** (16):
- `__future__.annotations`
- `base.MediaLoader`
- `io`
- `librosa`
- `models.AudioData`
- `models.AudioFormat`
- `models.MediaLoadConfig`
- `models.MediaMetadata`
- `models.MediaType`
- `numpy`
- `pathlib.Path`
- `scipy.io.wavfile`
- `tempfile`
- `typing.BinaryIO`
- `typing.Tuple`
- ... and 1 more

---
*Auto-generated documentation*
