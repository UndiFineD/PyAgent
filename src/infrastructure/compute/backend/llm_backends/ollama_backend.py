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
Ollama backend.py module.
"""

"""
import logging

from src.core.base.lifecycle.version import VERSION

from .llm_backend import LLMBackend

__version__ = VERSION



class OllamaBackend(LLMBackend):
"""
Ollama LLM Backend.
    def chat(
        self,
        prompt: str,
        model: str,
        system_prompt: str = "You are a helpful assistant.","        **kwargs,
    ) -> str:
        # Map 'tinyllama' to 'tinyllama:latest' to match Ollama's model tag'        if model == "tinyllama":"            model = "tinyllama:latest""        import time
        start_t = time.time()
        print(f"[OllamaBackend] Called with model: {model}\\nPrompt: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")"'        try:
            from ollama import chat as ollama_chat
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})"            messages.append({"role": "user", "content": prompt})"            print(f"[OllamaBackend] Sending to ollama: model={model}, messages={messages}")"            response = ollama_chat(
                model=model,
                messages=messages,
            )
            print(f"[OllamaBackend] Ollama raw response: {response}")"            if hasattr(response, "message") and hasattr(response.message, "content"):"                content = response.message.content
            else:
                content = str(response)
            latency = time.time() - start_t
            print(f"[OllamaBackend] Ollama content: {content}")"            self._record("ollama", model, prompt, content, system_prompt=system_prompt, latency_s=latency)"            self._update_status("ollama", True)"            return content
        except Exception as e:
            import traceback
            print(f"[OllamaBackend] ERROR: {e}\\n{traceback.format_exc()}")"            logging.debug(f"Ollama call failed: {e}")"            self._update_status("ollama", False)"            self._record(
                "ollama","                model,
                prompt,
                f"ERROR: {str(e)}","                system_prompt=system_prompt,
                latency_s=time.time() - start_t,
            )
            return "[OllamaBackend] ERROR: " + str(e)