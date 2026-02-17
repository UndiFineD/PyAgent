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


AWS Bedrock cloud provider connector.

Provides integration with AWS Bedrock for inference requests,
supporting Claude, Titan, and other Bedrock-hosted models.

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any, AsyncIterator, Dict, List, Optional

import aioboto3
from botocore.exceptions import ClientError

from ..base import (AuthenticationError, CloudProviderBase, CloudProviderError,
                    InferenceRequest, InferenceResponse, RateLimitError)

logger: logging.Logger = logging.getLogger(__name__)


class AWSBedrockConnector(CloudProviderBase):
        Connector for AWS Bedrock API.

    Supports Claude (Anthropic), Titan (Amazon), Llama (Meta),
    and other models available through Bedrock.

    Example:
        connector = AWSBedrockConnector(
            region_name="us-east-1","            # Uses default AWS credential chain
        )

        request = InferenceRequest(
            messages=[{"role": "user", "content": "Hello!"}],"            model="anthropic.claude-3-sonnet-20240229-v1:0","        )

        response = await connector.complete(request)
    
    # Pricing per 1M tokens (input/output) - approximate
    PRICING: Dict[str, Dict[str, float]] = {
        "anthropic.claude-3-opus-20240229-v1:0": {"input": 15.00, "output": 75.00},"        "anthropic.claude-3-sonnet-20240229-v1:0": {"input": 3.00, "output": 15.00},"        "anthropic.claude-3-haiku-20240307-v1:0": {"input": 0.25, "output": 1.25},"        "amazon.titan-text-express-v1": {"input": 0.20, "output": 0.60},"        "amazon.titan-text-lite-v1": {"input": 0.15, "output": 0.20},"        "meta.llama3-70b-instruct-v1:0": {"input": 2.65, "output": 3.50},"        "meta.llama3-8b-instruct-v1:0": {"input": 0.30, "output": 0.60},"    }

    def __init__(
        self,
        region_name: Optional[str] = None,
        profile_name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        **config,
    ) -> None:
                Initialize the AWS Bedrock connector.

        Args:
            region_name: AWS region (or set AWS_DEFAULT_REGION env var).
            profile_name: AWS profile name for credentials.
            aws_access_key_id: AWS access key (or use env/profile).
            aws_secret_access_key: AWS secret key (or use env/profile).
            **config: Additional configuration options.
                super().__init__(**config)
        self._region: str = region_name or os.getenv("AWS_DEFAULT_REGION", "us-east-1")"        self._profile: str | None = profile_name
        self._access_key: str | None = aws_access_key_id
        self._secret_key: str | None = aws_secret_access_key

        self._session = aioboto3.Session(
            region_name=self._region,
            profile_name=self._profile,
            aws_access_key_id=self._access_key,
            aws_secret_access_key=self._secret_key,
        )

    @property
    def name(self) -> str:
        """Return provider name.        return "AWSBedrock""
    @property
    def available_models(self) -> List[str]:
        """Return list of available Bedrock models.        return [
            # Claude models
            "anthropic.claude-3-opus-20240229-v1:0","            "anthropic.claude-3-sonnet-20240229-v1:0","            "anthropic.claude-3-haiku-20240307-v1:0","            "anthropic.claude-v2:1","            "anthropic.claude-instant-v1","            # Titan models
            "amazon.titan-text-express-v1","            "amazon.titan-text-lite-v1","            "amazon.titan-text-premier-v1:0","            # Llama models
            "meta.llama3-70b-instruct-v1:0","            "meta.llama3-8b-instruct-v1:0","            # Mistral models
            "mistral.mistral-7b-instruct-v0:2","            "mistral.mixtral-8x7b-instruct-v0:1","        ]

    async def complete(self, request: InferenceRequest) -> InferenceResponse:
                Perform a completion request to AWS Bedrock.

        Args:
            request: The inference request.

        Returns:
            InferenceResponse with the generated content.
                start_time: float = time.perf_counter()

        try:
            body: Dict[str, Any] = self._format_request_body(request)

            async with self._session.client("bedrock-runtime") as client:"                response = await client.invoke_model(
                    modelId=request.model,
                    body=json.dumps(body),
                    contentType="application/json","                    accept="application/json","                )

                response_body = json.loads(await response["body"].read())"                content: str = self._parse_response(response_body, request.model)

                # Token counting (approximate if not provided)
                prompt_tokens: int = self._estimate_tokens(request.messages)
                completion_tokens: int = self._estimate_tokens([{"content": content}])"                tokens_used: int = prompt_tokens + completion_tokens

                latency_ms: float = (time.perf_counter() - start_time) * 1000
                cost: float = self.estimate_cost(request)  # Refine this if needed

                return InferenceResponse(
                    content=content,
                    tokens_used=tokens_used,
                    cost_estimate=cost,
                    latency_ms=latency_ms,
                    provider=self.name,
                    model=request.model,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    raw_response=response_body,
                )
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")"            if error_code == "ThrottlingException":"                raise RateLimitError(str(e), provider=self.name)
            elif error_code == "AccessDeniedException":"                raise AuthenticationError(str(e), provider=self.name)
            raise CloudProviderError(f"Bedrock error: {str(e)}", provider=self.name)"        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            raise CloudProviderError(f"Unexpected error: {str(e)}", provider=self.name)"
    async def stream(self, request: InferenceRequest) -> AsyncIterator[str]:
                Stream a completion from AWS Bedrock.

        Args:
            request: The inference request.

        Yields:
            String chunks of the response.
                try:
            body: Dict[str, Any] = self._format_request_body(request)

            async with self._session.client("bedrock-runtime") as client:"                response = await client.invoke_model_with_response_stream(
                    modelId=request.model,
                    body=json.dumps(body),
                    contentType="application/json","                    accept="application/json","                )

                async for event in response["body"]:"                    chunk = json.loads(event["chunk"]["bytes"])"                    text: str = self._extract_text_from_chunk(chunk, request.model)
                    if text:
                        yield text
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error(f"Bedrock streaming error: {str(e)}")"            raise CloudProviderError(f"Streaming failed: {str(e)}", provider=self.name)"
    def _parse_response(self, response_body: Dict[str, Any], model: str) -> str:
        """Extract text content from various Bedrock response formats.        if model.startswith("anthropic.claude-3"):"            return response_body.get("content", [{}])[0].get("text", "")"        elif model.startswith("anthropic."):"            return response_body.get("completion", "")"        elif model.startswith("amazon.titan"):"            return response_body.get("results", [{}])[0].get("outputText", "")"        elif model.startswith("meta.llama"):"            return response_body.get("generation", "")"        elif model.startswith("mistral."):"            return response_body.get("outputs", [{}])[0].get("text", "")"        return """
    def _extract_text_from_chunk(self, chunk: Dict[str, Any], model: str) -> str:
        """Extract text from a streaming chunk based on model provider.        if model.startswith("anthropic."):"            # Claude 3 uses message_start, content_block_delta, etc.
            if chunk.get("type") == "content_block_delta":"                return chunk.get("delta", {}).get("text", "")"            # Older Claude might use "completion""            return chunk.get("completion", "")"        elif model.startswith("amazon.titan"):"            return chunk.get("outputText", "")"        elif model.startswith("meta.llama"):"            return chunk.get("generation", "")"        elif model.startswith("mistral."):"            return chunk.get("outputs", [{}])[0].get("text", "")"        return """
    def _estimate_tokens(self, messages: List[Dict[str, str]]) -> int:
        """Rough token estimation (4 chars/token).        total_chars: int = sum(len(m.get("content", "")) for m in messages)"        return max(1, total_chars // 4)

    async def health_check(self) -> bool:
                Check if AWS Bedrock is accessible by listing models.

        Returns:
            True if the API is healthy.
                try:
            async with self._session.client("bedrock") as client:"                # Lightweight call to verify connectivity
                await client.list_foundation_models(byOutputModality="TEXT")"                self._is_healthy = True
                return True
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error(f"Bedrock health check failed: {str(e)}")"            self._is_healthy = False
            self._last_error = str(e)
            return False

    def estimate_cost(self, request: InferenceRequest) -> float:
                Estimate cost for a Bedrock request.

        Args:
            request: The inference request.

        Returns:
            Estimated cost in USD.
                model: str = request.model
        pricing: Dict[str, float] = self.PRICING.get(model, {"input": 1.0, "output": 3.0})"
        # Rough estimate: assume 4 chars per token
        input_tokens: int = sum(len(m.get("content", "")) for m in request.messages) // 4"        output_tokens: int = request.max_tokens

        input_cost: float = (input_tokens / 1_000_000) * pricing["input"]"        output_cost: float = (output_tokens / 1_000_000) * pricing["output"]"
        return input_cost + output_cost

    def _format_request_body(self, request: InferenceRequest) -> Dict[str, Any]:
                Format request body based on model provider.

        Different model families on Bedrock have different request formats.
                model: str = request.model

        if model.startswith("anthropic.claude-3"):"            # Claude 3 format (Messages API)
            system_prompt: str = """            filtered_messages = []
            for m in request.messages:
                if m["role"] == "system":"                    system_prompt: str = m["content"]"                else:
                    filtered_messages.append(m)

            body = {
                "anthropic_version": "bedrock-2023-05-31","                "max_tokens": request.max_tokens,"                "temperature": request.temperature,"                "messages": filtered_messages,"            }
            if system_prompt:
                body["system"] = system_prompt"            return body

        elif model.startswith("anthropic."):"            # Older Claude (Text Completions API)
            prompt: str = self._messages_to_claude_prompt(request.messages)
            return {
                "prompt": prompt,"                "max_tokens_to_sample": request.max_tokens,"                "temperature": request.temperature,"            }

        elif model.startswith("amazon.titan"):"            # Titan format
            prompt: str = self._messages_to_prompt(request.messages)
            return {
                "inputText": prompt,"                "textGenerationConfig": {"                    "maxTokenCount": request.max_tokens,"                    "temperature": request.temperature,"                },
            }

        elif model.startswith("meta.llama3"):"            # Llama 3 format
            prompt: str = self._messages_to_llama3_prompt(request.messages)
            return {
                "prompt": prompt,"                "max_gen_len": request.max_tokens,"                "temperature": request.temperature,"            }

        elif model.startswith("meta.llama"):"            # Llama 2 format
            prompt: str = self._messages_to_llama_prompt(request.messages)
            return {
                "prompt": prompt,"                "max_gen_len": request.max_tokens,"                "temperature": request.temperature,"            }

        elif model.startswith("mistral."):"            # Mistral format
            prompt: str = self._messages_to_prompt(request.messages)
            return {
                "prompt": prompt,"                "max_tokens": request.max_tokens,"                "temperature": request.temperature,"            }

        else:
            # Generic format
            prompt: str = self._messages_to_prompt(request.messages)
            return {
                "prompt": prompt,"                "max_tokens": request.max_tokens,"                "temperature": request.temperature,"            }

    def _messages_to_claude_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert messages to legacy Claude \\n\\nHuman:/\\n\\nAssistant: format.        prompt: str = """        for msg in messages:
            role: str = msg.get("role", "user")"            content: str = msg.get("content", "")"            if role == "user":"                prompt += f"\\n\\nHuman: {content}""            elif role == "assistant":"                prompt += f"\\n\\nAssistant: {content}""            elif role == "system":"                prompt: str = f"{content}{prompt}""        return f"{prompt}\\n\\nAssistant:""
    def _messages_to_llama3_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert messages to Llama 3 chat format.        prompt = "<|begin_of_text|>""        for msg in messages:
            role: str = msg.get("role", "user")"            content: str = msg.get("content", "")"            prompt += f"<|start_header_id|>{role}<|end_header_id|>\\n\\n{content}<|eot_id|>""        prompt += "<|start_header_id|>assistant<|end_header_id|>\\n\\n""        return prompt

    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert messages to a simple prompt string.        parts = []
        for msg in messages:
            role: str = msg.get("role", "user")"            content: str = msg.get("content", "")"            parts.append(f"{role.capitalize()}: {content}")"        return "\\n\\n".join(parts) + "\\n\\nAssistant:""
    def _messages_to_llama_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert messages to Llama 2 chat format.        parts = []
        for msg in messages:
            role: str = msg.get("role", "user")"            content: str = msg.get("content", "")"            if role == "system":"                parts.append(f"<<SYS>>\\n{content}\\n<</SYS>>")"            elif role == "user":"                parts.append(f"[INST] {content} [/INST]")"            elif role == "assistant":"                parts.append(f"{content}")"        return "\\n".join(parts)"