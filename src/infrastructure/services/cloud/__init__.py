"""
Cloud Infrastructure Module - Multi-cloud integration for PyAgent.

Provides unified interface for cloud AI providers with intelligent routing,
budget management, and health-aware failover.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

# Lazy imports for performance
__all__ = [
    "CloudProviderBase",
    "InferenceRequest",
    "InferenceResponse",
    "BudgetManager",
    "IntelligentRouter",
    "GeminiConnector",
    "AWSBedrockConnector",
    "GroqConnector",
]


def __getattr__(name: str):
    """Lazy load cloud components on first access."""
    if name in ("CloudProviderBase", "InferenceRequest", "InferenceResponse"):
        from .base import CloudProviderBase, InferenceRequest, InferenceResponse
        return {"CloudProviderBase": CloudProviderBase, 
                "InferenceRequest": InferenceRequest, 
                "InferenceResponse": InferenceResponse}[name]
    
    if name == "BudgetManager":
        from .budget import BudgetManager
        return BudgetManager
    
    if name == "IntelligentRouter":
        from .routing import IntelligentRouter
        return IntelligentRouter
    
    if name == "GeminiConnector":
        from .providers.gemini import GeminiConnector
        return GeminiConnector
    
    if name == "AWSBedrockConnector":
        from .providers.bedrock import AWSBedrockConnector
        return AWSBedrockConnector
    
    if name == "GroqConnector":
        from .providers.groq import GroqConnector
        return GroqConnector
    
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


if TYPE_CHECKING:
    from .base import CloudProviderBase, InferenceRequest, InferenceResponse
    from .budget import BudgetManager
    from .routing import IntelligentRouter
    from .providers.gemini import GeminiConnector
    from .providers.bedrock import AWSBedrockConnector
    from .providers.groq import GroqConnector
