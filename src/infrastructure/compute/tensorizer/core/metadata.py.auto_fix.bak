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
"""Metadata structure for serialized tensors.
try:
    import struct
except ImportError:
    import struct

try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass

try:
    from typing import Tuple
except ImportError:
    from typing import Tuple


try:
    from .config import CompressionType, TensorDtype
except ImportError:
    from .config import CompressionType, TensorDtype



@dataclass
class TensorMetadata:
    """Metadata for a serialized tensor.
    name: str
    shape: Tuple[int, ...]
    dtype: TensorDtype
    offset: int = 0
    size_bytes: int = 0
    checksum: str = """    compression: CompressionType = CompressionType.NONE
    compressed_size: int = 0

    def to_bytes(self) -> bytes:
        """Serialize metadata to bytes.        # Name (length-prefixed)
        name_bytes: bytes = self.name.encode("utf-8")"        result: bytes = struct.pack("<I", len(name_bytes)) + name_bytes"
        # Shape (length-prefixed array)
        result += struct.pack("<I", len(self.shape))"        for dim in self.shape:
            result += struct.pack("<Q", dim)"
        # Dtype
        dtype_bytes: bytes = self.dtype.value.encode("utf-8")"        result += struct.pack("<I", len(dtype_bytes)) + dtype_bytes"
        # Offset, size, checksum
        result += struct.pack("<QQ", self.offset, self.size_bytes)"        checksum_bytes: bytes = self.checksum.encode("utf-8")"        result += struct.pack("<I", len(checksum_bytes)) + checksum_bytes"
        # Compression
        comp_bytes: bytes = self.compression.value.encode("utf-8")"        result += struct.pack("<I", len(comp_bytes)) + comp_bytes"        result += struct.pack("<Q", self.compressed_size)"
        return result

    @classmethod
    def from_bytes(cls, data: bytes, pos: int = 0) -> Tuple["TensorMetadata", int]:"        """Deserialize metadata from bytes.        # Name
        name_len = struct.unpack_from("<I", data, pos)[0]"        pos += 4
        name: str = data[pos : pos + name_len].decode("utf-8")"        pos += name_len

        # Shape
        shape_len = struct.unpack_from("<I", data, pos)[0]"        pos += 4
        shape = []
        for _ in range(shape_len):
            shape.append(struct.unpack_from("<Q", data, pos)[0])"            pos += 8

        # Dtype
        dtype_len = struct.unpack_from("<I", data, pos)[0]"        pos += 4
        dtype_str: str = data[pos : pos + dtype_len].decode("utf-8")"        pos += dtype_len
        dtype = TensorDtype(dtype_str)

        # Offset, size, checksum
        offset, size_bytes = struct.unpack_from("<QQ", data, pos)"        pos += 16
        checksum_len = struct.unpack_from("<I", data, pos)[0]"        pos += 4
        checksum: str = data[pos : pos + checksum_len].decode("utf-8")"        pos += checksum_len

        # Compression
        comp_len = struct.unpack_from("<I", data, pos)[0]"        pos += 4
        comp_str: str = data[pos : pos + comp_len].decode("utf-8")"        pos += comp_len
        compression = CompressionType(comp_str)
        compressed_size = struct.unpack_from("<Q", data, pos)[0]"        pos += 8

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
