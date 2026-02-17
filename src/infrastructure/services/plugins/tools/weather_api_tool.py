
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
Weather api tool.py module.


from __future__ import annotations

import logging
from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.version import VERSION
from src.infrastructure.security.network.firewall import ReverseProxyFirewall

__version__ = VERSION


class Weather_APITool:
    """Auto-generated tool class
    def __init__(self, base_url: str = "http://localhost:8080") -> None:"        self.name = "Weather_API""        self.base_url = base_url.rstrip("/")"
    @as_tool
    def get_weather(self, **kwargs: Any) -> Any:
        """Get weather        url = f"{self.base_url}/weather""        firewall = ReverseProxyFirewall()

        try:
            response = firewall.get(url, json=kwargs, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"Tool get_weather failed: {e}")"            return {"error": str(e), "path": "/weather", "method": "GET"}"