# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Streaming reader for large models."""

from pathlib import Path
from typing import Dict, List, Optional, Union
import numpy as np
from .config import TensorizerConfig
from .reader import TensorizerReader


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
