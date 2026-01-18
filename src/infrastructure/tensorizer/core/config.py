# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Enums and configuration for tensorizer."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
import numpy as np


class TensorDtype(Enum):
    """Supported tensor data types."""
    FLOAT32 = "float32"
    FLOAT16 = "float16"
    BFLOAT16 = "bfloat16"
    INT8 = "int8"
    UINT8 = "uint8"
    INT32 = "int32"
    INT64 = "int64"


class CompressionType(Enum):
    """Supported compression types."""
    NONE = "none"
    ZSTD = "zstd"
    LZ4 = "lz4"
    GZIP = "gzip"


# Magic bytes for file format
TENSORIZER_MAGIC = b"TNSR"
TENSORIZER_VERSION = 2


# Dtype mapping
DTYPE_MAP = {
    TensorDtype.FLOAT32: (np.float32, 4),
    TensorDtype.FLOAT16: (np.float16, 2),
    TensorDtype.INT8: (np.int8, 1),
    TensorDtype.UINT8: (np.uint8, 1),
    TensorDtype.INT32: (np.int32, 4),
    TensorDtype.INT64: (np.int64, 8),
}


@dataclass
class TensorizerConfig:
    """Configuration for tensorizer operations."""
    compression: CompressionType = CompressionType.NONE
    compression_level: int = 3
    verify_checksums: bool = True
    parallel_threads: int = 4
    use_mmap: bool = True
    chunk_size: int = 64 * 1024 * 1024  # 64MB chunks
    encryption_key: Optional[bytes] = None
