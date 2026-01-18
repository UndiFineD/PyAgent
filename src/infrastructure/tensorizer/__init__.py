# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 39: Tensorizer Module

"""
Tensorizer: High-performance model serialization.

Provides:
- TensorizerWriter: Write tensors to tensorizer format
- TensorizerReader: Read tensors from tensorizer format
- StreamingTensorizerReader: Streaming/on-demand tensor loading
- Compression support (zstd, lz4, gzip)
- Parallel loading
- Memory-mapped access
"""

from .Tensorizer import (
    # Enums
    TensorDtype,
    CompressionType,
    
    # Data classes
    TensorMetadata,
    TensorizerConfig,
    LoadProgress,
    
    # Writer
    TensorizerWriter,
    
    # Readers
    TensorizerReader,
    StreamingTensorizerReader,
    
    # Utilities
    save_model,
    load_model,
    get_model_info,
    compress_data,
    decompress_data,
)

__all__ = [
    # Enums
    "TensorDtype",
    "CompressionType",
    
    # Data classes
    "TensorMetadata",
    "TensorizerConfig",
    "LoadProgress",
    
    # Writer
    "TensorizerWriter",
    
    # Readers
    "TensorizerReader",
    "StreamingTensorizerReader",
    
    # Utilities
    "save_model",
    "load_model",
    "get_model_info",
    "compress_data",
    "decompress_data",
]
