#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
LLM_CONTEXT_START

## Source: src-old/core/base/logic/tts_service.description.md

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
## Source: src-old/core/base/logic/tts_service.improvements.md

# Improvements for tts_service

**File**: `src\core\base\logic\tts_service.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 313 lines (medium)  
**Complexity**: 18 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `tts_service_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""
Text-to-Speech Service
=====================

Inspired by Coqui TTS API patterns.
Provides unified interface for text-to-speech synthesis.
"""

import io
import logging
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, Union
from abc import ABC, abstractmethod

import numpy as np


class TTSEngine(ABC):
    """Abstract base class for TTS engines."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def synthesize(
        self,
        text: str,
        speaker: Optional[str] = None,
        language: Optional[str] = None,
        **kwargs
    ) -> bytes:
        """Synthesize speech from text."""
        pass

    @abstractmethod
    def get_speakers(self) -> list[str]:
        """Get available speakers."""
        return []

    @abstractmethod
    def get_languages(self) -> list[str]:
        """Get available languages."""
        return []


class CoquiTTSEngine(TTSEngine):
    """
    Coqui TTS engine implementation.

    Inspired by Coqui TTS API patterns.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._tts = None
        self._initialized = False

    def _ensure_initialized(self):
        """Lazy initialization of TTS model."""
        if self._initialized:
            return

        try:
            # Import Coqui TTS (inspired by their API)
            from TTS.api import TTS as CoquiTTS

            model_name = self.config.get("model_name", "tts_models/en/ljspeech/tacotron2-DDC")
            self._tts = CoquiTTS(model_name)

            self._initialized = True
            self.logger.info(f"Initialized Coqui TTS with model: {model_name}")

        except ImportError:
            self.logger.warning("Coqui TTS not available. Install with: pip install coqui-tts")
            # Fallback to mock implementation
            self._tts = None
        except Exception as e:
            self.logger.error(f"Failed to initialize Coqui TTS: {e}")
            self._tts = None

    def synthesize(
        self,
        text: str,
        speaker: Optional[str] = None,
        language: Optional[str] = None,
        **kwargs
    ) -> bytes:
        """Synthesize speech using Coqui TTS."""
        self._ensure_initialized()

        if self._tts is None:
            # Mock implementation for when TTS is not available
            return self._mock_synthesize(text)

        try:
            # Use Coqui TTS API pattern
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = temp_file.name

            # Generate speech to file
            self._tts.tts_to_file(
                text=text,
                speaker=speaker,
                language=language,
                file_path=temp_path,
                **kwargs
            )

            # Read the generated audio
            with open(temp_path, "rb") as f:
                audio_data = f.read()

            # Clean up
            Path(temp_path).unlink(missing_ok=True)

            return audio_data

        except Exception as e:
            self.logger.error(f"TTS synthesis failed: {e}")
            return self._mock_synthesize(text)

    def _mock_synthesize(self, text: str) -> bytes:
        """Mock TTS synthesis for when real TTS is not available."""
        # Generate a simple sine wave as placeholder
        sample_rate = 22050
        duration = min(len(text) * 0.1, 3.0)  # 0.1 seconds per character, max 3 seconds

        t = np.linspace(0, duration, int(sample_rate * duration), False)
        frequency = 440  # A4 note
        audio = np.sin(frequency * 2 * np.pi * t)

        # Convert to 16-bit PCM
        audio_int16 = (audio * 32767).astype(np.int16)

        # Create WAV header
        wav_header = self._create_wav_header(len(audio_int16) * 2, sample_rate)

        return wav_header + audio_int16.tobytes()

    def _create_wav_header(self, data_size: int, sample_rate: int) -> bytes:
        """Create a simple WAV header."""
        header = b'RIFF'
        header += (36 + data_size).to_bytes(4, 'little')
        header += b'WAVE'
        header += b'fmt '
        header += (16).to_bytes(4, 'little')  # Subchunk1Size
        header += (1).to_bytes(2, 'little')   # AudioFormat (PCM)
        header += (1).to_bytes(2, 'little')   # NumChannels
        header += sample_rate.to_bytes(4, 'little')
        header += (sample_rate * 2).to_bytes(4, 'little')  # ByteRate
        header += (2).to_bytes(2, 'little')   # BlockAlign
        header += (16).to_bytes(2, 'little')  # BitsPerSample
        header += b'data'
        header += data_size.to_bytes(4, 'little')
        return header

    def get_speakers(self) -> list[str]:
        """Get available speakers."""
        self._ensure_initialized()

        if self._tts and hasattr(self._tts, 'speakers'):
            return self._tts.speakers or []

        return ["default_speaker"]

    def get_languages(self) -> list[str]:
        """Get available languages."""
        self._ensure_initialized()

        if self._tts and hasattr(self._tts, 'languages'):
            return self._tts.languages or []

        return ["en"]


class TTSService:
    """
    Unified Text-to-Speech service.

    Provides a single interface for various TTS engines.
    """

    def __init__(self, default_engine: str = "coqui"):
        self.engines: Dict[str, TTSEngine] = {}
        self.default_engine = default_engine
        self.logger = logging.getLogger(__name__)

        # Register default engines
        self.register_engine("coqui", CoquiTTSEngine())

    def register_engine(self, name: str, engine: TTSEngine):
        """Register a TTS engine."""
        self.engines[name] = engine
        self.logger.info(f"Registered TTS engine: {name}")

    def synthesize(
        self,
        text: str,
        engine: Optional[str] = None,
        speaker: Optional[str] = None,
        language: Optional[str] = None,
        **kwargs
    ) -> bytes:
        """
        Synthesize speech from text.

        Args:
            text: Text to synthesize
            engine: TTS engine to use (default: configured default)
            speaker: Speaker voice to use
            language: Language for synthesis
            **kwargs: Additional engine-specific parameters

        Returns:
            Audio data as bytes
        """
        engine_name = engine or self.default_engine

        if engine_name not in self.engines:
            available = list(self.engines.keys())
            raise ValueError(f"Engine '{engine_name}' not found. Available: {available}")

        engine_instance = self.engines[engine_name]

        self.logger.info(f"Synthesizing text with {engine_name} engine (length: {len(text)})")

        return engine_instance.synthesize(text, speaker, language, **kwargs)

    def get_available_engines(self) -> list[str]:
        """Get available TTS engines."""
        return list(self.engines.keys())

    def get_engine_info(self, engine: Optional[str] = None) -> Dict[str, Any]:
        """Get information about a TTS engine."""
        engine_name = engine or self.default_engine

        if engine_name not in self.engines:
            return {}

        engine_instance = self.engines[engine_name]

        return {
            "name": engine_name,
            "speakers": engine_instance.get_speakers(),
            "languages": engine_instance.get_languages(),
            "type": engine_instance.__class__.__name__
        }

    def save_audio(self, audio_data: bytes, filename: str, format: str = "wav"):
        """Save audio data to file."""
        with open(filename, "wb") as f:
            f.write(audio_data)

        self.logger.info(f"Saved audio to {filename}")

    async def synthesize_streaming(
        self,
        text: str,
        engine: Optional[str] = None,
        **kwargs
    ) -> bytes:
        """
        Streaming synthesis (placeholder for future implementation).

        For now, just calls regular synthesize. In a real implementation,
        this would stream audio chunks as they're generated.
        """
        # In a real implementation, this would yield audio chunks
        return self.synthesize(text, engine, **kwargs)


# Convenience functions
def text_to_speech(
    text: str,
    output_file: Optional[str] = None,
    engine: str = "coqui",
    **kwargs
) -> bytes:
    """
    Convenience function for text-to-speech.

    Args:
        text: Text to synthesize
        output_file: Optional file path to save audio
        engine: TTS engine to use
        **kwargs: Additional parameters

    Returns:
        Audio data as bytes
    """
    service = TTSService()
    audio_data = service.synthesize(text, engine, **kwargs)

    if output_file:
        service.save_audio(audio_data, output_file)

    return audio_data
