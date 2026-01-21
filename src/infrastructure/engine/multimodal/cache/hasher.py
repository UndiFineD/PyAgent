# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Content-aware hasher for multimodal data."""

import hashlib
import io
import struct
from typing import Any, Optional, Tuple, Union
import numpy as np
from .enums import MediaType, HashAlgorithm
from .data import MediaHash

# Optional imports
try:
    import blake3
    HAS_BLAKE3 = True
except ImportError:
    HAS_BLAKE3 = False

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class MultiModalHasher:
    """
    Content-aware hasher for multimodal data.

    Supports:
    - Blake3 for fast cryptographic hashing
    - SHA256 for compatibility
    - Perceptual hashing for similar image detection
    """

    def __init__(
        self,
        algorithm: HashAlgorithm = HashAlgorithm.BLAKE3,
        perceptual_size: Tuple[int, int] = (8, 8),
    ):
        self.algorithm = algorithm
        self.perceptual_size = perceptual_size

        # Use Blake3 if available, fallback to SHA256
        if algorithm == HashAlgorithm.BLAKE3 and not HAS_BLAKE3:
            self.algorithm = HashAlgorithm.SHA256

    def hash_bytes(self, data: bytes) -> str:
        """Hash raw bytes."""
        if self.algorithm == HashAlgorithm.BLAKE3 and HAS_BLAKE3:
            return blake3.blake3(data).hexdigest()
        elif self.algorithm == HashAlgorithm.SHA256:
            return hashlib.sha256(data).hexdigest()
        elif self.algorithm == HashAlgorithm.XXHASH:
            # Simple xxHash-like implementation
            h = 0
            for i, byte in enumerate(data):
                h = (h * 31 + byte) & 0xFFFFFFFFFFFFFFFF
            return format(h, '016x')
        else:
            return hashlib.sha256(data).hexdigest()

    def hash_image(self, image_data: Union[bytes, Any]) -> MediaHash:
        """Hash image content."""
        if isinstance(image_data, bytes):
            content_hash = self.hash_bytes(image_data)
            size = len(image_data)
        elif HAS_PIL and isinstance(image_data, Image.Image):
            # Convert PIL image to bytes
            buffer = io.BytesIO()
            image_data.save(buffer, format='PNG')
            img_bytes = buffer.getvalue()
            content_hash = self.hash_bytes(img_bytes)
            size = len(img_bytes)
        else:
            # Try to get bytes from object
            content_hash = self.hash_bytes(str(image_data).encode())
            size = 0

        return MediaHash(
            value=content_hash,
            algorithm=self.algorithm,
            media_type=MediaType.IMAGE,
            size_bytes=size
        )

    def hash_audio(self, audio_data: bytes, sample_rate: int = 16000) -> MediaHash:
        """Hash audio content."""
        combined = audio_data + struct.pack('I', sample_rate)
        content_hash = self.hash_bytes(combined)

        return MediaHash(
            value=content_hash,
            algorithm=self.algorithm,
            media_type=MediaType.AUDIO,
            size_bytes=len(audio_data)
        )

    def hash_video(self, video_data: bytes, frame_count: int = 0) -> MediaHash:
        """Hash video content."""
        combined = video_data + struct.pack('I', frame_count)
        content_hash = self.hash_bytes(combined)

        return MediaHash(
            value=content_hash,
            algorithm=self.algorithm,
            media_type=MediaType.VIDEO,
            size_bytes=len(video_data)
        )

    def hash_embedding(self, embedding: np.ndarray) -> MediaHash:
        """Hash embedding vector."""
        content_hash = self.hash_bytes(embedding.tobytes())

        return MediaHash(
            value=content_hash,
            algorithm=self.algorithm,
            media_type=MediaType.EMBEDDING,
            size_bytes=embedding.nbytes
        )

    def perceptual_hash(self, image_data: Union[bytes, Any]) -> str:
        """Compute perceptual hash for image similarity."""
        if not HAS_PIL:
            if isinstance(image_data, bytes):
                return self.hash_bytes(image_data)[:16]
            return self.hash_bytes(str(image_data).encode())[:16]

        # Load image
        if isinstance(image_data, bytes):
            img = Image.open(io.BytesIO(image_data))
        elif isinstance(image_data, Image.Image):
            img = image_data
        else:
            return self.hash_bytes(str(image_data).encode())[:16]

        img = img.convert('L').resize(self.perceptual_size, Image.Resampling.LANCZOS)
        pixels = np.array(img)
        avg = pixels.mean()
        bits = (pixels > avg).flatten()
        hash_value = ''.join('1' if b else '0' for b in bits)
        return format(int(hash_value, 2), f'0{len(bits)//4}x')
