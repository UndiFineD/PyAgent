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
Web agent.py module.
"""

from .web_intelligence_agent import WebIntelligenceAgent


class WebAgent(WebIntelligenceAgent):  # pylint: disable=too-many-ancestors
    """Agent specialized in web content extraction and scraping orchestration."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = "You are the WebAgent (via WebIntelligence core)."
