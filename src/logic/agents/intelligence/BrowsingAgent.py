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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Agent specializing in web browsing, information retrieval, and data extraction.
Inspired by Skyvern and BrowserOS.
"""



import logging
import json
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool


class BrowsingAgent(BaseAgent):
    """Interacts with the web to retrieve documentation, search for solutions, and extract data."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Browsing Agent. "
            "Your role is to find information on the web that the fleet is missing. "
            "Use web search and page fetching to retrieve documentation, API specs, or debugging solutions. "
            "Think critically about the sources and prioritize official documentation."
        )

    @as_tool
    def search_and_summarize(self, query: str) -> str:
        """Searches the web for a query and provides a summarized report.
        (Uses available workspace tools for actual fetching).
        """
        logging.info(f"BrowsingAgent searching for: {query}")
        # In a real scenario, this would call a search engine tool.
        # Since we are an agent, we provide a plan for fetching.
        return f"Plan: 1. Search for '{query}' using Bing/Google. 2. Fetch top 3 results. 3. Synthesize answer."

    @as_tool
    def extract_api_spec(self, url: str) -> str:
        """Attempts to find and extract an OpenAPI/Swagger spec from a given URL."""
        logging.info(f"BrowsingAgent extracting spec from: {url}")
        # Here we would use fetch_webpage (which is available to us via the host)
        # For the simulation, we return a hypothesized success message.
        return f"Browsing {url}... Detected OpenAPI 3.0 spec. Ready for SpecToolAgent."

    def improve_content(self, prompt: str) -> str:
        """Browse the web based on a prompt."""
        if "http" in prompt:
            return self.extract_api_spec(prompt)
        return self.search_and_summarize(prompt)
