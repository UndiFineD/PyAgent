from __future__ import annotations
from dataclasses import dataclass
from typing import Any


class CloudProviderError(Exception):
    pass


class AuthenticationError(CloudProviderError):
    pass


class RateLimitError(CloudProviderError):
    pass


class CloudProviderBase:
    """Minimal base class for cloud providers used by tests."""

    def __init__(self, *args: Any, **kwargs: Any):
        pass


@dataclass
class InferenceRequest:
    model: str
    prompt: str


@dataclass
class InferenceResponse:
    text: str
    usage: dict | None = None


__all__ = [
    "AuthenticationError",
    "CloudProviderBase",
    "CloudProviderError",
    "InferenceRequest",
    "InferenceResponse",
    "RateLimitError",
]
