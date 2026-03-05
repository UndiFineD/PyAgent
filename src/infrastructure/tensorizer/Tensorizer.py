# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Tensorizer: High-performance model serialization and loading.
(Facade for modular implementation)
"""

from .core import (
    TensorizerConfig,
    CompressionType,
    TensorDtype,
    TensorMetadata,
    TensorizerWriter,
    TensorizerReader,
    StreamingTensorizerReader,
    save_model,
    load_model,
    get_model_info,
)

# Backward compatibility aliases
__all__ = [
    "TensorizerConfig",
    "CompressionType",
    "TensorDtype",
    "TensorMetadata",
    "TensorizerWriter",
    "TensorizerReader",
    "StreamingTensorizerReader",
    "save_model",
    "load_model",
    "get_model_info",
]

def save_tensors(path, tensors, compression=CompressionType.NONE, verify=True):
    """Legacy alias for save_model."""
    return save_model(path, tensors, compression, verify)

def load_tensors(path, parallel=True, verify=True):
    """Legacy alias for load_model."""
    return load_model(path, parallel, verify)