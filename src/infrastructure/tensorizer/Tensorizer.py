# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 39: Tensorizer - Fast Model Serialization
# Inspired by vLLM's tensorizer_loader.py

"""
Tensorizer: High-performance model serialization and loading.

Provides:
- Streaming tensor serialization/deserialization
- Parallel tensor loading
- Memory-mapped file support
- Compression support
- Checksum verification
"""

from __future__ import annotations

import hashlib
import mmap
import os
import struct
import threading
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, BinaryIO, Callable, Dict, Iterator, List, Optional, Tuple, Union
import numpy as np


# =============================================================================
# Enums and Constants
# =============================================================================

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


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class TensorMetadata:
    """Metadata for a serialized tensor."""
    name: str
    shape: Tuple[int, ...]
    dtype: TensorDtype
    offset: int = 0
    size_bytes: int = 0
    checksum: str = ""
    compression: CompressionType = CompressionType.NONE
    compressed_size: int = 0
    
    def to_bytes(self) -> bytes:
        """Serialize metadata to bytes."""
        # Name (length-prefixed)
        name_bytes = self.name.encode("utf-8")
        result = struct.pack("<I", len(name_bytes)) + name_bytes
        
        # Shape (length-prefixed array)
        result += struct.pack("<I", len(self.shape))
        for dim in self.shape:
            result += struct.pack("<Q", dim)
        
        # Dtype
        dtype_bytes = self.dtype.value.encode("utf-8")
        result += struct.pack("<I", len(dtype_bytes)) + dtype_bytes
        
        # Offset, size, checksum
        result += struct.pack("<QQ", self.offset, self.size_bytes)
        checksum_bytes = self.checksum.encode("utf-8")
        result += struct.pack("<I", len(checksum_bytes)) + checksum_bytes
        
        # Compression
        comp_bytes = self.compression.value.encode("utf-8")
        result += struct.pack("<I", len(comp_bytes)) + comp_bytes
        result += struct.pack("<Q", self.compressed_size)
        
        return result
    
    @classmethod
    def from_bytes(cls, data: bytes, pos: int = 0) -> Tuple["TensorMetadata", int]:
        """Deserialize metadata from bytes."""
        # Name
        name_len = struct.unpack_from("<I", data, pos)[0]
        pos += 4
        name = data[pos:pos + name_len].decode("utf-8")
        pos += name_len
        
        # Shape
        shape_len = struct.unpack_from("<I", data, pos)[0]
        pos += 4
        shape = []
        for _ in range(shape_len):
            shape.append(struct.unpack_from("<Q", data, pos)[0])
            pos += 8
        
        # Dtype
        dtype_len = struct.unpack_from("<I", data, pos)[0]
        pos += 4
        dtype_str = data[pos:pos + dtype_len].decode("utf-8")
        pos += dtype_len
        dtype = TensorDtype(dtype_str)
        
        # Offset, size, checksum
        offset, size_bytes = struct.unpack_from("<QQ", data, pos)
        pos += 16
        checksum_len = struct.unpack_from("<I", data, pos)[0]
        pos += 4
        checksum = data[pos:pos + checksum_len].decode("utf-8")
        pos += checksum_len
        
        # Compression
        comp_len = struct.unpack_from("<I", data, pos)[0]
        pos += 4
        comp_str = data[pos:pos + comp_len].decode("utf-8")
        pos += comp_len
        compression = CompressionType(comp_str)
        compressed_size = struct.unpack_from("<Q", data, pos)[0]
        pos += 8
        
        return cls(
            name=name,
            shape=tuple(shape),
            dtype=dtype,
            offset=offset,
            size_bytes=size_bytes,
            checksum=checksum,
            compression=compression,
            compressed_size=compressed_size,
        ), pos


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
        if self.total_tensors == 0:
            return 0.0
        return self.loaded_tensors / self.total_tensors
    
    @property
    def byte_progress(self) -> float:
        if self.total_bytes == 0:
            return 0.0
        return self.loaded_bytes / self.total_bytes


# =============================================================================
# Compression Utilities
# =============================================================================

def compress_data(
    data: bytes,
    compression: CompressionType,
    level: int = 3,
) -> bytes:
    """Compress data using specified compression."""
    if compression == CompressionType.NONE:
        return data
    
    if compression == CompressionType.ZSTD:
        try:
            import zstandard as zstd
            cctx = zstd.ZstdCompressor(level=level)
            return cctx.compress(data)
        except ImportError:
            return data
    
    if compression == CompressionType.LZ4:
        try:
            import lz4.frame
            return lz4.frame.compress(data, compression_level=level)
        except ImportError:
            return data
    
    if compression == CompressionType.GZIP:
        import gzip
        return gzip.compress(data, compresslevel=level)
    
    return data


