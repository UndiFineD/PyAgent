"""
Azure AI Foundry cloud provider connector.

Provides integration with Azure AI Foundry (formerly Azure ML) for inference requests.
"""

from __future__ import annotations

import os
import time
import json
import logging
from typing import AsyncIterator, List, Optional, Dict, Any

from ..base import (
    CloudProviderBase,
    InferenceRequest,
    InferenceResponse,
    CloudProviderError,
    RateLimitError,
    AuthenticationError,
)

logger = logging.getLogger(__name__)

class AzureAIConnector(CloudProviderBase):
    """
    Connector for Azure AI Foundry models.
    
    Supports models hosted on Azure AI Foundry endpoints, 
    including Llama 3, Phi-3, Cohere, etc.
    
    Compatible with OpenAI-style API endpoints provided by Azure.
    """
    
    # Pricing per 1M tokens (input/output) - approximate (Standard Azure Pay-As-Go)
    PRICING = {
        "gpt-4": {"input": 30.00, "output": 60.00},
        "gpt-4o": {"input": 5.00, "output": 15.00},
        "gpt-35-turbo": {"input": 0.50, "output": 1.50},
        "meta-llama-3-70b-instruct": {"input": 0.65, "output": 2.75},
        "meta-llama-3-8b-instruct": {"input": 0.15, "output": 0.15},
        "phi-3-mini-4k-instruct": {"input": 0.10, "output": 0.10},
    }
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        api_version: str = "2024-02-01",
        **config,
    ):
        """
        Initialize Azure AI Connector.
        
        Args:
            api_key: Azure AI Registry or Endpoint key.
            endpoint: Full endpoint URL (e.g., https://<name>.<region>.inference.ai.azure.com).
            api_version: API version for Azure requests.
            **config: Additional options.
        """
        super().__init__(api_key=api_key, **config)
        self._api_key = api_key or os.getenv("AZURE_AI_KEY")
        self._endpoint = endpoint or os.getenv("AZURE_AI_ENDPOINT")
        self._api_version = api_version
        
    @property
    def name(self) -> str:
        return "AzureAI"
        
    @property
    def available_models(self) -> List[str]:
        return list(self.PRICING.keys())
        
    async def complete(self, request: InferenceRequest) -> InferenceResponse:
        import httpx
        start_time = time.perf_counter()
        
        if not self._api_key or not self._endpoint:
            raise AuthenticationError("Azure AI API key and endpoint are required.")

        # Azure endpoints often use /v1/chat/completions for OpenAI compatibility
        url = self._endpoint
        if not url.endswith("/chat/completions"):
            url = f"{self._endpoint.rstrip('/')}/v1/chat/completions"
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}" if not self._is_entra_token() else f"Bearer {self._api_key}",
            "api-key": self._api_key # Azure specific header
        }
        
        payload = {
            "messages": request.messages,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "top_p": request.top_p or 1.0,
            "stream": False # Streaming handled separately if needed
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
            except Exception as e:
                raise CloudProviderError(f"Azure AI connection failed: {e}")
            
            if response.status_code == 429:
                raise RateLimitError("Azure AI rate limit exceeded.")
            elif response.status_code != 200:
                raise CloudProviderError(f"Azure AI returned error {response.status_code}: {response.text}")
                
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            
            # Simple token estimation if usage not returned
            usage = data.get("usage", {})
            input_tokens = usage.get("prompt_tokens", len(str(request.messages)) // 4)
            output_tokens = usage.get("completion_tokens", len(content) // 4)
            
            cost = self._calculate_cost(request.model, input_tokens, output_tokens)
            latency = (time.perf_counter() - start_time) * 1000
            
            return InferenceResponse(
                content=content,
                model=request.model,
                provider=self.name,
                latency_ms=latency,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost=cost,
                raw_response=data
            )

    def _is_entra_token(self) -> bool:
        # Check if the key looks like an Entra id token or a simple API key
        return len(self._api_key) > 64 # Heuristic

    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        pricing = self.PRICING.get(model, {"input": 1.0, "output": 1.0})
        return (input_tokens / 1_000_000 * pricing["input"]) + (output_tokens / 1_000_000 * pricing["output"])
