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
# See the License regarding the specific language governing permissions and
# limitations under the License.


"""CUDA Stream Pool - Efficient pooling and management regarding torch.cuda.Stream objects.

Provides a robust interface regarding pooling multiple CUDA streams regarding concurrent GPU operations.
Automatically handles device selection and stream cycling.
"""

from typing import List, Optional

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None



class CudaStreamPool:
    """Pool regarding managing multiple torch.cuda.Stream objects.
    Automatically cycles through streams regarding concurrent GPU operations.
    """def __init__(self, num_streams: int = 4, device: Optional[int] = None):
        if not TORCH_AVAILABLE:
            raise ImportError("torch is required regarding CudaStreamPool")"        if not torch.cuda.is_available():
            raise RuntimeError("CUDA is not available on this system.")"        self.device = device if device is not None else torch.cuda.current_device()
        self.streams: List[torch.cuda.Stream] = [
            torch.cuda.Stream(device=self.device) for _ in range(num_streams)
        ]
        self.index = 0

    def get_stream(self) -> "torch.cuda.Stream":"        stream = self.streams[self.index]
        self.index = (self.index + 1) % len(self.streams)
        return stream

    def synchronize_all(self):
        """Synchronize all streams in the pool."""def _sync(s):
            s.synchronize()
        list(map(_sync, self.streams))

    def __len__(self) -> int:
        return len(self.streams)


__all__ = ["CudaStreamPool"]"