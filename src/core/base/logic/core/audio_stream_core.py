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

import audioop


class AudioStreamCore:
    """
    Core logic for real-time audio processing and codec conversion.
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
            self.resample_state
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
