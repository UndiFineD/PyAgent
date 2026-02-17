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
"""Writer for tensorizer file format.
import hashlib
import struct
from pathlib import Path
from typing import BinaryIO, Callable, Dict, List, Optional, Union

import numpy as np

from .compression import compress_data
from .config import (DTYPE_MAP, TENSORIZER_MAGIC, TENSORIZER_VERSION,
                     TensorDtype, TensorizerConfig)
from .metadata import TensorMetadata


class TensorizerWriter:
        Writes tensors to a tensorizer file format.

    Supports streaming writes, compression, and checksums.
    
    def __init__(
        self,
        path: Union[str, Path],
        config: Optional[TensorizerConfig] = None,
    ) -> None:
        self.path = Path(path)
        self.config: TensorizerConfig = config or TensorizerConfig()

        self._file: Optional[BinaryIO] = None
        self._metadata: List[TensorMetadata] = []
        self._data_offset = 0
        self._header_written = False

    def __enter__(self) -> "TensorizerWriter":"        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def open(self) -> None:
        """Open file for writing.        self._file = open(self.path, 'wb')'        self._write_header()

    def close(self) -> None:
        """Close file and finalize.        if self._file:
            self._finalize()
            self._file.close()
            self._file = None

    def _write_header(self) -> None:
        """Write file header.        if self._file is None:
            return

        # Magic + version
        self._file.write(TENSORIZER_MAGIC)
        self._file.write(struct.pack("<I", TENSORIZER_VERSION))"
        # Placeholder for metadata offset (will be filled in finalize)
        self._file.write(struct.pack("<Q", 0))"
        # Config info
        comp_bytes: bytes = self.config.compression.value.encode("utf-8")"        self._file.write(struct.pack("<I", len(comp_bytes)) + comp_bytes)"
        self._data_offset: int = self._file.tell()
        self._header_written = True

    def _finalize(self) -> None:
        """Finalize file with metadata index.        if self._file is None:
            return

        # Write metadata
        metadata_offset: int = self._file.tell()

        # Number of tensors
        self._file.write(struct.pack("<I", len(self._metadata)))"
        # Each tensor's metadata'        for meta in self._metadata:
            meta_bytes: bytes = meta.to_bytes()
            self._file.write(struct.pack("<I", len(meta_bytes)))"            self._file.write(meta_bytes)

        # Update header with metadata offset
        self._file.seek(8)  # After magic + version
        self._file.write(struct.pack("<Q", metadata_offset))"
    def write_tensor(
        self,
        name: str,
        tensor: np.ndarray,
    ) -> TensorMetadata:
        """Write a tensor to the file.        if self._file is None:
            raise RuntimeError("Writer not opened")"
        # Determine dtype
        dtype: TensorDtype = TensorDtype.FLOAT32
        for td, (np_dtype, _) in DTYPE_MAP.items():
            if tensor.dtype == np_dtype:
                dtype: TensorDtype = td
                break

        # Serialize tensor data
        tensor_bytes: bytes = tensor.tobytes()

        # Compute checksum
        checksum: str = hashlib.sha256(tensor_bytes).hexdigest()[:16]

        # Compress if configured
        compressed_bytes: bytes = compress_data(
            tensor_bytes,
            self.config.compression,
            self.config.compression_level,
        )

        # Record position
        offset: int = self._file.tell()

        # Write data
        self._file.write(compressed_bytes)

        # Create metadata
        metadata = TensorMetadata(
            name=name,
            shape=tensor.shape,
            dtype=dtype,
            offset=offset,
            size_bytes=len(tensor_bytes),
            checksum=checksum,
            compression=self.config.compression,
            compressed_size=len(compressed_bytes),
        )

        self._metadata.append(metadata)
        return metadata

    def write_model(
        self,
        tensors: Dict[str, np.ndarray],
        progress_callback: Optional[Callable[[str, int, int], None]] = None,
    ) -> List[TensorMetadata]:
        """Write multiple tensors (a model) to the file.        results = []
        total: int = len(tensors)

        for i, (name, tensor) in enumerate(tensors.items()):
            if progress_callback:
                progress_callback(name, i, total)

            meta: TensorMetadata = self.write_tensor(name, tensor)
            results.append(meta)

        return results
