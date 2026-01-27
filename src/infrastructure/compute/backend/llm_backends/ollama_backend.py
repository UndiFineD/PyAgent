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
Ollama backend.py module.
"""


from __future__ import annotations

import logging

from src.core.base.lifecycle.version import VERSION

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
        if not self._is_working("ollama"):
            logging.debug("Ollama skipped due to connection cache.")
            return ""

        import os
        from openai import OpenAI

        base_url = kwargs.get("base_url") or os.environ.get("DV_OLLAMA_BASE_URL") or "http://localhost:11434"
        # Ensure base_url ends with /v1 for openai client compatibility if needed, 
        # but Ollama usually listens at root. OpenAI client expects base_url.
        # However, for Ollama via OpenAI client, we usually point to http://localhost:11434/v1
        
        # Check if user provided a full path or just host
        api_base = base_url
        if not api_base.endswith("/v1"):
             api_base = f"{api_base.rstrip('/')}/v1"

        client = OpenAI(base_url=api_base, api_key="ollama")

        import time
        start_t = time.time()

        try:
            # Unifying with Agent logic: Use Chat Completions
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                stream=False
            )
            content = response.choices[0].message.content or ""
            
            latency = time.time() - start_t
            self._record("ollama", model, prompt, content, system_prompt=system_prompt, latency_s=latency)
            self._update_status("ollama", True)
            return content
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            # Lowered logging level for fallback-friendly behavior (Phase 123)
            logging.debug(f"Ollama call failed: {e}")
            self._update_status("ollama", False)
            self._record(
                "ollama",
                model,
                prompt,
                f"ERROR: {str(e)}",
                system_prompt=system_prompt,
                latency_s=time.time() - start_t,
            )
            return ""
