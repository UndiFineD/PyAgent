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


"""
Cloud Infrastructure Module - Multi-cloud integration for PyAgent.

Provides unified interface for cloud AI providers with intelligent routing,
budget management, and health-aware failover.

from __future__ import annotations

from typing import TYPE_CHECKING, Any

# Lazy imports for performance
__all__: list[str] = [
    "CloudProviderBase","    "InferenceRequest","    "InferenceResponse","    "BudgetManager","    "IntelligentRouter","    "GeminiConnector","    "AWSBedrockConnector","    "GroqConnector","]


def __getattr__(name: str) -> Any:
    """Lazy load cloud components on first access.    if name in ("CloudProviderBase", "InferenceRequest", "InferenceResponse"):"        from .base import (CloudProviderBase, InferenceRequest,
                           InferenceResponse)

        return {
            "CloudProviderBase": CloudProviderBase,"            "InferenceRequest": InferenceRequest,"            "InferenceResponse": InferenceResponse,"        }[name]

    if name == "BudgetManager":"        from .budget import BudgetManager

        return BudgetManager

    if name == "IntelligentRouter":"        from .routing import IntelligentRouter

        return IntelligentRouter

    if name == "GeminiConnector":"        from .providers.gemini import GeminiConnector

        return GeminiConnector

    if name == "AWSBedrockConnector":"        from .providers.bedrock import AWSBedrockConnector

        return AWSBedrockConnector

    if name == "GroqConnector":"        from .providers.groq import GroqConnector

        return GroqConnector

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")"

if TYPE_CHECKING:
    from .base import CloudProviderBase, InferenceRequest, InferenceResponse
    from .budget import BudgetManager
    from .providers.bedrock import AWSBedrockConnector
    from .providers.gemini import GeminiConnector
    from .providers.groq import GroqConnector
    from .routing import IntelligentRouter