def decompress_data(
    data: bytes,
    compression: CompressionType,
) -> bytes:
    """Decompress data using specified compression."""
    if compression == CompressionType.NONE:
        return data
    
    if compression == CompressionType.ZSTD:
        try:
            import zstandard as zstd
            dctx = zstd.ZstdDecompressor()
            return dctx.decompress(data)
        except ImportError:
            return data
    
    if compression == CompressionType.LZ4:
        try:
            import lz4.frame
            return lz4.frame.decompress(data)
        except ImportError:
            return data
    
    if compression == CompressionType.GZIP:
        import gzip
        return gzip.decompress(data)
    
    return data


# =============================================================================
# Tensorizer Writer
# =============================================================================

class TensorizerWriter:
    """
    Writes tensors to a tensorizer file format.
    
    Supports streaming writes, compression, and checksums.
    """
    
    def __init__(
        self,
        path: Union[str, Path],
        config: Optional[TensorizerConfig] = None,
    ):
        self.path = Path(path)
        self.config = config or TensorizerConfig()
        
        self._file: Optional[BinaryIO] = None
        self._metadata: List[TensorMetadata] = []
        self._data_offset = 0
        self._header_written = False
    
    def __enter__(self) -> "TensorizerWriter":
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
    
    def open(self) -> None:
        """Open file for writing."""
        self._file = open(self.path, "wb")
        self._write_header()
    
    def close(self) -> None:
        """Close file and finalize."""
        if self._file:
            self._finalize()
            self._file.close()
            self._file = None
    
    def _write_header(self) -> None:
        """Write file header."""
        if self._file is None:
            return
        
        # Magic + version
        self._file.write(TENSORIZER_MAGIC)
        self._file.write(struct.pack("<I", TENSORIZER_VERSION))
        
        # Placeholder for metadata offset (will be filled in finalize)
        self._file.write(struct.pack("<Q", 0))
        
        # Config info
        comp_bytes = self.config.compression.value.encode("utf-8")
        self._file.write(struct.pack("<I", len(comp_bytes)) + comp_bytes)
        
        self._data_offset = self._file.tell()
        self._header_written = True
    
    def _finalize(self) -> None:
        """Finalize file with metadata index."""
        if self._file is None:
            return
        
        # Write metadata
        metadata_offset = self._file.tell()
        
        # Number of tensors
        self._file.write(struct.pack("<I", len(self._metadata)))
        
        # Each tensor's metadata
        for meta in self._metadata:
            meta_bytes = meta.to_bytes()
            self._file.write(struct.pack("<I", len(meta_bytes)))
            self._file.write(meta_bytes)
        
        # Update header with metadata offset
        self._file.seek(8)  # After magic + version
        self._file.write(struct.pack("<Q", metadata_offset))
    
    def write_tensor(
        self,
        name: str,
        tensor: np.ndarray,
    ) -> TensorMetadata:
        """Write a tensor to the file."""
        if self._file is None:
            raise RuntimeError("Writer not opened")
        
        # Determine dtype
        dtype = TensorDtype.FLOAT32
        for td, (np_dtype, _) in DTYPE_MAP.items():
            if tensor.dtype == np_dtype:
                dtype = td
                break
        
        # Serialize tensor data
        tensor_bytes = tensor.tobytes()
        
        # Compute checksum
        checksum = hashlib.sha256(tensor_bytes).hexdigest()[:16]
        
        # Compress if configured
        compressed_bytes = compress_data(
            tensor_bytes,
            self.config.compression,
            self.config.compression_level,
        )
        
        # Record position
        offset = self._file.tell()
        
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
        """Write multiple tensors (a model) to the file."""
        results = []
        total = len(tensors)
        
        for i, (name, tensor) in enumerate(tensors.items()):
            if progress_callback:
                progress_callback(name, i, total)
            
            meta = self.write_tensor(name, tensor)
            results.append(meta)
        
        return results


# =============================================================================
# Tensorizer Reader
# =============================================================================

