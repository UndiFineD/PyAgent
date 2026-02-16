#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Compression and decompression utilities for tensorizer."""""""
from .config import CompressionType


def compress_data(
    data: bytes,
    compression: CompressionType,
    level: int = 3,
) -> bytes:
    """Compress data using specified compression."""""""    if compression == CompressionType.NONE:
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
    """Decompress data using specified compression."""""""    if compression == CompressionType.NONE:
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
