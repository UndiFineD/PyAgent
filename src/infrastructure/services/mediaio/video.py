# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Video loader implementation.
"""

from __future__ import annotations

from typing import BinaryIO, Tuple, Union

import numpy as np

from .base import MediaLoader
from .models import (
    MediaLoadConfig,
    MediaMetadata,
    MediaType,
    VideoData,
    VideoFormat,
)


class VideoLoader(MediaLoader):
    """Load and process videos."""

    def __init__(self):
        self._cv2_available = False
        try:
            import cv2
            self._cv2_available = True
            self._cv2 = cv2
        except ImportError:
            pass

    def supports(self, media_type: MediaType) -> bool:
        return media_type == MediaType.VIDEO

    async def load(
        self,
        source: Union[str, bytes, BinaryIO],
        config: MediaLoadConfig,
    ) -> VideoData:
        """Load video from source."""
        if not self._cv2_available:
            raise RuntimeError("OpenCV required for video loading")

        if isinstance(source, bytes):
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
                f.write(source)
                path = f.name
            source_str = "<bytes>"
        else:
            path = str(source)
            source_str = path

        frames, timestamps, metadata = await self._load_frames(path, config)
        return VideoData(
            frames=frames,
            metadata=metadata,
            source=source_str,
            timestamps=timestamps,
        )

    async def _load_frames(
        self,
        path: str,
        config: MediaLoadConfig
    ) -> Tuple[np.ndarray, np.ndarray, MediaMetadata]:
        """Load frames from video file."""
        cap = self._cv2.VideoCapture(path)
        try:
            fps = cap.get(self._cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(self._cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(self._cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(self._cv2.CAP_PROP_FRAME_HEIGHT))
            duration = total_frames / fps if fps > 0 else 0

            if config.frame_rate and config.frame_rate < fps:
                step = fps / config.frame_rate
                indices = [int(i * step) for i in range(int(total_frames / step))]
            else:
                indices = list(range(total_frames))

            if len(indices) > config.max_frames:
                step = len(indices) / config.max_frames
                indices = [indices[int(i * step)] for i in range(config.max_frames)]

            frames = []
            timestamps = []
            for idx in indices:
                cap.set(self._cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if ret:
                    frame = self._cv2.cvtColor(frame, self._cv2.COLOR_BGR2RGB)
                    if config.target_size:
                        frame = self._cv2.resize(
                            frame,
                            config.target_size,
                            interpolation=self._cv2.INTER_LINEAR
                        )
                    frames.append(frame)
                    timestamps.append(idx / fps if fps > 0 else 0)

            frames_arr = np.stack(frames, axis=0).astype(np.float32)
            timestamps_arr = np.array(timestamps, dtype=np.float32)
            if config.normalize:
                frames_arr = frames_arr / 255.0
                mean = np.array(config.mean, dtype=np.float32).reshape(1, 1, 1, 3)
                std = np.array(config.std, dtype=np.float32).reshape(1, 1, 1, 3)
                frames_arr = (frames_arr - mean) / std

            metadata = MediaMetadata(
                media_type=MediaType.VIDEO,
                format=VideoFormat.MP4,
                width=width,
                height=height,
                channels=3,
                duration=duration,
                frame_count=len(frames),
            )
            return frames_arr, timestamps_arr, metadata
        finally:
            cap.release()
