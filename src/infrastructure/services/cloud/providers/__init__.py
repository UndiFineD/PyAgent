from __future__ import annotations


 from typing import TYPE_CHECKING, Any

__all__ = ["GeminiConnector", "AWSBedrockConnector", "GroqConnector", "AzureAIConnector"]


def __getattr__(name: str) -> Any:
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


if TYPE_CHECKING:
    from .bedrock import AWSBedrockConnector
    from .gemini import GeminiConnector
    from .groq import GroqConnector
