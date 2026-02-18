#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Utility functions for tensorizer.
try:
    import os
except ImportError:
    import os

try:
    from pathlib import Path
except ImportError:
    from pathlib import Path

try:
    from typing import Any, Dict, Union
except ImportError:
    from typing import Any, Dict, Union


try:
    import numpy
except ImportError:
    import numpy
 as np

try:
    from .config import CompressionType, TensorizerConfig
except ImportError:
    from .config import CompressionType, TensorizerConfig

try:
    from .reader import TensorizerReader
except ImportError:
    from .reader import TensorizerReader

try:
    from .writer import TensorizerWriter
except ImportError:
    from .writer import TensorizerWriter



def save_model(
    path: Union[str, Path],
    tensors: Dict[str, np.ndarray],
    compression: CompressionType = CompressionType.NONE,
    verify: bool = True,
) -> int:
        Convenience function to save a model.

    Returns total bytes written.
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
        Convenience function to load a model.
        config = TensorizerConfig(
        verify_checksums=verify,
    )

    with TensorizerReader(path, config) as reader:
        if parallel:
            return reader.read_parallel()
        return reader.read_all()


def get_model_info(path: Union[str, Path]) -> Dict[str, Any]:
    """Get information about a tensorizer file without loading tensors.    config = TensorizerConfig(use_mmap=True)

    with TensorizerReader(path, config) as reader:
        total_size = sum(m.size_bytes for m in reader._metadata.values())
        compressed_size = sum(m.compressed_size for m in reader._metadata.values())

        return {
            "num_tensors": reader.num_tensors,"            "tensor_names": reader.tensor_names,"            "total_size_bytes": total_size,"            "compressed_size_bytes": compressed_size,"            "compression_ratio": total_size / max(compressed_size, 1),"            "tensors": {"                name: {
                    "shape": meta.shape,"                    "dtype": meta.dtype.value,"                    "size_bytes": meta.size_bytes,"                }
                for name, meta in reader._metadata.items()
            },
        }
