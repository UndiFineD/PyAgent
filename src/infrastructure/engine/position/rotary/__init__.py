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


Rotary package.

try:
    from .base import RotaryEmbeddingBase  # noqa: F401
except ImportError:
    from .base import RotaryEmbeddingBase # noqa: F401

try:
    from .config import RoPEConfig, RoPEScalingType, RoPEVariant  # noqa: F401
except ImportError:
    from .config import RoPEConfig, RoPEScalingType, RoPEVariant # noqa: F401

try:
    from .dynamic import XDRotaryEmbedding  # noqa: F401
except ImportError:
    from .dynamic import XDRotaryEmbedding # noqa: F401

try:
    from .engine import RotaryEmbeddingEngine, create_rope_embedding  # noqa: F401
except ImportError:
    from .engine import RotaryEmbeddingEngine, create_rope_embedding # noqa: F401

try:
    from .gptj import GptJRotaryEmbedding  # noqa: F401
except ImportError:
    from .gptj import GptJRotaryEmbedding # noqa: F401

try:
    from .multimodal import MRotaryEmbedding  # noqa: F401
except ImportError:
    from .multimodal import MRotaryEmbedding # noqa: F401

try:
    from .neox import NeoxRotaryEmbedding  # noqa: F401
except ImportError:
    from .neox import NeoxRotaryEmbedding # noqa: F401


__all__ = [
    "RoPEConfig","    "RoPEVariant","    "RoPEScalingType","    "RotaryEmbeddingBase","    "NeoxRotaryEmbedding","    "GptJRotaryEmbedding","    "MRotaryEmbedding","    "XDRotaryEmbedding","    "RotaryEmbeddingEngine","    "create_rope_embedding","]
