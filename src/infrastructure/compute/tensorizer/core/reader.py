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

from __future__ import annotations

from _thread import LockType
from concurrent.futures import ThreadPoolExecutor  # noqa: F401
import hashlib
import mmap
import struct
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import (BinaryIO, Callable, Dict, Iterator, List, Optional, Tuple, Union)

import numpy as np

from .compression import decompress_data
from .config import (DTYPE_MAP, TENSORIZER_MAGIC, TENSORIZER_VERSION, CompressionType, TensorizerConfig)
from .metadata import TensorMetadata


@dataclass
class LoadProgress:
    """Progress information for loading."""
    total_tensors: int = 0
    loaded_tensors: int = 0
    total_bytes: int = 0
    loaded_bytes: int = 0
    current_tensor: str = ""

    @property
    def tensor_progress(self) -> float:
        """Returns the fraction of total tensors loaded (0.0 to 1.0)."""
        if self.total_tensors == 0:
            return 0.0
        return self.loaded_tensors / self.total_tensors

    @property
    def byte_progress(self) -> float:
        """Returns the fraction of total bytes loaded (0.0 to 1.0)."""
        if self.total_bytes == 0:
            return 0.0
        return self.loaded_bytes / self.total_bytes


class TensorizerReader:
    """
    Reads tensors from a tensorizer file format.

    Supports memory-mapped access and parallel loading.
    """

    def __init__(
        self,
        path: Union[str, Path],
        config: Optional[TensorizerConfig] = None,
    ) -> None:
        self.path = Path(path)
        self.config: TensorizerConfig = config or TensorizerConfig()

        self._file: Optional[BinaryIO] = None
        self._mmap: Optional[mmap.mmap] = None
        self._metadata: Dict[str, TensorMetadata] = {}
        self._compression: CompressionType = CompressionType.NONE
        self._lock: LockType = threading.Lock()
        self._metadata_offset = 0

    def __enter__(self) -> "TensorizerReader":
        """Context manager entry: open the file."""
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit: close the file."""
        self.close()

    def open(self) -> None:
        """Open file for reading."""
        self._file = open(self.path, 'rb')

        if self.config.use_mmap:
            self._mmap = mmap.mmap(
                self._file.fileno(),
                0,
                access=mmap.ACCESS_READ,
            )

        self._read_header()
        self._read_metadata()

    def close(self) -> None:
        """Close file."""
        if self._mmap:
            self._mmap.close()
            self._mmap = None

        if self._file:
            self._file.close()
            self._file = None

    def _read_header(self) -> None:
        """Read and validate file header."""
        if self._file is None:
            return

        # Magic
        magic: bytes = self._file.read(4)
        if magic != TENSORIZER_MAGIC:
            raise ValueError(f"Invalid tensorizer file: bad magic {magic}")

        # Version
        version = struct.unpack("<I", self._file.read(4))[0]
        if version > TENSORIZER_VERSION:
            raise ValueError(f"Unsupported tensorizer version: {version}")

        # Metadata offset
        self._metadata_offset = struct.unpack("<Q", self._file.read(8))[0]

        # Compression
        comp_len = struct.unpack("<I", self._file.read(4))[0]
        comp_str: str = self._file.read(comp_len).decode("utf-8")
        self._compression = CompressionType(comp_str)

    def _read_metadata(self) -> None:
        """Read tensor metadata index."""
        if self._file is None:
            return

        self._file.seek(self._metadata_offset)

        # Number of tensors
        num_tensors = struct.unpack("<I", self._file.read(4))[0]

        # Read each metadata
        for _ in range(num_tensors):
            meta_len = struct.unpack("<I", self._file.read(4))[0]
            meta_bytes: bytes = self._file.read(meta_len)
            meta, _ = TensorMetadata.from_bytes(meta_bytes)
            self._metadata[meta.name] = meta

    @property
    def tensor_names(self) -> List[str]:
        """Get list of tensor names."""
        return list(self._metadata.keys())

    @property
    def num_tensors(self) -> int:
        """Get number of tensors."""
        return len(self._metadata)

    def get_metadata(self, name: str) -> Optional[TensorMetadata]:
        """Get metadata for a tensor."""
        return self._metadata.get(name)

    def read_tensor(self, name: str) -> Optional[np.ndarray]:
        """Read a single tensor by name."""
        meta: TensorMetadata | None = self._metadata.get(name)
        if meta is None:
            return None

        return self._load_tensor(meta)

    def _load_tensor(self, meta: TensorMetadata) -> np.ndarray:
        """Load tensor data."""
        with self._lock:
            if self._mmap:
                data: bytes = self._mmap[meta.offset : meta.offset + meta.compressed_size]
            else:
                if self._file is None:
                    raise RuntimeError("Reader not opened")
                self._file.seek(meta.offset)
                data: bytes = self._file.read(meta.compressed_size)

        # Decompress if needed
        if meta.compression != CompressionType.NONE:
            data: bytes = decompress_data(data, meta.compression)

        # Verify checksum
        if self.config.verify_checksums:
            actual_checksum: str = hashlib.sha256(data).hexdigest()[:16]
            if actual_checksum != meta.checksum:
                raise ValueError(f"Checksum mismatch for {meta.name}: expected {meta.checksum}, got {actual_checksum}")

        # Convert to numpy
        np_dtype, _ = DTYPE_MAP.get(meta.dtype, (np.float32, 4))
        tensor: np.ndarray[Tuple[int], np.dtype[np.float64]] = np.frombuffer(data, dtype=np_dtype).reshape(meta.shape)

        return tensor

    def read_all(
        self,
        progress_callback: Optional[Callable[[LoadProgress], None]] = None,
    ) -> Dict[str, np.ndarray]:
        """Read all tensors."""
        progress = LoadProgress(
            total_tensors=len(self._metadata),
            total_bytes=sum(m.size_bytes for m in self._metadata.values()),
        )

        result = {}

        for name, meta in self._metadata.items():
            progress.current_tensor = name

            if progress_callback:
                progress_callback(progress)

            result[name] = self._load_tensor(meta)

            progress.loaded_tensors += 1
            progress.loaded_bytes += meta.size_bytes

        return result

    def read_parallel(
        self,
        tensor_names: Optional[List[str]] = None,
        progress_callback: Optional[Callable[[LoadProgress], None]] = None,
    ) -> Dict[str, np.ndarray]:
        """Read tensors in parallel."""
        names: List[str] = tensor_names or list(self._metadata.keys())

        progress = LoadProgress(
            total_tensors=len(names),
            total_bytes=sum(self._metadata[n].size_bytes for n in names if n in self._metadata),
        )

        result: Dict[str, np.ndarray] = {}
        result_lock: LockType = threading.Lock()

        def load_one(name: str) -> None:
            meta: TensorMetadata | None = self._metadata.get(name)
            if meta is None:
                return

            tensor = self._load_tensor(meta)

            with result_lock:
                result[name] = tensor
                progress.loaded_tensors += 1
                progress.loaded_bytes += meta.size_bytes
                progress.current_tensor = name

                if progress_callback:
                    progress_callback(progress)

        with ThreadPoolExecutor(max_workers=self.config.parallel_threads) as executor:
            executor.map(load_one, names)

        return result

    def iter_tensors(self) -> Iterator[Tuple[str, np.ndarray]]:
        """Iterate over tensors one at a time."""
        for name in self._metadata:
            tensor = self.read_tensor(name)
            if tensor is not None:
                yield name, tensor
