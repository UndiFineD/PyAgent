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

# Guarded imports to prevent package-level failures when optional dependencies (like vllm)
# are not installed. Each submodule is imported individually with try/except, allowing the
# package to be imported successfully even if some features are unavailable.
try:
    from .AsyncVllmEngine import (
        AsyncVllmEngine,
        AsyncEngineConfig,
        AsyncRequestHandle,
    )
except ImportError:  # pragma: no cover - optional dependency
    AsyncVllmEngine = None
    AsyncEngineConfig = None
    AsyncRequestHandle = None

try:
    from .StreamingEngine import (
        StreamingVllmEngine,
        StreamingConfig,
        StreamCallback,
        TokenStreamIterator,
    )
except ImportError:  # pragma: no cover - optional dependency
    StreamingVllmEngine = None
    StreamingConfig = None
    StreamCallback = None
    TokenStreamIterator = None

try:
    from .LoraManager import (
        LoraManager,
        LoraAdapter,
        LoraConfig,
        LoraRegistry,
    )
except ImportError:  # pragma: no cover
    LoraManager = None
    LoraAdapter = None
    LoraConfig = None
    LoraRegistry = None

try:
    from .GuidedDecoder import (
        GuidedDecoder,
        GuidedConfig,
        JsonSchema,
        RegexPattern,
        ChoiceConstraint,
    )
except ImportError:  # pragma: no cover
    GuidedDecoder = None
    GuidedConfig = None
    JsonSchema = None
    RegexPattern = None
    ChoiceConstraint = None

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
