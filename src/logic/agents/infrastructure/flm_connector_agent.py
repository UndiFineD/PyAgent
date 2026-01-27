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

"""Agent for connecting to local FastFlowLM instances on NPU edge nodes."""

from __future__ import annotations

<<<<<<< HEAD
import json

=======
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)
import requests

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
<<<<<<< HEAD
from src.infrastructure.security.network.firewall import ReverseProxyFirewall
=======
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)

__version__ = VERSION


# pylint: disable=too-many-ancestors
class FlmConnectorAgent(BaseAgent):
    """Handles local inference requests via the FastFlowLM API (Ryzen AI NPU)."""

    def __init__(self, file_path: str, endpoint: str = "http://localhost:5000") -> None:
        super().__init__(file_path)
        self.endpoint = endpoint
        self._system_prompt = "You are a Neural Processing Unit (NPU) Connector for FastFlowLM."
<<<<<<< HEAD
        self._firewall = ReverseProxyFirewall()

    def check_availability(self) -> bool:
        """Checks if the local FastFlowLM service is reachable using ReverseProxyFirewall."""
        health_url = f"{self.endpoint}/health"

        try:
            # Firewall handles caching, retries, and recording status
            response = self._firewall.get(health_url, timeout=2)
            return response.status_code == 200
        except (requests.RequestException, ConnectionError, TimeoutError) as e:
=======

    def check_availability(self) -> bool:
        """Checks if the local FastFlowLM service is reachable."""
        try:
            # Assuming FastFlowLM has a health endpoint similar to standard inference servers
            response = requests.get(f"{self.endpoint}/health", timeout=2)
            return response.status_code == 200
        except Exception:  # pylint: disable=broad-exception-caught
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)
            return False

    def generate_local(self, prompt: str, model: str = "flm-npu-optimized") -> str:
        """Runs a local inference request on the NPU."""
<<<<<<< HEAD
        # Using firewall check implicitly via the request below, but explicit check provides better error message
=======
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)
        if not self.check_availability():
            return "Error: FastFlowLM service not reachable at " + self.endpoint

        # Standard OpenAI-like completion format often used by these servers
        payload = {"model": model, "prompt": prompt, "max_tokens": 1024, "temperature": 0.7}

        try:
<<<<<<< HEAD
            # Use firewall for POST request
            response = self._firewall.post(f"{self.endpoint}/v1/completions", json=payload, timeout=30)
=======
            response = requests.post(f"{self.endpoint}/v1/completions", json=payload, timeout=30)
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)
            if response.status_code == 200:
                # Assuming standard OpenAI response format
                response_json = response.json()
                if "choices" in response_json and len(response_json["choices"]) > 0:
<<<<<<< HEAD
                    return response_json["choices"][0].get("text", "")
=======
                     return response_json["choices"][0].get("text", "")
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)
                return ""
            
            return f"Error: FastFlowLM returned status {response.status_code}"

<<<<<<< HEAD
        except (requests.RequestException, json.JSONDecodeError, KeyError, ValueError) as e:
=======
        except Exception as e:  # pylint: disable=broad-exception-caught
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)
            return f"Exception during NPU inference: {e}"


if __name__ == "__main__":
    from src.core.base.common.base_utilities import create_main_function
    main = create_main_function(FlmConnectorAgent, "FastFlowLM NPU Connector", "NPU Acceleration logs")
    main()
