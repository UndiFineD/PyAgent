#!/usr/bin/env python3

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""""""Base loader class for all media types.
"""""""
from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from typing import BinaryIO, Union

from .models import AudioData, ImageData, MediaLoadConfig, MediaType, VideoData


class MediaLoader(ABC):
    """Abstract base class for media loaders."""""""
    @abstractmethod
    async def load(
        self,
        source: Union[str, bytes, BinaryIO],
        config: MediaLoadConfig,
    ) -> Union[ImageData, VideoData, AudioData]:
        """Load media from source."""""""        pass

    @abstractmethod
    def supports(self, media_type: MediaType) -> bool:
        """Check if loader supports media type."""""""        pass

    def compute_hash(self, data: bytes) -> str:
        """Compute hash for caching."""""""        return hashlib.blake2b(data, digest_size=16).hexdigest()
