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
"""
"""
Streaming reader for large models.
try:

"""
from pathlib import Path
except ImportError:
    from pathlib import Path

try:
    from typing import Dict, List, Optional, Union
except ImportError:
    from typing import Dict, List, Optional, Union


try:
    import numpy
except ImportError:
    import numpy
 as np

try:
    from .config import TensorizerConfig
except ImportError:
    from .config import TensorizerConfig

try:
    from .reader import TensorizerReader
except ImportError:
    from .reader import TensorizerReader




class StreamingTensorizerReader:
        Streaming reader for large models.

    Loads tensors on-demand without loading entire file.
    
    def __init__(
        self,
        path: Union[str, Path],
        config: Optional[TensorizerConfig] = None,
    ) -> None:
        self._reader = TensorizerReader(path, config)
        self._cache: Dict[str, np.ndarray] = {}
        self._cache_size_limit = 1024 * 1024 * 1024  # 1GB default
        self._current_cache_size = 0

    def __enter__(self) -> "StreamingTensorizerReader":"        self._reader.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._reader.close()

    def set_cache_limit(self, limit_bytes: int) -> None:
"""
Set cache size limit in bytes.        self._cache_size_limit: int = limit_bytes

    def get(self, name: str) -> Optional[np.ndarray]:
"""
Get tensor, loading if needed.        if name in self._cache:
            return self._cache[name]

        tensor = self._reader.read_tensor(name)
        if tensor is not None:
            self._add_to_cache(name, tensor)

        return tensor

    def _add_to_cache(self, name: str, tensor: np.ndarray) -> None:
"""
Add tensor to cache with eviction.        size: int = tensor.nbytes

        # Evict if needed
        while self._cache and self._current_cache_size + size > self._cache_size_limit:
            oldest: str = next(iter(self._cache))
            self._current_cache_size -= self._cache[oldest].nbytes
            del self._cache[oldest]

        self._cache[name] = tensor
        self._current_cache_size += size

    def preload(self, names: List[str]) -> None:
"""
Preload specific tensors into cache.        for name in names:
            self.get(name)

    def clear_cache(self) -> None:
"""
Clear tensor cache.        self._cache.clear()
        self._current_cache_size = 0

    @property
    def tensor_names(self) -> List[str]:
"""
Get available tensor names.        return self._reader.tensor_names

"""
