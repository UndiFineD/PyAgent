# tts_service

**File**: `src\core\base\logic\tts_service.py`  
**Type**: Python Module  
**Summary**: 3 classes, 1 functions, 12 imports  
**Lines**: 313  
**Complexity**: 18 (moderate)

## Overview

Text-to-Speech Service
=====================

Inspired by Coqui TTS API patterns.
Provides unified interface for text-to-speech synthesis.

## Classes (3)

### `TTSEngine`

**Inherits from**: ABC

Abstract base class for TTS engines.

**Methods** (4):
- `__init__(self, config)`
- `synthesize(self, text, speaker, language)`
- `get_speakers(self)`
- `get_languages(self)`

### `CoquiTTSEngine`

**Inherits from**: TTSEngine

Coqui TTS engine implementation.

Inspired by Coqui TTS API patterns.

**Methods** (7):
- `__init__(self, config)`
- `_ensure_initialized(self)`
- `synthesize(self, text, speaker, language)`
- `_mock_synthesize(self, text)`
- `_create_wav_header(self, data_size, sample_rate)`
- `get_speakers(self)`
- `get_languages(self)`

### `TTSService`

Unified Text-to-Speech service.

Provides a single interface for various TTS engines.

**Methods** (6):
- `__init__(self, default_engine)`
- `register_engine(self, name, engine)`
- `synthesize(self, text, engine, speaker, language)`
- `get_available_engines(self)`
- `get_engine_info(self, engine)`
- `save_audio(self, audio_data, filename, format)`

## Functions (1)

### `text_to_speech(text, output_file, engine)`

Convenience function for text-to-speech.

Args:
    text: Text to synthesize
    output_file: Optional file path to save audio
    engine: TTS engine to use
    **kwargs: Additional parameters

Returns:
    Audio data as bytes

## Dependencies

**Imports** (12):
- `TTS.api.TTS`
- `abc.ABC`
- `abc.abstractmethod`
- `io`
- `logging`
- `numpy`
- `pathlib.Path`
- `tempfile`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- `typing.Union`

---
*Auto-generated documentation*
