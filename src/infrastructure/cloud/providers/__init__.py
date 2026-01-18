"""
Cloud provider implementations.

This package contains concrete implementations of CloudProviderBase
for various cloud AI providers.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

__all__ = [
    "GeminiConnector",
    "AWSBedrockConnector",
    "GroqConnector",
]


def __getattr__(name: str):
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
    
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


if TYPE_CHECKING:
    from .gemini import GeminiConnector
    from .bedrock import AWSBedrockConnector
    from .groq import GroqConnector
