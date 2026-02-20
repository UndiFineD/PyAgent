#!/usr/bin/env python3

from __future__ import annotations



# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Unified media loading engine.
"""
try:

"""
import asyncio
except ImportError:
    import asyncio

try:
    import hashlib
except ImportError:
    import hashlib

try:
    from pathlib import Path
except ImportError:
    from pathlib import Path

try:
    from typing import Any, BinaryIO, Dict, List, Optional, Tuple, Union
except ImportError:
    from typing import Any, BinaryIO, Dict, List, Optional, Tuple, Union


try:
    from .audio import AudioLoader
except ImportError:
    from .audio import AudioLoader

try:
    from .base import MediaLoader
except ImportError:
    from .base import MediaLoader

try:
    from .image import ImageLoader
except ImportError:
    from .image import ImageLoader

try:
    from .models import AudioData, ImageData, MediaLoadConfig, MediaType, VideoData
except ImportError:
    from .models import AudioData, ImageData, MediaLoadConfig, MediaType, VideoData

try:
    from .video import VideoLoader
except ImportError:
    from .video import VideoLoader




class MediaIOEngine:
"""
Unified media loading engine.
    def __init__(self, config: Optional[MediaLoadConfig] = None):
        self.config = config or MediaLoadConfig()
        self._loaders: Dict[MediaType, MediaLoader] = {}
        self._cache: Dict[str, Any] = {}

        # Register default loaders
        self._loaders[MediaType.IMAGE] = ImageLoader()
        self._loaders[MediaType.VIDEO] = VideoLoader()
        self._loaders[MediaType.AUDIO] = AudioLoader()

    def register_loader(self, media_type: MediaType, loader: MediaLoader):
"""
        Register custom loader for media type.        self._loaders[media_type] = loader

        async def load(
        self,
        source: Union[str, bytes, BinaryIO],
        media_type: Optional[MediaType] = None,
        config: Optional[MediaLoadConfig] = None,
        ) -> Union[ImageData, VideoData, AudioData]:
"""
        Load media from source.        cfg = config or self.config
        if media_type is None:
        media_type = self._detect_media_type(source)

        cache_key = self._compute_cache_key(source, media_type)
        if cfg.enable_cache and cache_key in self._cache:
        return self._cache[cache_key]

        loader = self._loaders.get(media_type)
        if loader is None:
        raise ValueError(f"No loader for media type: {media_type}")
        result = await loader.load(source, cfg)
        if cfg.enable_cache:
        self._cache[cache_key] = result
        return result

        async def load_batch(
        self,
        sources: List[Union[str, bytes]],
        media_type: Optional[MediaType] = None,
        config: Optional[MediaLoadConfig] = None,
        ) -> List[Union[ImageData, VideoData, AudioData]]:
"""
        Load multiple media files concurrently.        tasks = [self.load(source, media_type, config) for source in sources]
        return await asyncio.gather(*tasks)

    def _detect_media_type(self, source: Union[str, bytes, BinaryIO]) -> MediaType:
"""
Detect media type from source.        if isinstance(source, (str, Path)):
            ext = Path(str(source)).suffix.lower()
            if ext in (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tiff", ".heic"):"                return MediaType.IMAGE
            elif ext in (".mp4", ".webm", ".avi", ".mov", ".mkv"):"                return MediaType.VIDEO
            elif ext in (".wav", ".mp3", ".flac", ".ogg", ".m4a"):"                return MediaType.AUDIO
        return MediaType.IMAGE

    def _compute_cache_key(self, source: Union[str, bytes, BinaryIO], media_type: MediaType) -> str:
"""
Compute cache key for media.        if isinstance(source, str):
            return f"{media_type.name}:{source}""        elif isinstance(source, bytes):
            h = hashlib.blake2b(source, digest_size=16).hexdigest()
            return f"{media_type.name}:{h}""        return """
def clear_cache(self):
"""
Clear media cache.        self._cache.clear()


def create_media_engine(
    target_size: Optional[Tuple[int, int]] = None,
    normalize: bool = True,
    use_gpu: bool = True,
) -> MediaIOEngine:
"""
Create media IO engine with default config.    config = MediaLoadConfig(
        target_size=target_size,
        normalize=normalize,
        use_gpu_decode=use_gpu,
    )
    return MediaIOEngine(config)


async def load_image(
    source: Union[str, bytes],
    size: Optional[Tuple[int, int]] = None,
    normalize: bool = True,
) -> ImageData:
"""
Convenience function to load single image.    config = MediaLoadConfig(target_size=size, normalize=normalize)
    engine = MediaIOEngine(config)
    return await engine.load(source, MediaType.IMAGE)


async def load_video(
    source: Union[str, bytes],
    max_frames: int = 32,
    size: Optional[Tuple[int, int]] = None,
) -> VideoData:
"""
Convenience function to load video.    config = MediaLoadConfig(
        target_size=size,
        max_frames=max_frames,
    )
    engine = MediaIOEngine(config)
    return await engine.load(source, MediaType.VIDEO)


async def load_audio(
    source: Union[str, bytes],
    sample_rate: int = 16000,
    max_duration: float = 30.0,
) -> AudioData:
"""
Convenience function to load audio.    config = MediaLoadConfig(
        target_sample_rate=sample_rate,
        max_duration=max_duration,
    )
    engine = MediaIOEngine(config)
    return await engine.load(source, MediaType.AUDIO)

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""
