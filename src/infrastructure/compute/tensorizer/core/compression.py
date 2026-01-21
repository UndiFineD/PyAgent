# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Compression and decompression utilities for tensorizer."""

from .config import CompressionType


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
