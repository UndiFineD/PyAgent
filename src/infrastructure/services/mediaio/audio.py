# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Audio loader implementation.
"""

from __future__ import annotations

import io
from pathlib import Path
from typing import BinaryIO, Tuple, Union

try:
    import rust_core as rc
except ImportError:
    rc = None


class AudioLoader(MediaLoader):
from .models import (
    AudioData,
    AudioFormat,
    MediaLoadConfig,
    MediaMetadata,
    MediaType,
)


class AudioLoader(MediaLoader):
    """Load and process audio."""

    def __init__(self):
        self._scipy_available = False
        self._librosa_available = False
        try:
            from scipy.io import wavfile
            self._scipy_available = True
            self._wavfile = wavfile
        except ImportError:
            pass
        try:
            import librosa
            self._librosa_available = True
            self._librosa = librosa
        except ImportError:
            pass

    def supports(self, media_type: MediaType) -> bool:
        return media_type == MediaType.AUDIO

    async def load(
        self,
        source: Union[str, bytes, BinaryIO],
        config: MediaLoadConfig,
    ) -> AudioData:
        """Load audio from source."""
        if isinstance(source, bytes):
            data = source
            source_str = "<bytes>"
        elif isinstance(source, (str, Path)):
            with open(str(source), 'rb') as f:
                data = f.read()
            source_str = str(source)
        else:
            data = source.read()
            source_str = "<stream>"

        fmt = self._detect_format(data)
        if fmt == AudioFormat.WAV and self._scipy_available:
            waveform, sample_rate = await self._load_wav(data)
        elif self._librosa_available:
            waveform, sample_rate = await self._load_librosa(data, source_str)
        else:
            raise RuntimeError("No audio loading library available")

        if config.target_sample_rate and sample_rate != config.target_sample_rate:
            waveform = self._resample(waveform, sample_rate, config.target_sample_rate)
            sample_rate = config.target_sample_rate

        if config.mono and waveform.ndim > 1:
            waveform = waveform.mean(axis=0)

        max_samples = int(config.max_duration * sample_rate)
        if len(waveform.flatten()) > max_samples:
            if waveform.ndim == 1:
                waveform = waveform[:max_samples]
            else:
                waveform = waveform[:, :max_samples]

        if config.normalize:
            max_val = np.abs(waveform).max()
            if max_val > 0:
                waveform = waveform / max_val

        metadata = MediaMetadata(
            media_type=MediaType.AUDIO,
            format=fmt,
            sample_rate=sample_rate,
            duration=len(waveform.flatten()) / sample_rate,
            channels=waveform.shape[0] if waveform.ndim > 1 else 1,
        )
        return AudioData(waveform=waveform, metadata=metadata, source=source_str)

    def _detect_format(self, data: bytes) -> AudioFormat:
        """Detect audio format from magic bytes."""
        if data[:4] == b'RIFF' and data[8:12] == b'WAVE':
            return AudioFormat.WAV
        elif data[:3] == b'ID3' or data[:2] == b'\xff\xfb':
            return AudioFormat.MP3
        elif data[:4] == b'fLaC':
            return AudioFormat.FLAC
        elif data[:4] == b'OggS':
            return AudioFormat.OGG
        return AudioFormat.WAV

    async def _load_wav(self, data: bytes) -> Tuple[np.ndarray, int]:
        """Load WAV using scipy."""
        sample_rate, waveform = self._wavfile.read(io.BytesIO(data))
        waveform = waveform.astype(np.float32)
        if waveform.dtype == np.int16:
            waveform = waveform / 32768.0
        elif waveform.dtype == np.int32:
            waveform = waveform / 2147483648.0
        return waveform, sample_rate

    async def _load_librosa(
        self,
        data: bytes,
        source: str
    ) -> Tuple[np.ndarray, int]:
        """Load audio using librosa."""
        import tempfile
        if source == "<bytes>" or source == "<stream>":
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                f.write(data)
                path = f.name
        else:
            path = source
        waveform, sample_rate = self._librosa.load(path, sr=None)
        return waveform, sample_rate

    def _resample(
        self,
        waveform: np.ndarray,
        orig_sr: int,
        target_sr: int
    ) -> np.ndarray:
        """Resample audio."""
        if rc and hasattr(rc, "resample_audio_rust"):
            if waveform.ndim == 1:
                return np.array(rc.resample_audio_rust(waveform.tolist(), orig_sr, target_sr), dtype=np.float32)
            else:
                # Resample each channel
                resampled_channels = []
                for channel in waveform:
                    resampled_channels.append(rc.resample_audio_rust(channel.tolist(), orig_sr, target_sr))
                return np.array(resampled_channels, dtype=np.float32)

        if self._librosa_available:
            return self._librosa.resample(waveform, orig_sr=orig_sr, target_sr=target_sr)
        ratio = target_sr / orig_sr
        new_length = int(len(waveform) * ratio)
        indices = np.linspace(0, len(waveform) - 1, new_length)
        return np.interp(indices, np.arange(len(waveform)), waveform)
