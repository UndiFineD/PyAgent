# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Base loader class for all media types.
"""

from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from typing import BinaryIO, Optional, Tuple, Union

from .models import (
    AudioData,
    ImageData,
    MediaLoadConfig,
    MediaType,
    VideoData,
)


class MediaLoader(ABC):
    """Abstract base class for media loaders."""

    @abstractmethod
    async def load(
        self,
        source: Union[str, bytes, BinaryIO],
        config: MediaLoadConfig,
    ) -> Union[ImageData, VideoData, AudioData]:
        """Load media from source."""
        pass

    @abstractmethod
    def supports(self, media_type: MediaType) -> bool:
        """Check if loader supports media type."""
        pass

    def compute_hash(self, data: bytes) -> str:
        """Compute hash for caching."""
        return hashlib.blake2b(data, digest_size=16).hexdigest()
