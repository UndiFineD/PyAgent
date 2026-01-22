# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Multimodal input processing infrastructure.

Phase 26: Unified handling for image, video, audio, and text modalities.
"""

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
