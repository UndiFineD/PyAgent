# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Utility functions for tensorizer."""

import os
from pathlib import Path
from typing import Any, Dict, Union
import numpy as np
from .config import TensorizerConfig, CompressionType
from .writer import TensorizerWriter
from .reader import TensorizerReader


def save_model(
    path: Union[str, Path],
    tensors: Dict[str, np.ndarray],
    compression: CompressionType = CompressionType.NONE,
    verify: bool = True,
) -> int:
    """
    Convenience function to save a model.
    
    Returns total bytes written.
    """
    config = TensorizerConfig(
        compression=compression,
        verify_checksums=verify,
    )
    
    with TensorizerWriter(path, config) as writer:
        writer.write_model(tensors)
    
    return os.path.getsize(path)


def load_model(
    path: Union[str, Path],
    parallel: bool = True,
    verify: bool = True,
) -> Dict[str, np.ndarray]:
    """
    Convenience function to load a model.
    """
    config = TensorizerConfig(
        verify_checksums=verify,
    )
    
    with TensorizerReader(path, config) as reader:
        if parallel:
            return reader.read_parallel()
        return reader.read_all()


def get_model_info(path: Union[str, Path]) -> Dict[str, Any]:
    """Get information about a tensorizer file without loading tensors."""
    config = TensorizerConfig(use_mmap=True)
    
    with TensorizerReader(path, config) as reader:
        total_size = sum(m.size_bytes for m in reader._metadata.values())
        compressed_size = sum(m.compressed_size for m in reader._metadata.values())
        
        return {
            "num_tensors": reader.num_tensors,
            "tensor_names": reader.tensor_names,
            "total_size_bytes": total_size,
            "compressed_size_bytes": compressed_size,
            "compression_ratio": total_size / max(compressed_size, 1),
            "tensors": {
                name: {
                    "shape": meta.shape,
                    "dtype": meta.dtype.value,
                    "size_bytes": meta.size_bytes,
                }
                for name, meta in reader._metadata.items()
            },
        }
