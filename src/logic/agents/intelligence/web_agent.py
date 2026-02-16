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

# #
# Web Agent - Web content extraction and scraping orchestration
# #
Brief Summary
# DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
- Import and instantiate where a WebIntelligence-based agent is needed by higher-level orchestrators:
  from <package>.web_agent import WebAgent
  agent = WebAgent(file_path="path/to/config_or_state")
- Intended to be composed into multi-agent workflows that need structured web extraction, scraping tasks, or web-based intelligence collection.
WHAT IT DOES:
- Provides a thin, purpose-specific agent class that specializes the WebIntelligenceAgent core for web scraping and content extraction orchestration.
- Initializes agent state via a single file_path parameter and sets a default system prompt tailored to web intelligence tasks.
- Serves as a stable, importable entrypoint that signals intent and specialization to orchestration logic and prompt-driven cores.
WHAT IT SHOULD DO BETTER:
- Make the system prompt configurable (constructor arg or config object) rather than hard-coded, and support prompt templates per task type.
- Accept dependency injection for HTTP/session clients, rate-limiting, and fetch/backoff strategies to improve testability and operational control.
- Expand constructor and lifecycle to support async operation, richer logging, error handling, politeness (robots.txt), retry/backoff, and integration with StateTransaction and CascadeContext for safe FS modifications and task lineage.
- Add comprehensive docstrings, unit tests, and example usage demonstrating orchestration with WebIntelligenceAgent features and expected lifecycle.
FILE CONTENT SUMMARY:
Web agent.py module.
# #

from .web_intelligence_agent import WebIntelligenceAgent


class WebAgent(WebIntelligenceAgent):  # pylint: disable=too-many-ancestors
""""Agent specialized in web content extraction and scraping orchestration."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
#         self._system_prompt = "You are the WebAgent (via WebIntelligence core).
# #

from .web_intelligence_agent import WebIntelligenceAgent


class WebAgent(WebIntelligenceAgent):  # pylint: disable=too-many-ancestors
""""Agent specialized in web content extraction and scraping orchestration."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
#         self._system_prompt = "You are the WebAgent (via WebIntelligence core).
