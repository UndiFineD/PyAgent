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

import requests

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class OllamaConnectorAgent(BaseAgent):
    """Handles local inference requests via the Ollama API."""

    def __init__(self, file_path: str, endpoint: str = "http://localhost:11434") -> None:
        super().__init__(file_path)
        self.endpoint = endpoint
        self._system_prompt = "You are an Edge Intelligence Connector for Ollama."

    def check_availability(self) -> bool:
        """Checks if the local Ollama service is reachable."""
        try:
            response = requests.get(f"{self.endpoint}/api/tags", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def generate_local(self, prompt: str, model: str = "llama3") -> str:
        """Runs a local inference request."""
        if not self.check_availability():
            return "Error: Ollama service not reachable at " + self.endpoint

        payload = {"model": model, "prompt": prompt, "stream": False}

        try:
            response = requests.post(f"{self.endpoint}/api/generate", json=payload)
            response_text = ""
            if response.status_code == 200:
                response_text = response.json().get("response", "")
            else:
                response_text = f"Error: Ollama returned status {response.status_code}"

            # Phase 120: Harvest intelligence/interaction to shards
            if hasattr(self, "recorder") and self.recorder:
                self.recorder.record_interaction(provider="Ollama", model=model, prompt=prompt, result=response_text)
            return response_text
        except Exception as e:
            error_msg = f"Exception during local inference: {e}"

            if hasattr(self, "recorder") and self.recorder:
                self.recorder.record_interaction(
                    provider="Ollama",
                    model=model,
                    prompt=prompt,
                    result=error_msg,
                    meta={"status": "exception"},
                )
            return error_msg


if __name__ == "__main__":
    from src.core.base.common.base_utilities import create_main_function

    main = create_main_function(OllamaConnectorAgent)
    main()