class TensorizerReader:
    """
    Reads tensors from a tensorizer file format.
    
    Supports memory-mapped access and parallel loading.
    """
    
    def __init__(
        self,
        path: Union[str, Path],
        config: Optional[TensorizerConfig] = None,
    ):
        self.path = Path(path)
        self.config = config or TensorizerConfig()
        
        self._file: Optional[BinaryIO] = None
        self._mmap: Optional[mmap.mmap] = None
        self._metadata: Dict[str, TensorMetadata] = {}
        self._compression: CompressionType = CompressionType.NONE
        self._lock = threading.Lock()
    
    def __enter__(self) -> "TensorizerReader":
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
    
    def open(self) -> None:
        """Open file for reading."""
        self._file = open(self.path, "rb")
        
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
        magic = self._file.read(4)
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
        comp_str = self._file.read(comp_len).decode("utf-8")
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
            meta_bytes = self._file.read(meta_len)
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
        meta = self._metadata.get(name)
        if meta is None:
            return None
        
        return self._load_tensor(meta)
    
    def _load_tensor(self, meta: TensorMetadata) -> np.ndarray:
        """Load tensor data."""
        with self._lock:
            if self._mmap:
                data = self._mmap[meta.offset:meta.offset + meta.compressed_size]
            else:
                if self._file is None:
                    raise RuntimeError("Reader not opened")
                self._file.seek(meta.offset)
                data = self._file.read(meta.compressed_size)
        
        # Decompress if needed
        if meta.compression != CompressionType.NONE:
            data = decompress_data(data, meta.compression)
        
        # Verify checksum
        if self.config.verify_checksums:
            actual_checksum = hashlib.sha256(data).hexdigest()[:16]
            if actual_checksum != meta.checksum:
                raise ValueError(
                    f"Checksum mismatch for {meta.name}: "
                    f"expected {meta.checksum}, got {actual_checksum}"
                )
        
        # Convert to numpy
        np_dtype, _ = DTYPE_MAP.get(meta.dtype, (np.float32, 4))
        tensor = np.frombuffer(data, dtype=np_dtype).reshape(meta.shape)
        
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
        names = tensor_names or list(self._metadata.keys())
        
        progress = LoadProgress(
            total_tensors=len(names),
            total_bytes=sum(
                self._metadata[n].size_bytes
                for n in names
                if n in self._metadata
            ),
        )
        
        result: Dict[str, np.ndarray] = {}
        result_lock = threading.Lock()
        
        def load_one(name: str) -> None:
            meta = self._metadata.get(name)
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
            yield name, self.read_tensor(name)


# =============================================================================
# Streaming Support
# =============================================================================

class StreamingTensorizerReader:
    """
    Streaming reader for large models.
    
    Loads tensors on-demand without loading entire file.
    """
    
    def __init__(
        self,
        path: Union[str, Path],
        config: Optional[TensorizerConfig] = None,
    ):
        self._reader = TensorizerReader(path, config)
        self._cache: Dict[str, np.ndarray] = {}
        self._cache_size_limit = 1024 * 1024 * 1024  # 1GB default
        self._current_cache_size = 0
    
    def __enter__(self) -> "StreamingTensorizerReader":
        self._reader.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._reader.close()
    
    def set_cache_limit(self, limit_bytes: int) -> None:
        """Set cache size limit in bytes."""
        self._cache_size_limit = limit_bytes
    
    def get(self, name: str) -> Optional[np.ndarray]:
        """Get tensor, loading if needed."""
        if name in self._cache:
            return self._cache[name]
        
        tensor = self._reader.read_tensor(name)
        if tensor is not None:
            self._add_to_cache(name, tensor)
        
        return tensor
    
    def _add_to_cache(self, name: str, tensor: np.ndarray) -> None:
        """Add tensor to cache with eviction."""
        size = tensor.nbytes
        
        # Evict if needed
        while (
            self._cache and
            self._current_cache_size + size > self._cache_size_limit
        ):
            oldest = next(iter(self._cache))
            self._current_cache_size -= self._cache[oldest].nbytes
            del self._cache[oldest]
        
        self._cache[name] = tensor
        self._current_cache_size += size
    
    def preload(self, names: List[str]) -> None:
        """Preload specific tensors into cache."""
        for name in names:
            self.get(name)
    
    def clear_cache(self) -> None:
        """Clear tensor cache."""
        self._cache.clear()
        self._current_cache_size = 0
    
    @property
    def tensor_names(self) -> List[str]:
        """Get available tensor names."""
        return self._reader.tensor_names


# =============================================================================
# Utility Functions
# =============================================================================

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
