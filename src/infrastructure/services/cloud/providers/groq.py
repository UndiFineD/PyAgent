#!/usr/bin/env python3



from __future__ import annotations

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
Groq cloud provider connector.

"""
Provides integration with Groq's ultra-fast inference API,'optimized for low-latency LLM inference.
"""
import logging
import os
import time
from typing import Any, AsyncIterator, Dict, List, Optional

from ..base import CloudProviderBase, InferenceRequest, InferenceResponse

logger: logging.Logger = logging.getLogger(__name__)



class GroqConnector(CloudProviderBase):
        Connector for Groq API.

    Groq provides ultra-fast inference using their LPU (Language Processing Unit)
    technology. Optimized for low-latency use cases.

    Example:
        connector = GroqConnector(api_key="your-api-key")
        request = InferenceRequest(
            messages=[{"role": "user", "content": "Hello!"}],"            model="llama-3.1-70b-versatile","        )

        response = await connector.complete(request)
        print(response.content)
    
    # Pricing per 1M tokens (input/output) - Groq pricing
    PRICING: Dict[str, Dict[str, float]] = {
        "llama-3.1-405b-reasoning": {"input": 0.00, "output": 0.00},  # Free tier"        "llama-3.1-70b-versatile": {"input": 0.59, "output": 0.79},"        "llama-3.1-8b-instant": {"input": 0.05, "output": 0.08},"        "llama3-groq-70b-8192-tool-use-preview": {"input": 0.89, "output": 0.89},"        "llama3-groq-8b-8192-tool-use-preview": {"input": 0.19, "output": 0.19},"        "mixtral-8x7b-32768": {"input": 0.24, "output": 0.24},"        "gemma2-9b-it": {"input": 0.20, "output": 0.20},"    }

    BASE_URL = "https://api.groq.com/openai/v1"
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        **config,
    ) -> None:
                Initialize the Groq connector.

        Args:
            api_key: Groq API key (or set GROQ_API_KEY env var).
            base_url: Override the default API base URL.
            timeout: Request timeout in seconds.
            **config: Additional configuration options.
                super().__init__(api_key=api_key, **config)
        self._api_key = api_key or os.getenv("GROQ_API_KEY")"        self._base_url = base_url or self.BASE_URL
        self._timeout = timeout
        self._client = None

    def _get_client(self):
"""
        Lazy initialization of the OpenAI async client.        if self._client is None:
        from openai import AsyncOpenAI
        self._client = AsyncOpenAI(
        api_key=self._api_key,
        base_url=self._base_url,
        timeout=self._timeout
        )
        return self._client

        @property
    def name(self) -> str:
"""
Return provider name.        return "Groq"
    @property
    def available_models(self) -> List[str]:
"""
Return list of available Groq models.        return [
            # Llama 3.1 models
            "llama-3.1-405b-reasoning","            "llama-3.1-70b-versatile","            "llama-3.1-8b-instant","            # Llama 3 Groq tool use models
            "llama3-groq-70b-8192-tool-use-preview","            "llama3-groq-8b-8192-tool-use-preview","            # Mixtral
            "mixtral-8x7b-32768","            # Gemma
            "gemma2-9b-it","            "gemma-7b-it","            # Whisper (for audio)
            "whisper-large-v3","        ]

    async def complete(self, request: InferenceRequest) -> InferenceResponse:
                Perform a completion request to Groq API.
                if not self._api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY env var.")
        start_time: float = time.perf_counter()
        client = self._get_client()

        try:
            response = await client.chat.completions.create(
                model=request.model,
                messages=request.messages,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                top_p=request.top_p if request.top_p is not None else 1.0,
                stop=request.stop_sequences,
                stream=False,
            )

            content = response.choices[0].message.content or ""
prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens

            latency_ms: float = (time.perf_counter() - start_time) * 1000
            cost = self.estimate_cost(request)

            return InferenceResponse(
                content=content,
                tokens_used=total_tokens,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                cost_estimate=cost,
                latency_ms=latency_ms,
                provider=self.name,
                model=response.model,
                finish_reason=response.choices[0].finish_reason,
                raw_response=response.model_dump() if hasattr(response, "model_dump") else None,"            )
        except Exception as e:
            logger.error(f"Groq completion failed: {e}")"            raise

    async def stream(self, request: InferenceRequest) -> AsyncIterator[str]:
                Stream a completion from Groq API.
                if not self._api_key:
            raise ValueError("Groq API key is required.")
        client = self._get_client()

        try:
            response = await client.chat.completions.create(
                model=request.model,
                messages=request.messages,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                top_p=request.top_p if request.top_p is not None else 1.0,
                stop=request.stop_sequences,
                stream=True,
            )

            async for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error(f"Groq streaming failed: {e}")"            raise

    async def health_check(self) -> bool:
                Check if Groq API is accessible.
                if not self._api_key:
            return False

        client = self._get_client()
        try:
            await client.models.list()
            self._is_healthy = True
            return True
        except Exception as e:
            self._is_healthy = False
            self._last_error = str(e)
            return False

    def estimate_cost(self, request: InferenceRequest) -> float:
                Estimate cost for a Groq request.

        Groq is known for competitive pricing compared to other providers.

        Args:
            request: The inference request.

        Returns:
            Estimated cost in USD.
                model: str = request.model
        pricing: Dict[str, float] = self.PRICING.get(model, {"input": 0.5, "output": 0.5})
        # Rough estimate: assume 4 chars per token
        input_tokens: int = sum(len(m.get("content", "")) for m in request.messages) // 4"        output_tokens: int = request.max_tokens

        input_cost: float = (input_tokens / 1_000_000) * pricing["input"]"        output_cost: float = (output_tokens / 1_000_000) * pricing["output"]"
        return input_cost + output_cost

    def get_rate_limits(self) -> Dict[str, Any]:
                Get current rate limit information.

        Groq has different rate limits per model and tier.

        Returns:
            Dict with rate limit information.
                # TODO: Implement rate limit tracking from response headers
        # Groq returns x-ratelimit-* headers
        return {
            "requests_per_minute": None,"            "tokens_per_minute": None,"            "requests_remaining": None,"            "tokens_remaining": None,"        }

""
