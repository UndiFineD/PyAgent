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
Advanced vLLM Integration Module.

Phase 31: Extends PyAgent's vLLM integration with:
- AsyncLLMEngine for high-throughput async inference
- Streaming responses for real-time token output
- LoRA adapter management for efficient fine-tuned models
- Guided decoding for structured output (JSON, regex)
"""

from .AsyncVllmEngine import (
    AsyncVllmEngine,
    AsyncEngineConfig,
    AsyncRequestHandle,
)
from .StreamingEngine import (
    StreamingVllmEngine,
    StreamingConfig,
    StreamCallback,
    TokenStreamIterator,
)
from .LoraManager import (
    LoraManager,
    LoraAdapter,
    LoraConfig,
    LoraRegistry,
)
from .GuidedDecoder import (
    GuidedDecoder,
    GuidedConfig,
    JsonSchema,
    RegexPattern,
    ChoiceConstraint,
)

__all__ = [
    # Async Engine
    "AsyncVllmEngine",
    "AsyncEngineConfig",
    "AsyncRequestHandle",
    # Streaming
    "StreamingVllmEngine",
    "StreamingConfig",
    "StreamCallback",
    "TokenStreamIterator",
    # LoRA
    "LoraManager",
    "LoraAdapter",
    "LoraConfig",
    "LoraRegistry",
    # Guided Decoding
    "GuidedDecoder",
    "GuidedConfig",
    "JsonSchema",
    "RegexPattern",
    "ChoiceConstraint",
]
