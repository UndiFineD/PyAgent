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


"""Agent for connecting to local Ollama instances on edge nodes (Phase 125)."""

from __future__ import annotations

import logging
import re
from typing import Optional, Dict, Any

import httpx
from openai import AsyncOpenAI, OpenAIError

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION
logger = logging.getLogger(__name__)


# pylint: disable=too-many-ancestors
class OllamaConnectorAgent(BaseAgent):
    """
    Handles local inference requests via the Ollama API (OpenAI-compatible).
    Supports Chat, Reasoning (<think>), and FIM (Fill-In-The-Middle).
    """

    def __init__(self, file_path: str, endpoint: str = "http://localhost:11434/v1") -> None:
        super().__init__(file_path)
        self.endpoint = endpoint
        self._system_prompt = "You are an Edge Intelligence Connector for Ollama."
        # Initialize Async OpenAI Client for Ollama
        self.client = AsyncOpenAI(
            base_url=self.endpoint,
            api_key="ollama",  # Required but unused by Ollama
            http_client=httpx.AsyncClient(timeout=120.0)
        )

    async def check_availability(self) -> bool:
        """Checks if the local Ollama service is reachable."""
        try:
            # Simple models list check
            await self.client.models.list()
            return True
        except (OpenAIError, httpx.HTTPError):
            return False

    async def generate_local(
        self,
        prompt: str,
        model: str = "llama3",
        system: Optional[str] = None,
        suffix: Optional[str] = None,
        reasoning: bool = False,
        json_schema: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Runs a local inference request using OpenAI-compatible endpoints.
        
        Args:
            prompt: User query or code prefix (if suffix is present).
            model: Model name.
            system: System prompt override.
            suffix: Code suffix for FIM (Fill-In-The-Middle) tasks.
            reasoning: If True, parses deepseek-r1 <think> tags.
            json_schema: If provided, enforcing JSON output (Ollama output format).
            
        Returns:
            Dict containing 'content', 'reasoning_trace', and 'cost'.
        """
        if not await self.check_availability():
            return {"error": f"Ollama service not reachable at {self.endpoint}"}

        response_content = ""
        reasoning_content = None

        try:
            if suffix:
                # Use Legacy Completions API for FIM (Fill-In-The-Middle)
                # Note: Not all models support FIM. Codellama/Qwen-Coder do.
                response = await self.client.completions.create(
                    model=model,
                    prompt=prompt,
                    suffix=suffix,
                    max_tokens=2048,
                    stream=False
                )
                response_content = response.choices[0].text
            else:
                # Use Chat Completions API
                messages = [
                    {"role": "system", "content": system or self._system_prompt},
                    {"role": "user", "content": prompt}
                ]
                extra_args = {}
                if json_schema:
                    # Ollama simple JSON mode or structured output if supported
                    extra_args["response_format"] = {"type": "json_object"}
                
                response = await self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=False,
                    **extra_args
                )
                response_content = response.choices[0].message.content or ""
                # Phase 130: Reasoning Parsing (<think>)
                if reasoning or "<think>" in response_content:
                    reasoning_match = re.search(r"<think>(.*?)</think>", response_content, re.DOTALL)
                    if reasoning_match:
                        reasoning_content = reasoning_match.group(1).strip()
                        # Clean the output by removing the thought trace
                        response_content = re.sub(r"<think>.*?</think>", "", response_content, flags=re.DOTALL).strip()

            result_payload = {
                "content": response_content, 
                "reasoning_trace": reasoning_content,
                "model": model,
                "provider": "ollama"
            }

            # Phase 120: Harvest intelligence/interaction to shards
            if hasattr(self, "recorder") and self.recorder:
                self.recorder.record_interaction(
                    provider="Ollama",
                    model=model,
                    prompt=prompt,
                    result=response_content,
                    meta={"reasoning": reasoning_content}
                )
            return result_payload

        except (Exception, ConnectionError, TimeoutError, ValueError, KeyError) as e:  # pylint: disable=broad-exception-caught
            error_msg = f"Exception during local inference: {e}"
            logger.error(error_msg)
            return {"error": error_msg}


if __name__ == "__main__":
    from src.core.base.common.base_utilities import create_main_function

    main = create_main_function(OllamaConnectorAgent, "Ollama Edge Connector", "Edge Intelligence logs")
    main()
