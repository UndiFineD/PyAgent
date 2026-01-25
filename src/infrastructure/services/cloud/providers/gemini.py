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
Google Gemini cloud provider connector.

Provides integration with Google's Gemini API for inference requests.
"""

from __future__ import annotations

import os
import time
from typing import AsyncIterator, Dict, List, Optional

from ..base import (AuthenticationError, CloudProviderBase, CloudProviderError,
                    InferenceRequest, InferenceResponse, RateLimitError)


class GeminiConnector(CloudProviderBase):
    """
    Connector for Google Gemini API.

    Supports Gemini Pro, Gemini Ultra, and other Gemini model variants.

    Example:
        connector = GeminiConnector(api_key="your-api-key")

        request = InferenceRequest(
            messages=[{"role": "user", "content": "Hello!"}],
            model="gemini-pro",
        )

        response = await connector.complete(request)
        print(response.content)
    """

    # Pricing per 1M tokens (input/output) - approximate
    PRICING = {
        "gemini-pro": {"input": 0.50, "output": 1.50},
        "gemini-pro-vision": {"input": 0.50, "output": 1.50},
        "gemini-ultra": {"input": 7.00, "output": 21.00},
        "gemini-1.5-pro": {"input": 3.50, "output": 10.50},
        "gemini-1.5-flash": {"input": 0.35, "output": 1.05},
    }

    def __init__(
        self,
        api_key: Optional[str] = None,
        project_id: Optional[str] = None,
        location: str = "us-central1",
        **config,
    ):
        super().__init__(api_key=api_key, **config)
        self._api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self._project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self._location = location
        self._client = None

    @property
    def name(self) -> str:
        return "Gemini"

    @property
    def available_models(self) -> List[str]:
        return list(self.PRICING.keys())

    async def complete(self, request: InferenceRequest) -> InferenceResponse:
        import httpx

        start_time = time.perf_counter()

        if not self._api_key:
            raise AuthenticationError("Gemini API key is required.", provider="Gemini")

        gemini_contents = []
        for msg in request.messages:
            role = "user" if msg["role"] == "user" else "model"
            gemini_contents.append({"role": role, "parts": [{"text": msg["content"]}]})

        base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        url = f"{base_url}/{request.model}:generateContent?key={self._api_key}"
        payload = {
            "contents": gemini_contents,
            "generationConfig": {
                "temperature": request.temperature,
                "maxOutputTokens": request.max_tokens,
                "topP": request.top_p or 0.95,
            },
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, json=payload)
            except httpx.HTTPError as e:
                raise CloudProviderError(
                    f"Gemini connection failed: {e}",
                    provider="Google Gemini"
                ) from e

            if response.status_code == 429:
                raise RateLimitError(
                    "Gemini API rate limit exceeded.",
                    provider="Google Gemini"
                )
            elif response.status_code != 200:
                raise CloudProviderError(
                    f"Gemini API error ({response.status_code}): {response.text}",
                    provider="Google Gemini"
                )

            data = response.json()
            try:
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                prompt_tokens = len(str(payload)) // 4
                comp_tokens = len(content) // 4
                pricing = self.PRICING.get(request.model, self.PRICING["gemini-1.5-flash"])
                cost = (prompt_tokens * pricing["input"] + comp_tokens * pricing["output"]) / 1_000_000

                return InferenceResponse(
                    content=content,
                    tokens_used=prompt_tokens + comp_tokens,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=comp_tokens,
                    cost_estimate=cost,
                    latency_ms=(time.perf_counter() - start_time) * 1000,
                    provider="Google Gemini",
                    model=request.model,
                    raw_response=data,
                )
            except (KeyError, IndexError) as e:
                raise CloudProviderError(f"Failed to parse Gemini response: {e}", provider="Google Gemini")

    async def stream(self, request: InferenceRequest) -> AsyncIterator[InferenceResponse]:
        import json

        import httpx

        if not self._api_key:
            raise AuthenticationError("Gemini API key is required.", provider="Gemini")

        gemini_contents = []
        for msg in request.messages:
            role = "user" if msg["role"] == "user" else "model"
            gemini_contents.append({"role": role, "parts": [{"text": msg["content"]}]})

        base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        url = (
            f"{base_url}/{request.model}:streamGenerateContent"
            f"?alt=sse&key={self._api_key}"
        )
        payload = {
            "contents": gemini_contents,
            "generationConfig": {
                "temperature": request.temperature,
                "maxOutputTokens": request.max_tokens,
            },
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", url, json=payload) as response:
                if response.status_code != 200:
                    raise CloudProviderError(
                        f"Gemini streaming error ({response.status_code})",
                        provider="Google Gemini"
                    )

                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        try:
                            data = json.loads(line[6:])
                            if "candidates" in data:
                                chunk = data["candidates"][0]["content"]["parts"][0].get("text", "")
                                if chunk:
                                    yield InferenceResponse(
                                        content=chunk,
                                        tokens_used=0,
                                        cost_estimate=0.0,
                                        latency_ms=0.0,
                                        provider="Google Gemini",
                                        model=request.model,
                                    )
                        except json.JSONDecodeError:
                            continue

    async def health_check(self) -> bool:
        """Check if Gemini API is accessible."""
        return self._api_key is not None

    def estimate_cost(self, request: InferenceRequest) -> float:
        """
        Estimate cost for a Gemini request.

        Args:
            request: The inference request.

        Returns:
            Estimated cost in USD.
        """
        model = request.model
        pricing = self.PRICING.get(model, {"input": 1.0, "output": 3.0})

        # Rough estimate: assume 4 chars per token
        input_tokens = sum(len(m.get("content", "")) for m in request.messages) // 4
        output_tokens = request.max_tokens

        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]

        return input_cost + output_cost

    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """
        Format messages for Gemini API.

        Gemini uses a different message format than OpenAI-style APIs.
        """
        # TODO: Implement proper message formatting for Gemini
        # Gemini expects content parts, not OpenAI-style messages
        formatted = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            formatted.append(f"{role}: {content}")
        return "\n".join(formatted)
