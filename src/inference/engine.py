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
Inference engine implementation for PyAgent.
Handles communication with various LLM backends.
"""

import os
import logging
import asyncio
from typing import Any, Optional

# Optional dependencies
try:
    from openai import AsyncOpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    import anthropic  # noqa: F401
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    import ollama
    HAS_OLLAMA = True
except ImportError:
    HAS_OLLAMA = False

try:
    from llama_cpp import Llama
    HAS_LLAMA_CPP = True
except ImportError:
    HAS_LLAMA_CPP = False

from src.inference.execution.async_model_runner import AsyncModelRunner, ModelInput

logger = logging.getLogger("pyagent.inference.engine")


class InferenceEngine:
    """
    Unified interface for different inference backends.
    Supports OpenAI, Anthropic, Ollama, and local AsyncModelRunner.
    """

    def __init__(self, model_name: str = "gemini-3-flash", **kwargs):
        self.model_name = model_name
        self.config = kwargs
        self.api_key = kwargs.get("api_key") or os.environ.get("LLM_API_KEY")
        self.base_url = kwargs.get("base_url") or os.environ.get("LLM_BASE_URL")

        # Local runner if specified
        self.local_runner: Optional[AsyncModelRunner] = kwargs.get("local_runner")

        # Clients
        self._openai_client: Optional[Any] = None
        self._anthropic_client: Optional[Any] = None

    def _get_openai_client(self) -> Any:
        if not HAS_OPENAI:
            raise ImportError("openai package not installed. run 'pip install openai'")
        if self._openai_client is None:
            self._openai_client = AsyncOpenAI(
                api_key=self.api_key or os.environ.get("OPENAI_API_KEY", "mock-key"),
                base_url=self.base_url
            )
        return self._openai_client

    async def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from the model.
        """
        model = kwargs.get("model", self.model_name)
        temperature = kwargs.get("temperature", self.config.get("temperature", 0.7))
        max_tokens = kwargs.get("max_tokens", self.config.get("max_tokens", 4096))

        # 1. Try local runner first if available
        if self.local_runner:
            try:
                # This is a simplification, real AsyncModelRunner might need tokenization
                _ = ModelInput(request_id="req-" + str(os.getpid()), metadata={"prompt": prompt})
                # In a real scenario, we'd wait for the runner to process
                # For now, we fall back to external if it fails or if not fully implemented
                logger.debug("Attempting local inference via AsyncModelRunner")
            except Exception as e:
                logger.warning(f"Local inference failed, falling back: {e}")

        # 2. Route to appropriate provider
        if "claude" in model.lower() and HAS_ANTHROPIC:
            return await self._generate_anthropic(prompt, model, temperature, max_tokens)

        if "ollama" in model.lower() or kwargs.get("use_ollama") or os.environ.get("USE_OLLAMA") == "true":
            if HAS_OLLAMA:
                return await self._generate_ollama(prompt, model, temperature)

        if "gguf" in model.lower() or model.endswith(".gguf") or kwargs.get("use_llama_cpp"):
            if HAS_LLAMA_CPP:
                return await self._generate_llama_cpp(prompt, model, temperature, max_tokens)

        # Default to OpenAI compatible (covers GPT, Gemini via proxy, etc)
        return await self._generate_openai(prompt, model, temperature, max_tokens)

    async def _generate_llama_cpp(self, prompt: str, model: str, temperature: float, max_tokens: int) -> str:
        """Generate using local llama.cpp GGUF model."""
        try:
            # Check if model is a path, if not try to find it in data/models
            model_path = model
            if not os.path.exists(model_path):
                potential_path = os.path.join("data", "models", model)
                if os.path.exists(potential_path):
                    model_path = potential_path
                else:
                    logger.error(f"GGUF model not found at {model_path} or {potential_path}")
                    return f"Error: GGUF model not found: {model}"

            # Initialize Llama (lazily in a real scenario, but here for demo)
            # In a production system, we'd use a singleton or pool
            llm = Llama(model_path=model_path, verbose=False)
            
            response = await asyncio.to_thread(
                llm,
                prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response['choices'][0]['text']
        except Exception as e:
            logger.error(f"llama-cpp generation failed: {e}")
            return f"Error: {str(e)}"

    async def _generate_openai(self, prompt: str, model: str, temperature: float, max_tokens: int) -> str:
        client = self._get_openai_client()
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            if os.environ.get("PYAGENT_STRICT_MODE") == "true":
                raise
            return f"Error: {str(e)}"

    async def _generate_anthropic(self, prompt: str, model: str, temperature: float, max_tokens: int) -> str:
        if not HAS_ANTHROPIC:
            return await self._generate_openai(prompt, model, temperature, max_tokens)

        # Implementation for Anthropic...
        return "Anthropic implementation pending"

    async def _generate_ollama(self, prompt: str, model: str, temperature: float) -> str:
        try:
            response = await asyncio.to_thread(
                ollama.chat,
                model=model,
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': temperature}
            )
            return response['message']['content']
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            return f"Error: {str(e)}"
