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
Multimodal input processing infrastructure.

Phase 26: Unified handling for image, video, audio, and text modalities.
"""

<<<<<<< HEAD
from .multi_modal_processor import (MULTIMODAL_REGISTRY, AudioProcessor,  # noqa: F401
                                    BaseMultiModalProcessor, ImageProcessor,
                                    ModalityType, MultiModalConfig,
                                    MultiModalData, MultiModalInputs,
                                    MultiModalRegistry, PlaceholderInfo,
                                    TextEmbedProcessor, VideoProcessor,
                                    get_placeholder_tokens,
                                    process_multimodal_inputs)
from .muxer import ChannelType, Muxer  # noqa: F401
from .quantized_engine import QuantizedMultimediaEngine  # noqa: F401
from .tensorrt_loader import TensorRTLoader  # noqa: F401
=======
from .multi_modal_processor import (
    ModalityType,
    MultiModalConfig,
    MultiModalData,
    MultiModalInputs,
    PlaceholderInfo,
    BaseMultiModalProcessor,
    ImageProcessor,
    VideoProcessor,
    AudioProcessor,
    TextEmbedProcessor,
    MultiModalRegistry,
    MULTIMODAL_REGISTRY,
    process_multimodal_inputs,
    get_placeholder_tokens,
)
from .muxer import Muxer, ChannelType
from .quantized_engine import QuantizedMultimediaEngine
from .tensorrt_loader import TensorRTLoader
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

__all__ = [
    # Enums and config
    "ModalityType",
    "MultiModalConfig",
    "ChannelType",
    # Data classes
    "MultiModalData",
    "MultiModalInputs",
    "PlaceholderInfo",
    # Processor classes
    "BaseMultiModalProcessor",
    "ImageProcessor",
    "VideoProcessor",
    "AudioProcessor",
    "TextEmbedProcessor",
    "Muxer",
    "QuantizedMultimediaEngine",
    "TensorRTLoader",
    # Registry
    "MultiModalRegistry",
    "MULTIMODAL_REGISTRY",
    # Convenience functions
    "process_multimodal_inputs",
    "get_placeholder_tokens",
]
