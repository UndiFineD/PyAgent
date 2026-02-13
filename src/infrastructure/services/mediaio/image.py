#!/usr/bin/env python3
# Refactored by copilot-placeholder
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

"""Image loader implementation."""

# pylint: disable=too-many-function-args

from __future__ import annotations

import io
from pathlib import Path
from typing import BinaryIO, Tuple, Union

import numpy as np

from .base import MediaLoader
from .models import (ImageData, ImageFormat, MediaLoadConfig, MediaMetadata,
                     MediaType, ResizeMode)


class ImageLoader(MediaLoader):
    """Load and process images."""

    def __init__(self):
        self._pil_available = False
        self._cv2_available = False
        try:
            from PIL import Image
            self._pil_available = True
            self._image_lib = Image
        except ImportError:
            pass
        try:
            import cv2
            self._cv2_available = True
            self._cv2 = cv2
        except ImportError:
            pass

    def supports(self, media_type: MediaType) -> bool:
        return media_type == MediaType.IMAGE

    async def load(
        self,
        source: Union[str, bytes, BinaryIO],
        config: MediaLoadConfig,
    ) -> ImageData:
        """Load image from source."""
        data, source_str = await self._read_source(source)
        fmt = self._detect_format(data)

        if self._pil_available:
            img = await self._load_pil(data, config)
        elif self._cv2_available:
            img = await self._load_cv2(data, config)
        else:
            raise RuntimeError("No image loading library available")

        metadata = MediaMetadata(
            media_type=MediaType.IMAGE,
            format=fmt,
            width=img.shape[1],
            height=img.shape[0],
            channels=img.shape[2] if img.ndim == 3 else 1,
            file_size=len(data),
            hash=self.compute_hash(data),
        )

        return ImageData(data=img, metadata=metadata, source=source_str)

    async def _read_source(self, source: Union[str, bytes, BinaryIO]) -> Tuple[bytes, str]:
        """Read bytes from source."""
        if isinstance(source, bytes):
            return source, "<bytes>"
        if isinstance(source, (str, Path)):
            source_str = str(source)
            if source_str.startswith(("http://", "https://")):
                data = await self._fetch_url(source_str)
            else:
                with open(source_str, 'rb') as f:
                    data = f.read()
            return data, source_str

        data = source.read()
        return data, "<stream>"

    async def _fetch_url(self, url: str) -> bytes:
        """Fetch image from URL."""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    return await resp.read()
        except ImportError:
            import urllib.request
            with urllib.request.urlopen(url) as resp:
                return resp.read()

    def _detect_format(self, data: bytes) -> ImageFormat:
        """Detect image format from magic bytes."""
        if data[:2] == b"\xff\xd8":
            return ImageFormat.JPEG
        if data[:8] == b"\x89PNG\r\n\x1a\n":
            return ImageFormat.PNG
        if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
            return ImageFormat.WEBP
        if data[:6] in (b"GIF87a", b"GIF89a"):
            return ImageFormat.GIF
        if data[:2] == b"BM":
            return ImageFormat.BMP
        return ImageFormat.JPEG

    async def _load_pil(self, data: bytes, config: MediaLoadConfig) -> np.ndarray:
        """Load using PIL."""
        img = self._image_lib.open(io.BytesIO(data))
        if img.mode != "RGB":
            img = img.convert("RGB")

        if config.target_size:
            img = self._resize_pil(img, config.target_size, config.resize_mode)

        arr = np.array(img, dtype=np.float32)
        if config.normalize:
            arr = arr / 255.0
            mean = np.array(config.mean, dtype=np.float32).reshape(1, 1, 3)
            std = np.array(config.std, dtype=np.float32).reshape(1, 1, 3)
            arr = (arr - mean) / std
        return arr

    def _resize_pil(self, img, target: Tuple[int, int], mode: ResizeMode):
        """Resize image using PIL."""
        w, h = img.size
        tw, th = target

        if mode == ResizeMode.STRETCH:
            return img.resize((tw, th), self._image_lib.Resampling.BICUBIC)

        if mode == ResizeMode.CROP:
            scale = max(tw / w, th / h)
            new_w, new_h = int(w * scale), int(h * scale)
            img = img.resize((new_w, new_h), self._image_lib.Resampling.BICUBIC)
            left = (new_w - tw) // 2
            top = (new_h - th) // 2
            return img.crop((left, top, left + tw, top + th))

        if mode == ResizeMode.PAD:
            scale = min(tw / w, th / h)
            new_w, new_h = int(w * scale), int(h * scale)
            img = img.resize((new_w, new_h), self._image_lib.Resampling.BICUBIC)
            result = self._image_lib.new("RGB", (tw, th), (0, 0, 0))
            left = (tw - new_w) // 2
            top = (th - new_h) // 2
            result.paste(img, (left, top))
            return result

        if mode == ResizeMode.SHORTEST:
            scale = min(tw / w, th / h)
            new_w, new_h = int(w * scale), int(h * scale)
            return img.resize((new_w, new_h), self._image_lib.Resampling.BICUBIC)

        scale = max(tw / w, th / h)
        new_w, new_h = int(w * scale), int(h * scale)
        return img.resize((new_w, new_h), self._image_lib.Resampling.BICUBIC)

    async def _load_cv2(self, data: bytes, config: MediaLoadConfig) -> np.ndarray:
        """Load using OpenCV."""
        arr = np.frombuffer(data, dtype=np.uint8)
        img = self._cv2.imdecode(arr, self._cv2.IMREAD_COLOR)
        img = self._cv2.cvtColor(img, self._cv2.COLOR_BGR2RGB)

        if config.target_size:
            img = self._resize_cv2(img, config.target_size, config.resize_mode)

        img = img.astype(np.float32)
        if config.normalize:
            img = img / 255.0
            mean = np.array(config.mean, dtype=np.float32).reshape(1, 1, 3)
            std = np.array(config.std, dtype=np.float32).reshape(1, 1, 3)
            img = (img - mean) / std
        return img

    def _resize_cv2(self, img: np.ndarray, target: Tuple[int, int], mode: ResizeMode) -> np.ndarray:
        """Resize image using OpenCV."""
        h, w = img.shape[:2]
        tw, th = target

        if mode == ResizeMode.STRETCH:
            return self._cv2.resize(img, (tw, th), interpolation=self._cv2.INTER_LINEAR)

        if mode == ResizeMode.SHORTEST:
            scale = min(tw / w, th / h)
            new_w, new_h = int(w * scale), int(h * scale)
            return self._cv2.resize(img, (new_w, new_h), interpolation=self._cv2.INTER_LINEAR)

        return self._cv2.resize(img, (tw, th), interpolation=self._cv2.INTER_LINEAR)
