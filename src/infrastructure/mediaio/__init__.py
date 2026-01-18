# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 40: Media IO Package

"""
Media IO Engine.

Provides unified media loading with GPU decode support:
- Async image/video/audio loading
- Format-agnostic abstraction
- GPU-accelerated decode (NVDEC)
- Automatic resize and normalization
- Batched processing
"""

from .MediaIOEngine import (
    # Enums
    MediaType,
    ImageFormat,
    VideoFormat,
    AudioFormat,
    ResizeMode,
    
    # Data classes
    MediaMetadata,
    ImageData,
    VideoData,
    AudioData,
    MediaLoadConfig,
    
    # Loaders
    MediaLoader,
    ImageLoader,
    VideoLoader,
    AudioLoader,
    
    # Engine
    MediaIOEngine,
    
    # Factory functions
    create_media_engine,
    load_image,
    load_video,
    load_audio,
)

__all__ = [
    # Enums
    "MediaType",
    "ImageFormat",
    "VideoFormat",
    "AudioFormat",
    "ResizeMode",
    
    # Data classes
    "MediaMetadata",
    "ImageData",
    "VideoData",
    "AudioData",
    "MediaLoadConfig",
    
    # Loaders
    "MediaLoader",
    "ImageLoader",
    "VideoLoader",
    "AudioLoader",
    
    # Engine
    "MediaIOEngine",
    
    # Factory functions
    "create_media_engine",
    "load_image",
    "load_video",
    "load_audio",
]
