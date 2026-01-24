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
Audio.py module.
"""

from typing import Any, Dict, Optional, Tuple

import numpy as np

from .base import BaseMultiModalProcessor, ModalityType, MultiModalConfig


class AudioProcessor(BaseMultiModalProcessor[Tuple[np.ndarray, int]]):
    """Processor for audio inputs."""

    modality = ModalityType.AUDIO

    def __init__(
        self,
        config: Optional[MultiModalConfig] = None,
        target_sample_rate: int = 16000,
        max_length_seconds: float = 30.0,
        feature_size: int = 80,  # Mel bins
        hop_length: int = 160,
    ):
        super().__init__(config)
        self.target_sample_rate = target_sample_rate
        self.max_length_seconds = max_length_seconds
        self.feature_size = feature_size
        self.hop_length = hop_length

    def process(
        self,
        data: Tuple[np.ndarray, int],
        **kwargs: Any,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        waveform, sample_rate = data
        target_sr = kwargs.get("target_sample_rate", self.target_sample_rate)
        max_len = kwargs.get("max_length_seconds", self.max_length_seconds)

        if waveform.ndim > 1:
            waveform = waveform.mean(axis=-1) if waveform.shape[-1] < waveform.shape[0] else waveform.mean(axis=0)

        if sample_rate != target_sr:
            waveform = self._resample(waveform, sample_rate, target_sr)
            sample_rate = target_sr

        max_samples = int(max_len * sample_rate)
        original_length = len(waveform)
        if len(waveform) > max_samples:
            waveform = waveform[:max_samples]

        num_frames = max(1, len(waveform) // self.hop_length)
        features = np.zeros((num_frames, self.feature_size), dtype=np.float32)

        for i in range(num_frames):
            start = i * self.hop_length
            end = min(start + self.hop_length * 2, len(waveform))
            segment = waveform[start:end]
            if segment.size > 0:
                features[i, 0] = np.sqrt(np.mean(segment**2))

        metadata = {
            "original_sample_rate": sample_rate,
            "original_length": original_length,
            "processed_length": len(waveform),
            "num_frames": num_frames,
            "feature_size": self.feature_size,
            "duration_seconds": len(waveform) / sample_rate,
        }

        return features, metadata

    def get_placeholder_count(
        self,
        data: Tuple[np.ndarray, int],
        **kwargs: Any,
    ) -> int:
        waveform, sample_rate = data
        target_sr = kwargs.get("target_sample_rate", self.target_sample_rate)
        max_len = kwargs.get("max_length_seconds", self.max_length_seconds)

        duration = min(len(waveform) / sample_rate, max_len)
        num_samples = int(duration * target_sr)
        num_frames = max(1, num_samples // self.hop_length)

        return num_frames

    def _resample(
        self,
        waveform: np.ndarray,
        src_rate: int,
        tgt_rate: int,
    ) -> np.ndarray:
        if src_rate == tgt_rate:
            return waveform

        ratio = tgt_rate / src_rate
        new_length = int(len(waveform) * ratio)
        indices = np.arange(new_length) / ratio
        indices = np.clip(indices, 0, len(waveform) - 1)

        idx_floor = np.floor(indices).astype(int)
        idx_ceil = np.minimum(idx_floor + 1, len(waveform) - 1)
        weights = indices - idx_floor

        resampled = waveform[idx_floor] * (1 - weights) + waveform[idx_ceil] * weights
        return resampled.astype(np.float32)
