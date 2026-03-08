# VoiceAgent

**File**: `src\classes\specialized\VoiceAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 92  
**Complexity**: 7 (moderate)

## Overview

Agent specializing in voice-to-text and multimedia processing.
Integrates with fleet for voice-driven commands.

## Classes (1)

### `VoiceAgent`

**Inherits from**: BaseAgent

Handles voice interactions and audio processing with paralinguistic support.

**Methods** (7):
- `__init__(self, file_path)`
- `synthesize_advanced_speech(self, text, reference_voice_path, language_code)`
- `inject_speaker_embedding(self, reference_audio_path)`
- `transcribe_audio(self, audio_file_path, strategy)`
- `apply_voice_activity_detection(self, audio_file_path)`
- `generate_speech(self, text, output_path)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `logging`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `typing.Optional`

---
*Auto-generated documentation*
