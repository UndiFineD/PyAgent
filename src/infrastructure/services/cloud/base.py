"""
Base classes for cloud provider integration.

Defines the abstract interface that all cloud providers must implement,
along with standardized request/response dataclasses.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import AsyncIterator, List, Optional, Dict, Any


@dataclass
class InferenceRequest:
    """Standardized inference request across all cloud providers."""
    
    messages: List[Dict[str, str]]
    """List of message dicts with 'role' and 'content' keys."""
    
    model: str
    """Model identifier (provider-specific or canonical name)."""
    
    max_tokens: int = 4096
    """Maximum tokens to generate in the response."""
    
    temperature: float = 0.7
    """Sampling temperature (0.0 = deterministic, 1.0 = creative)."""
    
    stream: bool = False
    """Whether to stream the response token by token."""
    
    # Optional parameters
    top_p: Optional[float] = None
    """Nucleus sampling parameter."""
    
    stop_sequences: Optional[List[str]] = None
    """Sequences that will stop generation."""
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    """Additional provider-specific parameters."""


@dataclass
class InferenceResponse:
    """Standardized inference response from cloud providers."""
    
    content: str
    """The generated text content."""
    
    tokens_used: int
    """Total tokens consumed (prompt + completion)."""
    
    cost_estimate: float
    """Estimated cost in USD for this request."""
    
    latency_ms: float
    """End-to-end latency in milliseconds."""
    
    provider: str
    """Name of the provider that handled the request."""
    
    # Optional metadata
    model: Optional[str] = None
    """Actual model used (may differ from requested)."""
    
    prompt_tokens: Optional[int] = None
    """Number of tokens in the prompt."""
    
    completion_tokens: Optional[int] = None
    """Number of tokens in the completion."""
    
    finish_reason: Optional[str] = None
    """Reason generation stopped (e.g., 'stop', 'length', 'content_filter')."""
    
    raw_response: Optional[Dict[str, Any]] = None
    """Raw response from the provider for debugging."""


class CloudProviderBase(ABC):
    """
    Abstract base class for cloud AI provider integrations.
    
    All cloud connectors (Gemini, Bedrock, Groq, etc.) must inherit from this
    class and implement the required abstract methods.
    
    Example:
        class MyProvider(CloudProviderBase):
            async def complete(self, request: InferenceRequest) -> InferenceResponse:
                # Implementation here
                ...
    """
    
    def __init__(self, api_key: Optional[str] = None, **config):
        """
        Initialize the cloud provider.
        
        Args:
            api_key: API key for authentication (can also use env vars).
            **config: Additional provider-specific configuration.
        """
        self._api_key = api_key
        self._config = config
        self._is_healthy = True
        self._last_error: Optional[str] = None
    
    @property
    def name(self) -> str:
        """Return the provider name (defaults to class name)."""
        return self.__class__.__name__
    
    @property
    def is_healthy(self) -> bool:
        """Return current health status."""
        return self._is_healthy
    
    @property
    @abstractmethod
    def available_models(self) -> List[str]:
        """
        Return list of available model identifiers for this provider.
        
        Returns:
            List of model names/IDs that can be used with this provider.
        """
        ...
    
    @abstractmethod
    async def complete(self, request: InferenceRequest) -> InferenceResponse:
        """
        Perform a completion request (non-streaming).
        
        Args:
            request: The inference request with messages, model, etc.
            
        Returns:
            InferenceResponse with generated content and metadata.
            
        Raises:
            CloudProviderError: If the request fails.
        """
        ...
    
    @abstractmethod
    async def stream(self, request: InferenceRequest) -> AsyncIterator[str]:
        """
        Perform a streaming completion request.
        
        Args:
            request: The inference request (stream flag will be set to True).
            
        Yields:
            String chunks of the generated response.
            
        Raises:
            CloudProviderError: If the request fails.
        """
        ...
    
    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check if the provider is healthy and accessible.
        
        Returns:
            True if the provider is operational, False otherwise.
        """
        ...
    
    @abstractmethod
    def estimate_cost(self, request: InferenceRequest) -> float:
        """
        Estimate the cost in USD for a given request.
        
        Args:
            request: The inference request to estimate.
            
        Returns:
            Estimated cost in USD.
        """
        ...
    
    def supports_model(self, model: str) -> bool:
        """Check if this provider supports the given model."""
        return model in self.available_models
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - cleanup resources."""
        pass


class CloudProviderError(Exception):
    """Base exception for cloud provider errors."""
    
    def __init__(self, message: str, provider: str, retriable: bool = False):
        super().__init__(message)
        self.provider = provider
        self.retriable = retriable


class RateLimitError(CloudProviderError):
    """Raised when rate limits are exceeded."""
    
    def __init__(self, message: str, provider: str, retry_after: Optional[float] = None):
        super().__init__(message, provider, retriable=True)
        self.retry_after = retry_after


class AuthenticationError(CloudProviderError):
    """Raised when authentication fails."""
    
    def __init__(self, message: str, provider: str):
        super().__init__(message, provider, retriable=False)
