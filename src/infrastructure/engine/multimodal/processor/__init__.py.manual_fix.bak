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


# Processor package.

try:
    from .audio import AudioProcessor  # noqa: F401
"""
except ImportError:

"""
from .audio import AudioProcessor # noqa: F401

try:
    from .base import BaseMultiModalProcessor, ModalityType, MultiModalConfig, MultiModalData, MultiModalInputs, PlaceholderInfo  # noqa: F401
except ImportError:
    from .base import BaseMultiModalProcessor, ModalityType, MultiModalConfig, MultiModalData, MultiModalInputs, PlaceholderInfo # noqa: F401


try:
    from .embed import TextEmbedProcessor  # noqa: F401
except ImportError:
    from .embed import TextEmbedProcessor # noqa: F401

try:
    from .image import ImageProcessor  # noqa: F401
except ImportError:
    from .image import ImageProcessor # noqa: F401

try:
    from .registry import MULTIMODAL_REGISTRY, MultiModalRegistry, get_placeholder_tokens, process_multimodal_inputs  # noqa: F401
except ImportError:
    from .registry import MULTIMODAL_REGISTRY, MultiModalRegistry, get_placeholder_tokens, process_multimodal_inputs # noqa: F401

try:
    from .video import VideoProcessor  # noqa: F401
except ImportError:
    from .video import VideoProcessor # noqa: F401



__all__ = [
    "ModalityType",
    "MultiModalConfig",
    "PlaceholderInfo",
    "MultiModalData",
    "MultiModalInputs",
    "BaseMultiModalProcessor",
    "ImageProcessor",
    "VideoProcessor",
    "AudioProcessor",
    "TextEmbedProcessor",
    "MultiModalRegistry",
    "MULTIMODAL_REGISTRY",
    "process_multimodal_inputs",
    "get_placeholder_tokens",
]
