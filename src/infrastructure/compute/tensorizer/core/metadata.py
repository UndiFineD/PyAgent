# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Metadata structure for serialized tensors."""

import struct
from dataclasses import dataclass
from typing import Tuple
from .config import TensorDtype, CompressionType


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
