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

"""LLM_CONTEXT_START

## Source: src-old/core/base/logic/core/audio_stream_core.description.md

# audio_stream_core

**File**: `src\\core\base\\logic\\core\audio_stream_core.py`  
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
## Source: src-old/core/base/logic/core/audio_stream_core.improvements.md

# Improvements for audio_stream_core

**File**: `src\\core\base\\logic\\core\audio_stream_core.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 61 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `audio_stream_core_test.py` with pytest tests

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

import audioop


class AudioStreamCore:
    """Core logic for real-time audio processing and codec conversion.
    Harvested from .external/Asterisk-AI-Voice-Agent.
    """

    def __init__(self, target_sample_rate: int = 16000, target_width: int = 2):
        self.target_sample_rate = target_sample_rate
        self.target_width = target_width  # 2 bytes for 16-bit
        self.resample_state = None

    def convert_ulaw_to_pcm(self, ulaw_data: bytes) -> bytes:
        """Converts u-law coded audio (8kHz, 8-bit) to linear PCM."""
        pcm_data = audioop.ulaw2lin(ulaw_data, self.target_width)
        return pcm_data

    def resample(self, pcm_data: bytes, source_rate: int) -> bytes:
        """Resamples PCM audio to the target sample rate."""
        if source_rate == self.target_sample_rate:
            return pcm_data

        resampled_data, self.resample_state = audioop.ratecv(
            pcm_data,
            self.target_width,
            1,  # channels
            source_rate,
            self.target_sample_rate,
            self.resample_state,
        )
        return resampled_data

    def normalize_volume(self, pcm_data: bytes, target_rms: int = 2000) -> bytes:
        """Normalizes audio volume to a target RMS level."""
        rms = audioop.rms(pcm_data, self.target_width)
        if rms == 0:
            return pcm_data

        factor = target_rms / rms
        return audioop.mul(pcm_data, self.target_width, factor)

    def detect_voice(self, pcm_data: bytes, threshold: int = 500) -> bool:
        """Simple RMS-based voice activity detection."""
        rms = audioop.rms(pcm_data, self.target_width)
        return rms > threshold
