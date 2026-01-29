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
Cloud provider implementations.

This package contains concrete implementations of CloudProviderBase
for various cloud AI providers.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.infrastructure.services.cloud.providers.azure import AzureAIConnector
from src.infrastructure.services.cloud.providers.bedrock import AWSBedrockConnector
from src.infrastructure.services.cloud.providers.gemini import GeminiConnector
from src.infrastructure.services.cloud.providers.groq import GroqConnector

__all__: list[str] = [
    "GeminiConnector",
    "AWSBedrockConnector",
    "GroqConnector",
    "AzureAIConnector",
]


def __getattr__(name: str) -> type[GeminiConnector] | type[AWSBedrockConnector] | type[GroqConnector] | type[AzureAIConnector]:
    """Lazy load provider implementations."""
    if name == "GeminiConnector":
        from .gemini import GeminiConnector

        return GeminiConnector
    if name == "AWSBedrockConnector":
        from .bedrock import AWSBedrockConnector

        return AWSBedrockConnector
    if name == "GroqConnector":
        from .groq import GroqConnector

        return GroqConnector
    if name == "AzureAIConnector":
        from .azure import AzureAIConnector

        return AzureAIConnector
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    if name == "GeminiConnector":
        from .gemini import GeminiConnector

        return GeminiConnector

    if name == "AWSBedrockConnector":
        from .bedrock import AWSBedrockConnector

        return AWSBedrockConnector

    if name == "GroqConnector":
        from .groq import GroqConnector

        return GroqConnector

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


if TYPE_CHECKING:
    from .bedrock import AWSBedrockConnector
    from .gemini import GeminiConnector
    from .groq import GroqConnector
