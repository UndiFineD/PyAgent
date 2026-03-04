#!/usr/bin/env python3
from __future__ import annotations
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


import logging
import os
import time

from src.core.base.Version import VERSION  # type: ignore
from .llm_backend import LLMBackend

__version__ = VERSION


class OllamaBackend(LLMBackend):
    """Ollama LLM Backend."""

    def chat(
        self,
        prompt: str,
        model: str,
        system_prompt: str = "You are a helpful assistant.",
        **kwargs,
    ) -> str:
        """
        Send a chat request to the Ollama LLM backend and return the response.

        Args:
            prompt: The user prompt to send to the model.
            model: The model name to use for inference.
            system_prompt: The system prompt to set the assistant's behavior.
            **kwargs: Additional arguments including base_url and timeout_s.

        Returns:
            The model's response as a string, or an empty string on failure.
        """
        if not self._is_working("ollama"):
            logging.debug("Ollama skipped due to connection cache.")
            return ""

        base_url = (
            kwargs.get("base_url")
            or os.environ.get("DV_OLLAMA_BASE_URL")
            or "http://localhost:11434"
        )
        url = base_url.rstrip("/") + "/api/generate"
        payload = {
            "model": model,
            "system": system_prompt,
            "prompt": prompt,
            "stream": False,
        }

        timeout_s = kwargs.get("timeout_s", 120)
        start_t = time.time()

        try:
            response = self.session.post(url, json=payload, timeout=timeout_s)
            response.raise_for_status()
            content = response.json().get("response", "")
            latency = time.time() - start_t
            self._record("ollama", model, prompt, content, system_prompt=system_prompt, latency_s=latency)
            self._update_status("ollama", True)
            return content
        except Exception as e:
            # Lowered logging level for fallback-friendly behavior (Phase 123)
            logging.debug(f"Ollama call failed: {e}")
            self._update_status("ollama", False)
            self._record(
                "ollama", 
                model,
                prompt,
                f"ERROR: {str(e)}",
                system_prompt=system_prompt,
                latency_s=time.time() - start_t
            )
            return ""
