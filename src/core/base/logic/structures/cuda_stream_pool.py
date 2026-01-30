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

"""
Mock implementation of a CUDA stream pool for testing and development.
Provides a simple interface for pooling multiple CUDA streams.
"""

from typing import List, Optional

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None

class MockCudaStream:
    def __init__(self, device: Optional[int] = None):
        self.device = device
        self.active = False
    def __enter__(self):
        self.active = True
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.active = False

class CudaStreamPool:
    """A mock pool for managing multiple CUDA streams."""
    def __init__(self, num_streams: int = 4, device: Optional[int] = None):
        self.device = device
        self.streams: List[MockCudaStream] = [MockCudaStream(device) for _ in range(num_streams)]
        self.index = 0
    def get_stream(self) -> MockCudaStream:
        stream = self.streams[self.index]
        self.index = (self.index + 1) % len(self.streams)
        return stream
    def __len__(self) -> int:
        return len(self.streams)

__all__ = ["CudaStreamPool", "MockCudaStream"]
