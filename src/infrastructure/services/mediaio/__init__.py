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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Media IO package for unified media loading and processing.
"""

from .audio import AudioLoader  # noqa: F401
from .base import MediaLoader  # noqa: F401
from .engine import (MediaIOEngine, create_media_engine, load_audio,  # noqa: F401
                     load_image, load_video)
from .image import ImageLoader  # noqa: F401
from .models import (AudioData, AudioFormat, ImageData, ImageFormat,  # noqa: F401
                     MediaLoadConfig, MediaMetadata, MediaType, ResizeMode,
                     VideoData, VideoFormat)
from .video import VideoLoader  # noqa: F401

__all__ = [
    "MediaType",
    "ImageFormat",
    "VideoFormat",
    "AudioFormat",
    "ResizeMode",
    "MediaMetadata",
    "ImageData",
    "VideoData",
    "AudioData",
    "MediaLoadConfig",
    "MediaLoader",
    "ImageLoader",
    "VideoLoader",
    "AudioLoader",
    "MediaIOEngine",
    "create_media_engine",
    "load_image",
    "load_video",
    "load_audio",
]
